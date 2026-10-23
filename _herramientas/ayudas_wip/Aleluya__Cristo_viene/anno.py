import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
SC={"T":["A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4","F4","G4","A4","B4","C5","D5"],
    "G":["A3","B3","C4","D4","E4","F4","G4","A4","B4","C5","D5","E5","F5","G5","A5","B5","C6","D6"],
    "B":["C2","D2","E2","F2","G2","A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4","F4"]}
def clusters(rows):
    g=[];cur=[]
    for r in rows:
        if cur and r-cur[-1]>2: g.append(cur);cur=[]
        cur.append(r)
    if cur:g.append(cur)
    return [sum(c)/len(c) for c in g]
f,clefs,x0,x1,zoom=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),float(sys.argv[5])
ylo=int(sys.argv[6]) if len(sys.argv)>6 else 0; yhi=int(sys.argv[7]) if len(sys.argv)>7 else None; tag=sys.argv[8] if len(sys.argv)>8 else ''
im=Image.open(f).convert("L"); a=np.asarray(im)<150
H,W=a.shape; n=len(clefs)
wins=[]
for xc in range(120,min(W-100,2400),30):
    fr=a[:,xc-50:xc+50].mean(axis=1)
    wins.append((xc,clusters(np.where(fr>0.6)[0])))
good=[(xc,cs) for xc,cs in wins if len(cs)==5*n]
if not good: print("sin ventanas buenas",[len(c) for _,c in wins]); sys.exit()
ref=np.array([c for _,c in good]); xs=np.array([x for x,_ in good])
def line(i,x): return float(np.interp(x,xs,ref[:,i]))
yhi=yhi or H
c=im.convert("RGB").crop((x0,ylo,x1,yhi)); c=c.resize((int(c.width*zoom),int(c.height*zoom)),Image.LANCZOS)
d=ImageDraw.Draw(c)
fnt=ImageFont.truetype("arial.ttf",13)
for s,cl in enumerate(clefs):
    for st in range(-6,13):
        col=(255,0,0) if st%2==0 and 0<=st<=8 else ((0,170,0) if st%2==0 else (120,170,255))
        pl=[]
        for x in range(x0,x1+1,10):
            bot=line(s*5+4,x)
            sp=(line(s*5+4,x)-line(s*5,x))/4
            pl.append(((x-x0)*zoom,(bot-st*sp/2-ylo)*zoom))
        d.line(pl,fill=col,width=1)
    for xx in range(x0+10,x1,90):
        bot=line(s*5+4,xx); sp=(bot-line(s*5,xx))/4
        for st in range(-5,12):
            idx=4+st
            if 0<=idx<len(SC[cl]) and st%2==0:
                d.text(((xx-x0)*zoom,(bot-st*sp/2-ylo)*zoom-14),SC[cl][idx],fill=(200,0,200),font=fnt)
out=f.replace(".png",f"_a{x0}{tag}.png"); c.save(out); print(out)
