import sys, numpy as np
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
# uso: bar.py d/p1_sN.png claves xa xb zoom tag [up] [down]
f,clefs,xa,xb,zoom,tag=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),float(sys.argv[5]),sys.argv[6]
im=Image.open(f).convert("L"); a=np.asarray(im)<150
H,W=a.shape; n=len(clefs)
wins=[]
for xc in range(120,min(W-100,2400),30):
    fr=a[:,xc-50:xc+50].mean(axis=1); wins.append((xc,clusters(np.where(fr>0.6)[0])))
good=[(xc,cs) for xc,cs in wins if len(cs)==5*n]
ref=np.array([c for _,c in good]); xs=np.array([x for x,_ in good])
def line(i,x): return float(np.interp(x,xs,ref[:,i]))
fnt=ImageFont.truetype("arial.ttf",13)
bands=[]
for s,cl in enumerate(clefs):
    xm=(xa+xb)//2
    top=line(s*5,xm); bot=line(s*5+4,xm); spl=(bot-top)/4
    ylo=int(top-spl*3.2); yhi=int(bot+spl*3.6)
    c=im.convert("RGB").crop((xa,ylo,xb,yhi)); c=c.resize((int(c.width*zoom),int(c.height*zoom)),Image.LANCZOS)
    d=ImageDraw.Draw(c)
    for st in range(-7,13):
        col=(255,60,60) if st%2==0 and 0<=st<=8 else ((0,170,0) if st%2==0 else (150,185,255))
        pl=[]
        for x in range(xa,xb+1,10):
            bt=line(s*5+4,x); sq=(bt-line(s*5,x))/4
            pl.append(((x-xa)*zoom,(bt-st*sq/2-ylo)*zoom))
        d.line(pl,fill=col,width=1)
    for xx in (xa+4,xb-40):
        bt=line(s*5+4,xx); sq=(bt-line(s*5,xx))/4
        for st in range(-6,12):
            idx=4+st
            if 0<=idx<len(SC[cl]):
                d.text(((xx-xa)*zoom,(bt-st*sq/2-ylo)*zoom-7),SC[cl][idx],fill=(190,0,190),font=fnt)
    bands.append(c)
Wd=bands[0].width; Ht=sum(b.height for b in bands)+6*(len(bands)-1)
out=Image.new("RGB",(Wd,Ht),(255,255,0)); y=0
for b in bands: out.paste(b,(0,y)); y+=b.height+6
o=f.replace(".png",f"_b{tag}.png"); out.save(o); print(o,out.size)
