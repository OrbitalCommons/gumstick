import numpy as np
from shapely import contains_xy
from shapely.geometry import box,LineString
import heapq

def local_search(old,radius,pads,foreign,holes,active,anchors,trees,layers,softforeign):
 step=.025;n=241;half=n//2;xx,yy=np.meshgrid(old[0]+(np.arange(n)-half)*step,old[1]+(np.arange(n)-half)*step)
 area=box(xx.min()-.5,yy.min()-.5,xx.max()+.5,yy.max()+.5)
 def raster(shapes,buf):
  mask=np.zeros((n,n),bool)
  for g in shapes:
   if not g.intersects(area):continue
   shape=g.buffer(buf);x0,y0,x1,y1=shape.bounds
   a=max(0,int((x0-xx[0,0])/step)-1);c=min(n,int((x1-xx[0,0])/step)+2);z=max(0,int((y0-yy[0,0])/step)-1);e=min(n,int((y1-yy[0,0])/step)+2)
   if a<c and z<e:mask[z:e,a:c]|=contains_xy(shape,xx[z:e,a:c],yy[z:e,a:c])
  return mask
 valid=~raster([g for _,g,_,_ in pads],radius+.0751)
 valid&=~raster(holes,0)
 for l in layers:valid&=~raster(foreign[l],radius+.1001)
 valid&=(xx>100.3+radius)&(xx<119.7-radius)&(yy>107.7+radius)&(yy<145.3-radius)&((xx-110)**2+(yy-128.25)**2>(3.5+radius)**2)
 score=np.zeros((n,n),np.int32);preds={}
 for l in active:
  mask=raster(foreign[l],.1502);mask|=(xx<100.35)|(xx>119.65)|(yy<107.75)|(yy>145.25)|((xx-110)**2+(yy-128.25)**2<3.55**2)
  cost=1+30*raster(softforeign[l],.1502).astype(np.int32)
  dist=np.full((n,n),100000000,np.int32);prev=np.full((n,n),-1,np.int32);dist[half,half]=0;todo=[(0,half,half)]
  while todo:
   dd,y,x=heapq.heappop(todo)
   if dd!=dist[y,x]:continue
   for dy,dx in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
    a=x+dx;z=y+dy
    if not(0<=a<n and 0<=z<n) or mask[z,a]:continue
    if dx and dy and (mask[y,a] or mask[z,x]):continue
    nd=dd+int(cost[z,a])
    if nd>=dist[z,a]:continue
    dist[z,a]=nd;prev[z,a]=y*n+x;heapq.heappush(todo,(nd,z,a))
  valid&=dist<100000000;score+=dist;preds[l]=prev
 ids=np.flatnonzero(valid)
 if not len(ids):return None
 ids=ids[np.argsort(score.reshape(-1)[ids])]
 for idx in ids[:100]:
  y,x=divmod(int(idx),n);dest=(float(xx[y,x]),float(yy[y,x]));routes=[];ok=True
  for l in active:
   path=[dest];cur=int(idx)
   while cur!=half*n+half:
    cy,cx=divmod(cur,n);cur=int(preds[l][cy,cx]);cy,cx=divmod(cur,n);path.append((float(xx[cy,cx]),float(yy[cy,cx])))
   # Exact geometry validation remains authoritative for diagonal transitions.
   for a,z in zip(path,path[1:]):
    if len(trees[l].query(LineString([a,z]).buffer(.1501),predicate='intersects')):ok=False;break
    routes.append((l,a,z))
   for a in anchors[l]:
    if a!=old:routes.append((l,a,old))
   if not ok:break
  if ok:return dest,routes
 return None
