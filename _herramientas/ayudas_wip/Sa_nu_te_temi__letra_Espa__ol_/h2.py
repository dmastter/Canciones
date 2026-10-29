import sys, numpy as np, cv2
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from heads import BANDS, SC
from lt2 import lines_track2
def run(s,x0,x1,z=3.4,thr=5.0,pad=55,out=None,verbose=True):
    im=Image.open('crops/d%d.png'%s).convert('L'); g=np.asarray(im)
    _,bw=cv2.threshold(g,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    parts=[];allres=[]
    for idx,clef in ((0,'T'),(1,'B')):
        t0,t1=BANDS[s][idx]
        fits,_=lines_track2(bw,t0,t1)
        ker=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,11))
        op=cv2.morphologyEx(bw,cv2.MORPH_OPEN,ker)
        band=np.zeros_like(op); band[t0-pad:t1+pad,:]=op[t0-pad:t1+pad,:]
        dist=cv2.distanceTransform(band,cv2.DIST_L2,5)
        mx=ndi.maximum_filter(dist,size=11)
        pk=(dist==mx)&(dist>=thr)
        lab,n=ndi.label(pk); cs=ndi.center_of_mass(pk,lab,range(1,n+1))
        w=im.crop((x0,t0-pad,x1,t1+pad)).convert('RGB').resize((int((x1-x0)*z),int((t1-t0+2*pad)*z)),Image.LANCZOS)
        d=ImageDraw.Draw(w)
        for k in range(0,9,2):
            pts=[((X),(np.polyval(fits[4-k//2],x0+X/z)-(t0-pad))*z) for X in range(0,w.width,8)]
            for i in range(0,len(pts)-1,2): d.line([pts[i],pts[i+1]],fill=(255,150,150),width=1)
        for (cy,cx) in sorted(cs,key=lambda c:c[1]):
            if not (x0<=cx<x1): continue
            bot=np.polyval(fits[4],cx); sp=(bot-np.polyval(fits[0],cx))/4
            pos=(bot-cy)/(sp/2); k=int(round(pos))
            nm=SC[clef][4+k] if 0<=4+k<17 else '?'
            X=(cx-x0)*z; Y=(cy-(t0-pad))*z
            d.ellipse([X-6,Y-6,X+6,Y+6],outline=(255,0,0),width=2)
            d.text((X+9,Y-8),'%s%+.1f'%(nm,pos-k),fill=(0,0,255))
            allres.append((clef,round(cx),round(cy),round(pos,2),nm))
        parts.append(w)
    H=sum(p.height for p in parts)+6
    c=Image.new('RGB',(parts[0].width,H),(128,128,128)); y=0
    for p in parts: c.paste(p,(0,y)); y+=p.height+6
    d=ImageDraw.Draw(c)
    for x in range((x0//50+1)*50,x1,50):
        X=(x-x0)*z; d.line([(X,0),(X,14)],fill=(255,0,0),width=2); d.text((X+3,0),str(x),fill=(255,0,0))
    c.save(out or 'h%d_%d.png'%(s,x0))
    if verbose:
        for r in allres: print(*r)
if __name__=='__main__':
    s,x0,x1=map(int,sys.argv[1:4]); run(s,x0,x1,float(sys.argv[4]) if len(sys.argv)>4 else 3.4)
