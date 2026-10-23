import sys, numpy as np
from PIL import Image, ImageDraw
import lg2
BANDS={1:((99,181),(663,746)),2:((108,188),(670,753)),3:((104,188),(432,515)),4:((112,198),(461,544))}
def band(im,a_full,s,idx,x0,x1,clef,pad,z,xfit=None):
    (t0,t1)=BANDS[s][idx]
    fx0,fx1=xfit if xfit else (x0,x1)
    A,B=lg2.tracks(a_full[:,fx0:fx1],t0-15,t1+15)
    # shift A for window offset differences: tracks are relative to fx0
    w=im.crop((x0,t0-pad,x1,t1+pad)); rgb=Image.merge('RGB',(w,w,w)); d=ImageDraw.Draw(rgb)
    names=lg2.SC[clef]
    for k in range(-4,13):
        nm=names[4+k] if 0<=4+k<len(names) else '?'
        col=((255,0,0) if 0<=k<=8 else (0,160,0)) if k%2==0 else (0,110,255)
        pts=[]
        for x in range(0,rgb.width+1,8):
            xr=x+x0-fx0
            bot=np.polyval(A,xr)-(t0-pad); sp=np.polyval(B,xr)
            pts.append((x,bot-k*sp/2))
        for i in range(0,len(pts)-1,2): d.line([pts[i],pts[i+1]],fill=col)
        d.text((2,pts[0][1]-6),nm,fill=(160,0,160)); d.text((rgb.width-24,pts[-1][1]-6),nm,fill=(160,0,160))
    return rgb
def make(s,x0,x1,z=3.5,pad=55,out=None,xfit=None):
    im=Image.open('crops/d%d.png'%s).convert('L'); a=np.asarray(im)<128
    t=band(im,a,s,0,x0,x1,'T',pad,z,xfit); b=band(im,a,s,1,x0,x1,'B',pad,z,xfit)
    W=x1-x0
    c=Image.new('RGB',(W,t.height+b.height+6),(128,128,128)); c.paste(t,(0,0)); c.paste(b,(0,t.height+6))
    c=c.resize((int(W*z),int(c.height*z)),Image.LANCZOS); d=ImageDraw.Draw(c)
    for x in range((x0//50+1)*50,x1,50):
        X=(x-x0)*z; d.line([(X,0),(X,14)],fill=(255,0,0),width=2); d.text((X+3,0),str(x),fill=(255,0,0))
    c.save(out or 'g%d_%d.png'%(s,x0))
if __name__=='__main__':
    s,x0,x1=map(int,sys.argv[1:4]); make(s,x0,x1,z=float(sys.argv[4]) if len(sys.argv)>4 else 3.5)
