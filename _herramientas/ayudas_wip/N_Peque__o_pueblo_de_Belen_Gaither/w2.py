import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'C:/Users/ESB0001672/Canciones_work')
from guide import SCALE
font=ImageFont.truetype('arial.ttf',14)
def best_angle(a):
    best=None
    for ang in np.arange(-3,3.01,0.1):
        r=np.asarray(Image.fromarray((a*255).astype('uint8')).rotate(ang,resample=Image.BILINEAR,fillcolor=0))>100
        p=r.sum(axis=1).astype(float)
        s=(p**2).sum()
        if best is None or s>best[0]: best=(s,ang)
    return best[1]
def groups(p,thr):
    rows=np.where(p>thr)[0];g=[];cur=[]
    for x in rows:
        if cur and x-cur[-1]>2: g.append(cur);cur=[]
        cur.append(x)
    if cur: g.append(cur)
    return [sum(c)/len(c) for c in g]
def staves_in(p,thr):
    cen=groups(p,thr);st=[];i=0
    while i+4<len(cen):
        c=cen[i:i+5];g=np.diff(c)
        if g.max()-g.min()<4 and 8<g.mean()<60: st.append(c);i+=5
        else: i+=1
    return st
def main(page,y0,y1,x0,x1,clefs,win,zoom,outp,ang=None,xs=None):
    im=Image.open(page).convert('RGB').crop((x0,y0,x1,y1))
    a=np.asarray(im.convert('L'))<140
    if ang is None: ang=best_angle(a[:,150:-50] if a.shape[1]>400 else a)
    im=im.rotate(ang,resample=Image.BICUBIC,fillcolor=(255,255,255))
    a=np.asarray(im.convert('L'))<140
    print('ang',ang,'size',im.size)
    W=im.width;n=0
    x=0
    while x<W:
        xe=min(W,x+win)
        sub=a[:,x:xe]
        p=sub.sum(axis=1).astype(float)
        thr=max(p.max()*0.5,0.35*(xe-x))
        st=staves_in(p,thr)
        w=im.crop((x,0,xe,im.height)).copy()
        d=ImageDraw.Draw(w)
        if len(st)!=len(clefs): print('window',x,'staves',len(st),'expected',len(clefs))
        for s,cl in zip(st,clefs):
            sp=(s[4]-s[0])/4;names=SCALE[cl]
            for k in range(-4,13):
                y=s[4]-k*sp/2
                nm=names[4+k] if 0<=4+k<len(names) else '?'
                if k%2==0:
                    d.line([(0,y),(w.width,y)],fill=(220,0,0) if 0<=k<=8 else (0,150,0),width=1)
                else:
                    for xx in range(0,w.width,10): d.line([(xx,y),(xx+4,y)],fill=(0,90,220),width=1)
                for xx in range(2,w.width,200): d.text((xx,y-7),nm,fill=(120,0,120),font=font)
        w=w.resize((int(w.width*zoom),int(w.height*zoom)),Image.LANCZOS)
        w.save(f'{outp}_{n}.png');print(f'{outp}_{n}.png x{x}-{xe}')
        n+=1
        if xe>=W: break
        x+=win-100
if __name__=='__main__':
    a=sys.argv
    main(a[1],int(a[2]),int(a[3]),int(a[4]),int(a[5]),a[6],int(a[7]),float(a[8]),a[9])
