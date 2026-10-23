import sys, numpy as np, cv2
from PIL import Image, ImageDraw
from heads import lines_track, BANDS, SC
def make(s,x0,x1,z=3.5,pad=50,out=None):
    im=Image.open('crops/d%d.png'%s).convert('L'); g=np.asarray(im)
    _,bw=cv2.threshold(g,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    parts=[]
    for idx,clef in ((0,'T'),(1,'B')):
        t0,t1=BANDS[s][idx]
        fits=lines_track(bw,t0,t1)
        w=im.crop((x0,t0-pad,x1,t1+pad)); rgb=Image.merge('RGB',(w,w,w)).resize((int(w.width*z),int(w.height*z)),Image.LANCZOS)
        d=ImageDraw.Draw(rgb)
        names=SC[clef]
        for k in range(-4,13):
            nm=names[4+k] if 0<=4+k<17 else '?'
            col=((255,0,0) if 0<=k<=8 else (0,170,0)) if k%2==0 else (0,110,255)
            pts=[]
            for X in range(0,rgb.width+1,6):
                x=x0+X/z
                bot=np.polyval(fits[4],x); top=np.polyval(fits[0],x); sp=(bot-top)/4
                y=(bot-k*sp/2-(t0-pad))*z
                pts.append((X,y))
            if k%2==0:
                for i in range(0,len(pts)-1,3): d.line([pts[i],pts[i+1]],fill=col,width=1)
            else:
                for i in range(0,len(pts)-1,6): d.line([pts[i],pts[i]],fill=col,width=1)
            d.text((1,pts[0][1]-6),nm,fill=(160,0,160)); d.text((rgb.width-24,pts[-1][1]-6),nm,fill=(160,0,160))
        parts.append(rgb)
    H=sum(p.height for p in parts)+6
    c=Image.new('RGB',(parts[0].width,H),(128,128,128)); y=0
    for p in parts: c.paste(p,(0,y)); y+=p.height+6
    d=ImageDraw.Draw(c)
    for x in range((x0//50+1)*50,x1,50):
        X=(x-x0)*z; d.line([(X,0),(X,14)],fill=(255,0,0),width=2); d.text((X+3,0),str(x),fill=(255,0,0))
    c.save(out or 'q%d_%d.png'%(s,x0))
if __name__=='__main__':
    s,x0,x1=map(int,sys.argv[1:4]); make(s,x0,x1,float(sys.argv[4]) if len(sys.argv)>4 else 3.5)
