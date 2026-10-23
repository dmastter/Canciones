import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
# uso: lc.py crop x0 y0 x1 y1 zoom clefs out    (clefs: R=treble real, T=tenor 8vb real, B=bass; uno por pentagrama de arriba abajo)
p,x0,y0,x1,y1,z,clefs,out=sys.argv[1:9]
x0,y0,x1,y1=map(int,(x0,y0,x1,y1)); z=float(z)
im=Image.open(p).convert('L').crop((x0,y0,x1,y1))
a=np.asarray(im)<150
W=a.shape[1]
def longest(row):
    m=0;c=0
    for v in row:
        if v:
            c+=1
            if c>m:m=c
        else:c=0
    return m
runs=np.array([longest(r) for r in a])
rows=np.where(runs>0.55*W)[0]
groups=[];cur=[]
for r in rows:
    if cur and r-cur[-1]>2: groups.append(cur);cur=[]
    cur.append(r)
if cur:groups.append(cur)
cs=[np.mean(g) for g in groups]
staves=[];i=0
while i+4<len(cs):
    c=cs[i:i+5];g=np.diff(c)
    if g.max()-g.min()<=max(4,0.2*g.mean()) and 8<g.mean()<60:
        staves.append(c);i+=5
    else:i+=1
print('staves',len(staves),[ [round(float(x),1) for x in s] for s in staves])
NAT="CDEFGAB"
def names(base_letter_idx,base_oct):  # nombre de la línea inferior
    res={}
    return res
# línea inferior: R=E4, T=E3, B=G2
bot={'R':('E',4),'T':('E',3),'B':('G',2)}
def pitch(clef,k): # k pasos diatónicos sobre la línea inferior
    l,o=bot[clef]; idx=NAT.index(l)+k
    return NAT[idx%7]+str(o+idx//7)
im2=im.convert('RGB').resize((int(im.width*z),int(im.height*z)),Image.LANCZOS)
d=ImageDraw.Draw(im2)
try: f=ImageFont.truetype('arial.ttf',14)
except: f=ImageFont.load_default()
for st,cl in zip(staves,clefs):
    sp=(st[4]-st[0])/4
    for k in range(-5,14):
        y=(st[4]-k*sp/2)*z
        if k%2==0:
            col=(255,0,0) if 0<=k<=8 else (0,160,0)
            d.line([(0,y),(im2.width,y)],fill=col,width=1)
        else:
            for xx in range(0,im2.width,10): d.line([(xx,y),(xx+4,y)],fill=(0,80,255),width=1)
        d.text((2,y-8),pitch(cl,k),fill=(160,0,160),font=f)
        d.text((im2.width-30,y-8),pitch(cl,k),fill=(160,0,160),font=f)
im2.save(out)
