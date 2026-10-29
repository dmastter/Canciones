import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
NAT="CDEFGAB"
bot={'R':('E',4),'T':('E',3),'B':('G',2)}
def pitch(clef,k):
    l,o=bot[clef]; idx=NAT.index(l)+k
    return NAT[idx%7]+str(o+idx//7)
def runs_of(a):
    h,w=a.shape
    out=np.zeros(h,int)
    for y in range(h):
        row=a[y]
        if not row.any(): continue
        d=np.diff(np.concatenate(([0],row.astype(int),[0])))
        s=np.where(d==1)[0]; e=np.where(d==-1)[0]
        out[y]=(e-s).max()
    return out
def staves_in(a,thr=0.6):
    W=a.shape[1]
    runs=runs_of(a)
    rows=np.where(runs>thr*W)[0]
    groups=[];cur=[]
    for r in rows:
        if cur and r-cur[-1]>2: groups.append(cur);cur=[]
        cur.append(r)
    if cur:groups.append(cur)
    cs=[float(np.mean(g)) for g in groups]
    st=[];i=0
    while i+4<len(cs):
        c=cs[i:i+5];g=np.diff(c)
        if g.max()-g.min()<=max(5,0.22*g.mean()) and 10<g.mean()<60:
            st.append(c);i+=5
        else:i+=1
    return st
def sysmodel(path,n,win=140,stride=40):
    im=Image.open(path).convert('L'); a=np.asarray(im)<150
    H,W=a.shape
    data=[[] for _ in range(n)]
    for x in range(0,W-win,stride):
        st=staves_in(a[:,x:x+win])
        if len(st)==n:
            for j,s in enumerate(st): data[j].append((x+win/2,s))
    models=[]
    for j in range(n):
        xs=np.array([d[0] for d in data[j]]); ys=np.array([d[1] for d in data[j]])  # (m,5)
        if len(xs)<3: models.append(None);continue
        coefs=[np.polyfit(xs,ys[:,k],1) for k in range(5)]
        models.append(coefs)
    print(path,'windows ok:',[len(d) for d in data])
    return models
def render(path,models,staffsel,clefs,box,z,out):
    x0,y0,x1,y1=box
    im=Image.open(path).convert('L').crop(box)
    im2=im.convert('RGB').resize((int(im.width*z),int(im.height*z)),Image.LANCZOS)
    d=ImageDraw.Draw(im2); f=ImageFont.truetype('arial.ttf',13)
    for j,cl in zip(staffsel,clefs):
        mdl=models[j]
        if mdl is None: continue
        def lineY(k,x): # k en pasos (0 = línea inferior); y en coords de crop
            ys=[np.polyval(c,x) for c in mdl]   # ys[0] línea superior ... ys[4] inferior
            sp=(ys[4]-ys[0])/4
            return ys[4]-k*sp/2
        xs=np.linspace(x0,x1,12)
        for k in range(-5,14):
            pts=[((x-x0)*z,(lineY(k,x)-y0)*z) for x in xs]
            if k%2==0:
                col=(255,0,0) if 0<=k<=8 else (0,170,0)
                d.line(pts,fill=col,width=1)
            else:
                for (a1,b1),(a2,b2) in zip(pts[:-1],pts[1:]):
                    n=int((a2-a1)/10)
                    for t in range(n):
                        u=t/n; v=(t+0.4)/n
                        d.line([(a1+(a2-a1)*u,b1+(b2-b1)*u),(a1+(a2-a1)*v,b1+(b2-b1)*v)],fill=(0,80,255),width=1)
            d.text((2,pts[0][1]-8),pitch(cl,k),fill=(160,0,160),font=f)
            d.text((im2.width-32,pts[-1][1]-8),pitch(cl,k),fill=(160,0,160),font=f)
    im2.save(out)
if __name__=='__main__':
    sysn=sys.argv[1]; nst=int(sys.argv[2]); layout=sys.argv[3]   # layout: 'TBRB' etc
    vy0,vy1,py0,py1=map(int,sys.argv[4:8]); z=float(sys.argv[8]) if len(sys.argv)>8 else 2.0
    path=f'crops/{sysn}.png'
    models=sysmodel(path,nst)
    W=Image.open(path).width
    wins=[(0,700),(600,1300),(1200,1900),(1800,W)]
    for i,(a,b) in enumerate(wins):
        if nst==4:
            render(path,models,[0,1],layout[:2],(a,vy0,b,vy1),z,f'w/{sysn}_v{i}.png')
            render(path,models,[2,3],layout[2:],(a,py0,b,py1),z,f'w/{sysn}_p{i}.png')
        else:
            render(path,models,[0,1],layout,(a,py0,b,py1),z,f'w/{sysn}_p{i}.png')
