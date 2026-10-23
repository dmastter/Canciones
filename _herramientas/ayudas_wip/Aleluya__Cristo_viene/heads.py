import sys, numpy as np, cv2
from scipy import ndimage as ndi
from PIL import Image, ImageDraw, ImageFont
SC={"T":["A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4","F4","G4","A4","B4","C5","D5"],
    "B":["C2","D2","E2","F2","G2","A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4","F4"]}
def clusters(rows):
    g=[];cur=[]
    for r in rows:
        if cur and r-cur[-1]>2: g.append(cur);cur=[]
        cur.append(r)
    if cur:g.append(cur)
    return [sum(c)/len(c) for c in g]
f,clefs,x0,x1,zoom=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),float(sys.argv[5])
ylo=int(sys.argv[6]); yhi=int(sys.argv[7]); tag=sys.argv[8] if len(sys.argv)>8 else 'h'
si=int(sys.argv[9]) if len(sys.argv)>9 else 0   # índice del pentagrama (para las líneas) -> se anota el pentagrama del rango
im=Image.open(f).convert("L"); g=np.asarray(im); B=(g<150).astype(np.uint8)
H,W=B.shape; n=len(clefs)
wins=[]
for xc in range(120,min(W-100,2400),30):
    fr=B[:,xc-50:xc+50].mean(axis=1); wins.append((xc,clusters(np.where(fr>0.6)[0])))
good=[(xc,cs) for xc,cs in wins if len(cs)==5*n]
ref=np.array([c for _,c in good]); xs=np.array([x for x,_ in good])
def line(i,x): return float(np.interp(x,xs,ref[:,i]))
sp=float(np.mean(ref[:,1]-ref[:,0]))
# quitar pentagrama
lines=cv2.morphologyEx(B,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_RECT,(int(sp*3),1)))
mask=np.zeros_like(B)
for x in range(W):
    for i in range(5*n):
        y=int(round(line(i,x)))
        mask[max(0,y-4):y+5,x]=1
lines=lines&mask
B2=B.copy(); B2[lines>0]=0
B2=cv2.morphologyEx(B2,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_RECT,(1,int(sp*0.55))))
inv=(B2==0).astype(np.uint8)
nn,ll,ss,_=cv2.connectedComponentsWithStats(inv,connectivity=4)
Bf=B2.copy()
for i in range(1,nn):
    if ss[i,4]<sp*sp*0.9: Bf[ll==i]=1
k=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(sp*0.85),int(sp*0.7)))
O=cv2.morphologyEx(Bf,cv2.MORPH_OPEN,k)
num,lab,stats,cent=cv2.connectedComponentsWithStats(O)
rgb=im.convert("RGB").crop((x0,ylo,x1,yhi)); rgb=rgb.resize((int(rgb.width*zoom),int(rgb.height*zoom)),Image.LANCZOS)
d=ImageDraw.Draw(rgb); fnt=ImageFont.truetype("arial.ttf",15)
res=[]
for s_ in range(n):
    for st in range(-5,12):
        col=(255,150,150) if st%2==0 and 0<=st<=8 else ((0,170,0) if st%2==0 else (170,200,255))
        pl=[]
        for x in range(x0,x1+1,10):
            bt=line(s_*5+4,x); sq=(bt-line(s_*5,x))/4
            pl.append(((x-x0)*zoom,(bt-st*sq/2-ylo)*zoom))
        d.line(pl,fill=col,width=1)
    for xx in range(x0+6,x1,100):
        bt=line(s_*5+4,xx); sq=(bt-line(s_*5,xx))/4
        for st in range(-4,11,2):
            idx=4+st
            if 0<=idx<len(SC[clefs[s_]]): d.text(((xx-x0)*zoom,(bt-st*sq/2-ylo)*zoom-14),SC[clefs[s_]][idx],fill=(0,120,0),font=fnt)
for i in range(1,num):
    x,y,w,h,a=stats[i]
    if not(x0<=x+w/2<x1) or not(ylo<=y+h/2<yhi) or a<sp*sp*0.4: continue
    cx=x+w/2
    # pentagrama más cercano
    best=None
    for s in range(n):
        mid=(line(s*5,cx)+line(s*5+4,cx))/2
        if best is None or abs(mid-(y+h/2))<best[0]: best=(abs(mid-(y+h/2)),s)
    s=best[1]; bot=line(s*5+4,cx); spl=(bot-line(s*5,cx))/4
    def pit(yc):
        stf=(bot-yc)/(spl/2); st=round(stf); idx=4+st
        FR.append(round(stf,2))
        return (SC[clefs[s]][idx] if 0<=idx<len(SC[clefs[s]]) else '?'),st
    nh=1
    labs=[]
    FR=[]
    if h>spl*1.25:
        nh=2
        labs=[pit(y+spl/2),pit(y+h-spl/2)]
        if h>spl*2.4:
            labs=[pit(y+spl/2),pit(y+h/2),pit(y+h-spl/2)]
    else:
        labs=[pit(y+h/2)]
    res.append((s,round(cx),[l[0] for l in labs],FR,round(h/spl,2)))
    X0=(x-x0)*zoom; Y0=(y-ylo)*zoom
    d.rectangle([X0,Y0,X0+w*zoom,Y0+h*zoom],outline=(255,0,0),width=2)
    d.text((X0,Y0-17),"/".join(l[0] for l in labs),fill=(220,0,220),font=fnt)
out=f.replace(".png",f"_{tag}{x0}.png"); rgb.save(out); print(out)
for r in sorted(res,key=lambda r:(r[1],r[0])): print(r)
