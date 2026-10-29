import sys, numpy as np
from PIL import Image, ImageDraw
SC={"T":["A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4","F4","G4","A4","B4","C5"],
    "B":["C2","D2","E2","F2","G2","A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4"]}
def comb(a,ylo,yhi,spr=(17,26)):
    prof=a.mean(axis=1)
    best=None
    for sp in np.arange(spr[0],spr[1],0.5):
        for st in range(ylo,int(yhi-4*sp)):
            ys=(st+np.arange(5)*sp).round().astype(int)
            sc=sum(prof[max(0,y-1):y+2].max() for y in ys)
            if best is None or sc>best[0]: best=(sc,st,sp)
    return best
def tracks(a,ylo,yhi,strip=60):
    xs=[];st=[];sps=[];scs=[]
    for x in range(0,a.shape[1]-strip+1,strip//2):
        sc,s,sp=comb(a[:,x:x+strip],ylo,yhi)
        xs.append(x+strip/2);st.append(s);sps.append(sp);scs.append(sc)
    xs=np.array(xs);st=np.array(st,float);sps=np.array(sps);scs=np.array(scs)
    good=scs>=np.percentile(scs,50)
    # linear fit of bottom line y = st+4sp
    bot=st+4*sps
    A=np.polyfit(xs[good],bot[good],1); B=np.polyfit(xs[good],sps[good],1)
    return A,B
def run(path,x0,x1,clef,ylo,yhi,zoom,out):
    im=Image.open(path).convert('L')
    a_full=np.asarray(im)<128
    A,B=tracks(a_full[:,x0:x1],ylo,yhi)
    print(A,B)
    w=im.crop((x0,0,x1,im.height))
    rgb=Image.merge('RGB',(w,w,w)); d=ImageDraw.Draw(rgb)
    names=SC[clef]
    for k in range(-4,13):
        nm=names[4+k] if 0<=4+k<len(names) else '?'
        col=((255,0,0) if 0<=k<=8 else (0,160,0)) if k%2==0 else (0,110,255)
        pts=[]
        for x in range(0,rgb.width+1,10):
            bot=np.polyval(A,x); sp=np.polyval(B,x)
            pts.append((x,bot-k*sp/2))
        for i in range(0,len(pts)-1,2):
            d.line([pts[i],pts[i+1]],fill=col)
        d.text((2,pts[0][1]-6),nm,fill=(160,0,160)); d.text((rgb.width-22,pts[-1][1]-6),nm,fill=(160,0,160))
    top=int(min(ylo,np.polyval(A,0)-8*np.polyval(B,0)/2*2)-30); bt=int(yhi+40)
    rgb=rgb.crop((0,max(0,top),rgb.width,bt))
    rgb=rgb.resize((int(rgb.width*zoom),int(rgb.height*zoom)),Image.LANCZOS); rgb.save(out)
if __name__=='__main__':
    p,x0,x1,clef,ylo,yhi,z,out=sys.argv[1:9]
    run(p,int(x0),int(x1),clef,int(ylo),int(yhi),float(z),out)
