import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'C:/Users/ESB0001672/Canciones_work')
from guide import SCALE
def find(im):
    a=(np.asarray(im.convert('L'))<140)
    best=None
    for ang in np.arange(-2,2.01,0.1):
        r=Image.fromarray((a*255).astype('uint8')).rotate(ang,resample=Image.BILINEAR)
        p=(np.asarray(r)>100).sum(axis=1).astype(float)
        s=(p**2).sum()
        if best is None or s>best[0]: best=(s,ang,p)
    return best
def run(path,clefs,x0,x1,zoom,out,y0=0,y1=None):
    im=Image.open(path).convert('RGB')
    y1=y1 or im.height
    im=im.crop((x0,y0,x1,y1))
    s,ang,p=find(im)
    im=im.rotate(ang,resample=Image.BICUBIC,fillcolor=(255,255,255))
    s,_,p=find(im)  # recompute at ang~0
    a=(np.asarray(im.convert('L'))<140)
    p=a.sum(axis=1).astype(float)
    thr=p.max()*0.45
    rows=np.where(p>thr)[0]
    groups=[];cur=[]
    for r in rows:
        if cur and r-cur[-1]>2: groups.append(cur);cur=[]
        cur.append(r)
    if cur: groups.append(cur)
    cen=[sum(g)/len(g) for g in groups]
    staves=[];i=0
    while i+4<len(cen):
        c=cen[i:i+5];g=np.diff(c)
        if g.max()-g.min()<5 and 6<g.mean()<70: staves.append(c);i+=5
        else: i+=1
    print('angle',ang,'staves',len(staves),'expected',len(clefs))
    d=ImageDraw.Draw(im)
    W=im.width
    font=ImageFont.truetype('arial.ttf',13)
    for st,cl in zip(staves,clefs):
        sp=(st[4]-st[0])/4;names=SCALE[cl]
        for k in range(-4,13):
            y=st[4]-k*sp/2
            name=names[4+k] if 0<=4+k<len(names) else '?'
            if k%2==0:
                col=(220,0,0) if 0<=k<=8 else (0,150,0)
                d.line([(0,y),(W,y)],fill=col,width=1)
            else:
                for x in range(0,W,12): d.line([(x,y),(x+5,y)],fill=(0,90,220),width=1)
            for x in range(2,W,300): d.text((x,y-7),name,fill=(120,0,120),font=font)
    im=im.resize((int(im.width*zoom),int(im.height*zoom)),Image.LANCZOS)
    im.save(out)
if __name__=='__main__':
    a=sys.argv
    run(a[1],a[2],int(a[3]),int(a[4]),float(a[5]),a[6],int(a[7]) if len(a)>7 else 0,int(a[8]) if len(a)>8 else None)
