import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
T=["A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4","F4","G4","A4","B4","C5"]
B=["C2","D2","E2","F2","G2","A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4"]
def lines(a, thr):
    fr=a.mean(axis=1); rows=np.where(fr>thr)[0]; g=[];c=[]
    for r in rows:
        if c and r-c[-1]>2: g.append(c);c=[]
        c.append(r)
    if c:g.append(c)
    return [sum(x)/len(x) for x in g]
def find5(cs):
    out=[];i=0
    while i+4<len(cs):
        c=cs[i:i+5];d=np.diff(c)
        if d.max()-d.min()<5 and 12<d.mean()<30: out.append(c);i+=5
        else:i+=1
    return out
p,x0,x1,z=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),float(sys.argv[4])
clefs=sys.argv[5] if len(sys.argv)>5 else "TB"
im=Image.open(p).convert("RGB").crop((x0,0,x1,Image.open(p).height))
a=np.asarray(im.convert("L"))<140
st=[]
for thr in (0.5,0.4,0.3,0.22,0.15):
    st=find5(lines(a,thr))
    if len(st)>=len(clefs):break
print("staves",len(st))
d=ImageDraw.Draw(im)
f=ImageFont.truetype("arial.ttf",12)
for s,cl in zip(st,clefs):
    sp=(s[4]-s[0])/4; names=T if cl=="T" else B
    for k in range(-5,14):
        y=s[4]-k*sp/2; n=names[4+k] if 0<=4+k<len(names) else "?"
        if k%2==0:
            col=(255,0,0) if 0<=k<=8 else (0,170,0)
            for x in range(0,im.width,6): d.line([(x,y),(x+2,y)],fill=col)
        else:
            for x in range(0,im.width,10): d.point((x,y),fill=(0,0,255))
        d.text((1,y-6),n,fill=(150,0,150),font=f)
im=im.resize((int(im.width*z),int(im.height*z)),Image.LANCZOS)
out=sys.argv[6] if len(sys.argv)>6 else p.replace("crops","w").replace(".png",f"_{x0}.png")
im.save(out);print(out)
