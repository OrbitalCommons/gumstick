// Clearance-constrained fanout and low-speed routing assistant. Critical nets are pre-routed.
#include <bits/stdc++.h>
using namespace std;
struct P{int x,y,z;};struct Net{int id,mode,priority;vector<P> p;};
int W,H,L,N;vector<int16_t>A,V;vector<uint8_t>K;vector<float> distv;vector<int> par,seen;int gen=0;ofstream out;
int idx(P p){return p.z*N+p.y*W+p.x;}P point(int i){return {i%W,(i%N)/W,i/N};}
bool ok(int16_t a,int net){return a==0||a==net;}
bool viaok(P p,int net){int i=p.y*W+p.x;if(K[i]||!ok(V[i],net))return false;for(int z=0;z<L;z++)if(!ok(A[z*N+i],net))return false;return true;}
void paint(int16_t& a,int net){if(a==0)a=net;else if(a!=net)a=-1;}
void disk(P p,double radius,int net,bool via){int R=ceil(radius);for(int dy=-R;dy<=R;dy++)for(int dx=-R;dx<=R;dx++){if(dx*dx+dy*dy>radius*radius)continue;int x=p.x+dx,y=p.y+dy;if(x<0||y<0||x>=W||y>=H)continue;int i=y*W+x;if(via){for(int z=0;z<L;z++)paint(A[z*N+i],net);}else paint(A[p.z*N+i],net);}}
void vdisk(P p,double radius,int net){int R=ceil(radius);for(int dy=-R;dy<=R;dy++)for(int dx=-R;dx<=R;dx++){if(dx*dx+dy*dy>radius*radius)continue;int x=p.x+dx,y=p.y+dy;if(x>=0&&y>=0&&x<W&&y<H)paint(V[y*W+x],net);}}
float heur(P a,P b){int dx=abs(a.x-b.x),dy=abs(a.y-b.y);return max(dx,dy)+.414214f*min(dx,dy);}
vector<P> search(P start,P target,int net,bool fan){
 gen++;using Q=tuple<float,float,int>;priority_queue<Q,vector<Q>,greater<Q>>q;int si=idx(start);seen[si]=gen;distv[si]=0;par[si]=-1;q.push({fan?0:heur(start,target),0,si});int expansions=0;
 while(!q.empty()){
  auto [f,g,i]=q.top();q.pop();if(distv[i]!=g)continue;P p=point(i);
  if((fan&&viaok(p,net))||(!fan&&i==idx(target))){vector<P>path;for(int j=i;j!=-1;j=par[j])path.push_back(point(j));reverse(path.begin(),path.end());return path;}
  if(++expansions>1200000)break;
  for(int d=0;d<10;d++){
   P v=p;float cost=1;static int dx[]={1,0,-1,0,1,-1,-1,1},dy[]={0,1,0,-1,1,1,-1,-1};
   if(d<8){v.x+=dx[d];v.y+=dy[d];if(v.x<1||v.x>=W-1||v.y<1||v.y>=H-1)continue;if(!ok(A[idx(v)],net))continue;
    if(d>=4){if(!ok(A[idx({v.x,p.y,p.z})],net)||!ok(A[idx({p.x,v.y,p.z})],net))continue;cost=1.414214f;}
    if(p.z==1)cost*=1.25f;
    if(fan&&heur(v,start)>110)continue;
   }else{if(fan||!viaok(p,net))continue;v.z=(p.z+d-7)%3;cost=85;}
   int j=idx(v);float ng=g+cost;if(seen[j]!=gen||ng<distv[j]){seen[j]=gen;distv[j]=ng;par[j]=i;q.push({ng+(fan?0:heur(v,target)),ng,j});}
  }
 }
 cerr<<"SEARCHBLOCK net="<<net<<" start="<<start.x<<","<<start.y<<","<<start.z<<" target="<<target.x<<","<<target.y<<","<<target.z<<" exp="<<expansions<<" A="<<A[idx(start)]<<","<<A[idx(target)]<<" V="<<V[start.y*W+start.x]<<","<<V[target.y*W+target.x]<<" viaok="<<viaok(target,net)<<" K="<<int(K[target.y*W+target.x])<<" layers="<<A[target.y*W+target.x]<<","<<A[N+target.y*W+target.x]<<","<<A[2*N+target.y*W+target.x]<<endl;
 return {};
}
void emit(vector<P> path,int net,bool fan){
 if(path.empty())return;
 for(auto p:path){disk(p,4.7,net,false);vdisk(p,7.7,net);}
 for(int j=1;j<(int)path.size();j++)if(path[j].z!=path[j-1].z){P p=path[j];out<<"V "<<net<<" "<<p.x<<" "<<p.y<<"\n";disk(p,7.7,net,true);vdisk(p,16.0,net);}
 if(fan){P p=path.back();out<<"V "<<net<<" "<<p.x<<" "<<p.y<<"\n";disk(p,7.7,net,true);vdisk(p,16.0,net);}
 int s=0;
 for(int j=1;j<(int)path.size();j++){
  bool end=j+1==(int)path.size()||path[j+1].z!=path[j].z||path[j].z!=path[j-1].z||(path[j].x-path[j-1].x)!=(path[j+1].x-path[j].x)||(path[j].y-path[j-1].y)!=(path[j+1].y-path[j].y);
  if(path[j].z!=path[j-1].z){s=j;continue;}
  if(end){auto a=path[s],b=path[j];if(a.x!=b.x||a.y!=b.y)out<<"T "<<net<<" "<<a.z<<" "<<a.x<<" "<<a.y<<" "<<b.x<<" "<<b.y<<"\n";s=j;}
 }
}
int main(int argc,char**argv){
 string dir=argc>1?argv[1]:"tmp/module-layout";ifstream f(dir+"/grid.bin",ios::binary);int h[3];f.read((char*)h,12);W=h[0];H=h[1];L=h[2];N=W*H;A.resize(N*L);V.resize(N);K.resize(N);f.read((char*)A.data(),A.size()*2);f.read((char*)V.data(),V.size()*2);f.read((char*)K.data(),K.size());distv.resize(N*L);par.resize(N*L);seen.resize(N*L);
 ifstream nf(dir+"/nets.txt");vector<Net>nets;Net n;int count;while(nf>>n.id>>n.mode>>n.priority>>count){n.p.clear();for(int j=0;j<count;j++){P p;nf>>p.x>>p.y>>p.z;n.p.push_back(p);}nets.push_back(n);}
 stable_sort(nets.begin(),nets.end(),[](const Net&a,const Net&b){int aa=a.mode?10:a.priority,bb=b.mode?10:b.priority;return aa<bb;});out.open(dir+"/routes.txt");int fails=0,done=0;
 // Fan out all terminals before drawing long connections across escape corridors.
 for(auto& n:nets){
  for(P& p:n.p){auto path=search(p,p,n.id,true);if(path.empty()){cerr<<"FAN pending "<<n.id<<" "<<p.x<<" "<<p.y<<endl;if(n.mode)fails++;}else{emit(path,n.id,true);p=path.back();if(n.mode)done++;}}
 }
 out.flush();ifstream ff(dir+"/routes.txt");string prefix((istreambuf_iterator<char>(ff)),{});ff.close();
 auto baseA=A,baseV=V;int baseDone=done,baseFails=fails,best=100000;vector<int>weight(1000);string bestText;mt19937 rng(7624);
 for(int round=0;round<16;round++){
  A=baseA;V=baseV;done=baseDone;fails=baseFails;out.close();out.open(dir+"/routes.txt");out<<prefix;
  vector<Net*>order;for(auto& n:nets)if(!n.mode)order.push_back(&n);if(round)shuffle(order.begin(),order.end(),rng);
  stable_sort(order.begin(),order.end(),[&](Net*a,Net*b){return (a->priority*.2-weight[a->id])<(b->priority*.2-weight[b->id]);});
  vector<int>bad;
  for(auto ptr:order){auto& n=*ptr;
   vector<bool>connected(n.p.size());connected[0]=true;
   for(size_t step=1;step<n.p.size();step++){float best=1e9;int a=-1,b=-1;for(int i=0;i<(int)n.p.size();i++)if(!connected[i])for(int j=0;j<(int)n.p.size();j++)if(connected[j]){float d=heur(n.p[i],n.p[j]);if(d<best){best=d;a=i;b=j;}}auto path=search(n.p[a],n.p[b],n.id,false);connected[a]=true;if(path.empty()){bad.push_back(n.id);fails++;}else{emit(path,n.id,false);done++;}}
  }
  out.flush();cout<<"ROUND "<<round<<" DONE "<<done<<" FAIL "<<fails<<endl;
  if(fails<best){best=fails;ifstream rf(dir+"/routes.txt");bestText.assign((istreambuf_iterator<char>(rf)),{});ofstream report(dir+"/failed-nets.txt");for(int n:bad)report<<n<<"\n";}
  if(fails==baseFails)break;
  for(int n:bad)weight[n]++;
 }
 out.close();out.open(dir+"/routes.txt");out<<bestText;fails=best;
 cout<<"DONE "<<done<<" FAIL "<<fails<<endl;return fails?1:0;
}
