#!/usr/bin/env python3
"""Read-only width-transition inventory and geometric triage.

Run with tmp/layout-venv/bin/python (pcbnew + Shapely 2). Does not save boards.
Reports direct joints, T junctions, and overlapping-copper joins; evaluates the
whole contiguous narrow run, not just the segment next to a width transition.
Geometric widening proposals require KiCad DRC and electrical review before use.
"""
import argparse, csv, hashlib, json, math
from collections import Counter, defaultdict
from pathlib import Path
import pcbnew as pcb
from shapely.geometry import Point, LineString, Polygon
from shapely.ops import nearest_points, unary_union
from shapely.strtree import STRtree

EPS = .000002  # 2 nm tolerance, in mm

def xy(v): return (v.x / 1e6, v.y / 1e6)
def uid(t): return t.m_Uuid.AsString()
def polygons(poly):
    result = []
    for i in range(poly.OutlineCount()):
        out = poly.COutline(i)
        holes = []
        for h in range(poly.HoleCount(i)):
            hole = poly.CHole(i, h)
            holes.append([xy(hole.CPoint(k)) for k in range(hole.PointCount())])
        result.append(Polygon([xy(out.CPoint(k)) for k in range(out.PointCount())], holes))
    return unary_union(result)

def track_line(t):
    if isinstance(t, pcb.PCB_ARC):
        # A copper arc has the same width semantics as a straight segment.
        a, m, c = xy(t.GetStart()), xy(t.GetMid()), xy(t.GetEnd())
        center = xy(t.GetCenter()); r = math.dist(a, center)
        angles = [math.atan2(q[1]-center[1], q[0]-center[0]) for q in [a,m,c]]
        sweep = (angles[2]-angles[0]) % (2*math.pi)
        if (angles[1]-angles[0]) % (2*math.pi) > sweep: sweep -= 2*math.pi
        n = max(8, math.ceil(abs(sweep)*r/.005))
        return LineString([(center[0]+r*math.cos(angles[0]+sweep*i/n), center[1]+r*math.sin(angles[0]+sweep*i/n)) for i in range(n+1)])
    return LineString([xy(t.GetStart()),xy(t.GetEnd())])

def audit(path):
    path = Path(path); b = pcb.LoadBoard(str(path)); origin = xy(b.GetDesignSettings().GetAuxOrigin())
    pro = path.with_suffix('.kicad_pro')
    config = json.loads(pro.read_text()) if pro.exists() else {}
    rules = config.get('board',{}).get('design_settings',{}).get('rules',{})
    classes = config.get('net_settings',{}).get('classes',[])
    clearance = max([rules.get('min_clearance', .1)] + [c.get('clearance',.1) for c in classes])
    edge_clearance = rules.get('min_copper_edge_clearance',.3)
    boardpoly = pcb.SHAPE_POLY_SET(); outline_ok = b.GetBoardPolygonOutlines(boardpoly,False)
    outline = polygons(boardpoly) if outline_ok else None
    if outline is not None and not outline.is_valid: outline = outline.buffer(0)
    boundary = outline.buffer(-edge_clearance) if outline is not None else None
    tracks = [t for t in b.GetTracks() if not isinstance(t,pcb.PCB_VIA)]
    lines = [track_line(t) for t in tracks]
    shapes = [g.buffer(t.GetWidth()/2e6,quad_segs=32) for g,t in zip(lines,tracks)]
    widths = [t.GetWidth()/1e6 for t in tracks]
    by_layer = defaultdict(list)
    for i,t in enumerate(tracks): by_layer[t.GetLayer()].append(i)
    adj = [set() for _ in tracks]; events = []
    # Index actual copper, so contacts at segment interiors and offset overlaps
    # are included; endpoint-only counting misses these.
    for layer, ids in by_layer.items():
        tree = STRtree([shapes[i] for i in ids])
        for i in ids:
            for raw in tree.query(shapes[i],predicate='dwithin',distance=EPS):
                k = ids[int(raw)]
                if k <= i or tracks[k].GetNetCode()!=tracks[i].GetNetCode(): continue
                adj[i].add(k); adj[k].add(i)
                if abs(widths[i]-widths[k])<EPS: continue
                shared = set(lines[i].coords) & set(lines[k].coords)
                hit = lines[i].intersection(lines[k])
                if shared: q = Point(sorted(shared)[0]); kind = 'endpoint'
                elif not hit.is_empty: q = hit.representative_point(); kind = 'interior_join'
                else:
                    a,c = nearest_points(lines[i],lines[k]); q = Point((a.x+c.x)/2,(a.y+c.y)/2); kind = 'copper_overlap'
                events.append((i,k,q,kind))
    pads = []; vias = []
    for f in b.GetFootprints():
        for a in f.Pads(): pads.append((f.GetReference()+'.'+a.GetNumber(),a))
    for t in b.GetTracks():
        if isinstance(t,pcb.PCB_VIA): vias.append(t)
    obstacles = {}; terminals = {}
    for layer in by_layer:
        obs=[]; term=[]
        for i in by_layer[layer]: obs.append((tracks[i].GetNetCode(),shapes[i],'track '+uid(tracks[i]),0.0))
        for name,pad in pads:
            if pad.IsOnLayer(layer):
                poly=pcb.SHAPE_POLY_SET();pad.TransformShapeToPolygon(poly,layer,0,1000,pcb.ERROR_OUTSIDE);g=polygons(poly)
                obs.append((pad.GetNetCode(),g,'pad '+name,0.0));term.append((pad.GetNetCode(),g,'pad '+name))
        for via in vias:
            if via.IsOnLayer(layer):
                g=Point(xy(via.GetPosition())).buffer(via.GetWidth(layer)/2e6,quad_segs=32)
                obs.append((via.GetNetCode(),g,'via '+uid(via),0.0));term.append((via.GetNetCode(),g,'via '+uid(via)))
        for z in b.Zones():
            if not z.IsOnLayer(layer): continue
            if z.GetIsRuleArea():
                if z.GetDoNotAllowTracks():obs.append((None,polygons(z.Outline()),'track keepout '+uid(z),0.0))
            else:
                g=polygons(z.GetFilledPolysList(layer))
                if not g.is_empty:obs.append((z.GetNetCode(),g,'zone '+uid(z),0.0))
        obstacles[layer]=(obs,STRtree([o[1] for o in obs]));terminals[layer]=term
    records=[]
    center_trees={layer:STRtree([lines[i] for i in ids]) for layer,ids in by_layer.items()}
    for i,k,q,kind in events:
        small,big=(i,k) if widths[i]<widths[k] else (k,i)
        net=tracks[i].GetNetCode();layer=tracks[i].GetLayer();lo,hi=widths[small],widths[big]
        # Follow constant-width series runs; stop at branches, pads, and vias.
        # Nearby parallel copper must not merge unrelated route sections.
        run={small};todo=[small]
        while todo:
            current=todo.pop()
            for endpoint in [Point(lines[current].coords[0]),Point(lines[current].coords[-1])]:
                if any(n==net and g.distance(endpoint)<EPS for n,g,name in terminals[layer]):continue
                ids=by_layer[layer]
                incident=[ids[int(a)] for a in center_trees[layer].query(endpoint,predicate='dwithin',distance=EPS) if tracks[ids[int(a)]].GetNetCode()==net]
                if len(incident)!=2:continue
                other=next(a for a in incident if a!=current)
                if other not in run and abs(widths[other]-lo)<EPS:run.add(other);todo.append(other)
        runline=unary_union([lines[v] for v in run]); length=sum(lines[v].length for v in run)
        proposal=runline.buffer(hi/2,quad_segs=32); blockers=[];obs,tree=obstacles[layer]
        for oi in tree.query(proposal.buffer(clearance)):
            onet,g,name,_=obs[int(oi)]
            if onet==net:continue
            required=0 if onet is None else clearance
            gap=proposal.distance(g)
            if (onet is None and proposal.intersects(g)) or gap+EPS<required:
                blockers.append({'object':name,'gap_mm':round(gap,6),'required_mm':required})
        if boundary is None: blockers.append({'object':'board outline unavailable'})
        elif not boundary.buffer(EPS).covers(proposal):blockers.append({'object':'board edge / cutout','required_mm':edge_clearance})
        near=[name for n,g,name in terminals[layer] if n==net and g.distance(q)<=.25]
        touching=[v for v in by_layer[layer] if tracks[v].GetNetCode()==net and lines[v].distance(q)<EPS]
        branch=len(touching)>2 or kind=='interior_join'
        zone_conflicts=[o for o in blockers if o['object'].startswith('zone ')]
        blockers=[o for o in blockers if not o['object'].startswith('zone ')]
        if kind=='copper_overlap': category='overlap_topology_review'; action='Inspect the overlapping copper join before editing widths; this is not a simple endpoint transition.'
        elif branch: category='branch_review'; action='Review branch currents and topology; different branch widths can be intentional.'
        elif not blockers: category='widen_run_candidate'; action=f'Widen the entire {length:.3f} mm narrow run to {hi:.3f} mm; then run DRC.'
        elif near: category='terminal_escape_review'; action='Check pad/via escape: keep only the length that needs neck-down; review the listed blockers.'
        else: category='constrained_run_review'; action='Widening is blocked on this path. Reroute or choose one electrically adequate width for the complete run; do not retain isolated wide islands by default.'
        records.append({'net':tracks[i].GetNetname(),'layer':b.GetLayerName(layer),'x_mm':round(q.x-origin[0],6),'y_mm':round(q.y-origin[1],6),'board_x_mm':round(q.x,6),'board_y_mm':round(q.y,6),'narrow_mm':lo,'wide_mm':hi,'contact':kind,'category':category,'narrow_run_length_mm':round(length,6),'narrow_run_tracks':sorted(uid(tracks[v]) for v in run),'tracks':sorted([uid(tracks[i]),uid(tracks[k])]),'near_terminals':near,'widening_blockers':blockers,'zone_refill_conflicts':zone_conflicts,'recommendation':action})
    order={'widen_run_candidate':0,'constrained_run_review':1,'terminal_escape_review':2,'branch_review':3,'overlap_topology_review':4}
    records.sort(key=lambda r:(order[r['category']],r['net'],r['layer'],r['y_mm'],r['x_mm'],r['tracks']))
    for n,r in enumerate(records,1):r['id']=f'W{n:03d}'
    # A bounded constant-width island has a width change at both ends.
    islands=[];seen=set()
    for i in range(len(tracks)):
        if i in seen:continue
        group={i};todo=[i];seen.add(i)
        while todo:
            a=todo.pop()
            for c in adj[a]:
                if c not in seen and abs(widths[c]-widths[i])<EPS:group.add(c);seen.add(c);todo.append(c)
        neighbors={k for a in group for k in adj[a] if k not in group}
        contacts={tuple(round(v,6) for v in nearest_points(lines[a],lines[k])[0].coords[0]) for a in group for k in adj[a] if k not in group}
        if len(contacts)<2 or not neighbors:continue
        lower=all(widths[k]<widths[i]-EPS for k in neighbors);higher=all(widths[k]>widths[i]+EPS for k in neighbors)
        if not(lower or higher):continue
        g=unary_union([shapes[a] for a in group]);n=tracks[i].GetNetCode();ls=tracks[i].GetLayer()
        attached=[name for nn,shape,name in terminals[ls] if nn==n and shape.distance(g)<EPS]
        ids={uid(tracks[a]) for a in group}
        islands.append({'priority':'high' if lower and not attached else 'review','kind':'wide_island' if lower else 'narrow_neck','net':tracks[i].GetNetname(),'layer':b.GetLayerName(ls),'width_mm':widths[i],'length_mm':round(sum(lines[a].length for a in group),6),'tracks':sorted(ids),'attached_terminals':attached,'transition_ids':[r['id'] for r in records if ids.intersection(r['tracks'])],'recommendation':'Review the complete route. This width island is not automatically justified by available space; do not narrow power or controlled-impedance routes without electrical review.'})
    return {'board':str(path),'board_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'coordinate_origin_mm':origin,'clearance_mm':clearance,'edge_clearance_mm':edge_clearance,'summary':dict(Counter(r['category'] for r in records)),'transition_pair_count':len(records),'contact_counts':dict(Counter(r['contact'] for r in records)),'unique_transition_locations':len({(r['net'],r['layer'],r['x_mm'],r['y_mm']) for r in records}),'width_islands':islands,'transitions':records,'limitations':['Read-only geometry triage, not a DRC waiver or electrical approval.','Counts are contacting different-width track pairs; multiple pairs can share a branch location.','Uses the largest configured netclass clearance conservatively; custom .kicad_dru rules require KiCad DRC.','Pad outlines use 1 um polygon approximation; arcs use <=5 um sampling.','Filled foreign zones are reported separately: widening requires refill plus plane-connectivity checks. No impedance/current requirements are inferred.']}

def write_reports(result,out):
    out.mkdir(parents=True,exist_ok=True);(out/'trace-width-audit.json').write_text(json.dumps(result,indent=2)+'\n')
    fields=['id','category','net','layer','x_mm','y_mm','narrow_mm','wide_mm','contact','narrow_run_length_mm','near_terminals','widening_blockers','zone_refill_conflicts','tracks','recommendation']
    with (out/'trace-width-audit.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fields);w.writeheader()
        for r in result['transitions']:w.writerow({k:json.dumps(r[k]) if isinstance(r[k],list) else r[k] for k in fields})
    s=['# Trace-width triage','',f"Board SHA-256: `{result['board_sha256']}`",'',f"**{result['transition_pair_count']} width-changing contacts at {result['unique_transition_locations']} locations.** Coordinates are millimetres relative to the drill/auxiliary origin.",'','## Categories','']
    s.extend(f'- {k}: **{v}**' for k,v in result['summary'].items())
    s+=['','Contact types: '+str(result['contact_counts'])+'. Overlapping-copper pairs are reported separately from centerline width transitions.',
        '', '## First-pass priorities', '',
        '1. Review high-priority wide islands: these have narrower connections and no attached pad or via. Choose a suitable continuous width; do not blindly shrink power traces.',
        '2. Review whole-run widening candidates, then refill zones and run KiCad DRC.',
        '3. Reroute constrained runs before deciding which neck-downs are necessary.',
        '4. Inspect branches and overlap contacts for redundant segments; geometry alone cannot decide the intended topology.',
        '', '## Width islands','',f"Found {len(result['width_islands'])} constant-width runs bounded by narrower or wider copper.",'']
    for a in result['width_islands']:
        s.append(f"- **{a['priority']}** — {a['kind']}: {a['net']} / {a['layer']}, {a['width_mm']:.3f} mm × {a['length_mm']:.3f} mm; contacts {', '.join(a['transition_ids'])}; attached pads/vias: {len(a['attached_terminals'])}.")
    s+=['','## Every transition','']
    for r in result['transitions']:
        s += [f"### {r['id']} — {r['net']} / {r['layer']}",'',f"({r['x_mm']:.4f}, {r['y_mm']:.4f}) mm; **{r['narrow_mm']:.3f} ↔ {r['wide_mm']:.3f} mm**; `{r['category']}` / `{r['contact']}`.",'',r['recommendation'],'']
        if r['widening_blockers']:s+=['Blockers: '+ '; '.join(x['object'] for x in r['widening_blockers'])+'.','']
        if r['zone_refill_conflicts']:s+=['Zone refill required; verify plane continuity after widening.','']
        s+=['Track UUIDs: '+', '.join('`'+t+'`' for t in r['tracks'])+'.','']
    s+=['## Limits','']+['- '+v for v in result['limitations']]
    (out/'trace-width-audit.md').write_text('\n'.join(s)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('board',nargs='?',type=Path,default=Path('boards/esp32-fpga-module/module.kicad_pcb'));parser.add_argument('--out',type=Path,default=Path('boards/esp32-fpga-module/docs/trace-width-audit'));args=parser.parse_args()
    before=hashlib.sha256(args.board.read_bytes()).hexdigest();result=audit(args.board);assert before==hashlib.sha256(args.board.read_bytes()).hexdigest(), 'Board changed while audit was running';write_reports(result,args.out);print(json.dumps({k:result[k] for k in ['transition_pair_count','unique_transition_locations','summary']},indent=2))
