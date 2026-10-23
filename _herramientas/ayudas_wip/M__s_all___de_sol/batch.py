import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
NAT="CDEFGAB"
bot={'R':('E',4),'T':('E',3),'B':('G',2)}
def pitch(clef,k):
    l,o=bot[clef]; idx=NAT.index(l)+k
    return NAT[idx%7]+str(o+idx//7)
def runs_of(a):
    # longest horizontal run per row, vectorized-ish
    h,w=a.shape
    out=np.zeros(h,int)
    for y in range(h):
        row=a[y]
        if not row.any(): continue
        d=np.diff(np.concatenate(([0],row.astype(int),[0])))
        s=np.where(d==1)[0]; e=np.where(d==-1)[0]
        out[y]=(e-s).max()
    return out
def find_staves(a):
    W=a.shape[1]
    runs=runs_of(a)
    for thr in (0.55,0.45,0.35,0.28):
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
            if g.max()-g.min()<=max(5,0.25*g.mean()) and 8<g.mean()<60:
                st.append(c);i+=5
            else:i+=1
        if st: return st
    return []
def render(path,box,z,clefs,out):
    x0,y0,x1,y1=box
    im=Image.open(path).convert('L').crop(box)
    a=np.asarray(im)<150
    staves=find_staves(a)
    im2=im.convert('RGB').resize((int(im.width*z),int(im.height*z)),Image.LANCZOS)
    d=ImageDraw.Draw(im2)
    f=ImageFont.truetype('arial.ttf',13)
    ok=len(staves)==len(clefs)
    if ok:
        for st,cl in zip(staves,clefs):
            sp=(st[4]-st[0])/4
            for k in range(-5,14):
                y=(st[4]-k*sp/2)*z
                if k%2==0:
                    col=(255,0,0) if 0<=k<=8 else (0,170,0)
                    d.line([(0,y),(im2.width,y)],fill=col,width=1)
                else:
                    for xx in range(0,im2.width,10): d.line([(xx,y),(xx+4,y)],fill=(0,80,255),width=1)
                d.text((2,y-8),pitch(cl,k),fill=(160,0,160),font=f)
                d.text((im2.width-32,y-8),pitch(cl,k),fill=(160,0,160),font=f)
    im2.save(out)
    return len(staves)
if __name__=='__main__':
    sysn=sys.argv[1]; vy0,vy1,py0,py1=map(int,sys.argv[2:6]); z=float(sys.argv[6]) if len(sys.argv)>6 else 2.0
    path=f'crops/{sysn}.png'
    W=Image.open(path).width
    wins=[(0,700),(600,1300),(1200,1900),(1800,W)]
    for i,(a,b) in enumerate(wins):
        n=render(path,(a,vy0,b,vy1),z,'TB',f'w/{sysn}_v{i}.png')
        m=render(path,(a,py0,b,py1),z,'RB',f'w/{sysn}_p{i}.png')
        print(sysn,i,'voc staves',n,'pno staves',m)
