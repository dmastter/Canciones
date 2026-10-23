import sys, numpy as np, cv2
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
BANDS={1:((99,181),(663,746)),2:((108,188),(670,753)),3:((104,188),(432,515)),4:((112,198),(461,544))}
SC={"T":["A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4","F4","G4","A4","B4","C5"],
    "B":["C2","D2","E2","F2","G2","A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4"]}
def lines_track(bw,t0,t1):
    k=cv2.getStructuringElement(cv2.MORPH_RECT,(45,1))
    lm=cv2.morphologyEx(bw,cv2.MORPH_OPEN,k)
    H,W=bw.shape
    # per-column runs in band
    ys=np.full((5,W),np.nan)
    sp0=(t1-t0)/4
    exp=t0+np.arange(5)*sp0
    for x in range(W):
        col=lm[max(0,t0-12):t1+13,x]>0
        idx=np.where(col)[0]
        if len(idx)==0: continue
        groups=np.split(idx,np.where(np.diff(idx)>1)[0]+1)
        for g in groups:
            if len(g)>11: continue
            c=g.mean()+max(0,t0-12)
            j=np.argmin(abs(exp-c))
            if abs(exp[j]-c)<sp0*0.45: ys[j,x]=c
    fits=[]
    X=np.arange(W)
    for j in range(5):
        ok=~np.isnan(ys[j])
        # use global poly deg 2 then robust
        p=np.polyfit(X[ok],ys[j][ok],2)
        r=ys[j][ok]-np.polyval(p,X[ok]); keep=abs(r)<3*r.std()+1
        p=np.polyfit(X[ok][keep],ys[j][ok][keep],2)
        fits.append(p)
    return fits
def detect(s,x0,x1,out,z=3):
    im=Image.open('crops/d%d.png'%s).convert('L'); g=np.asarray(im)
    _,bw=cv2.threshold(g,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    rgb=Image.merge('RGB',(im,im,im)); d=ImageDraw.Draw(rgb)
    res=[]
    for idx,clef in ((0,'T'),(1,'B')):
        t0,t1=BANDS[s][idx]
        fits=lines_track(bw,t0,t1)
        ker=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,11))
        op=cv2.morphologyEx(bw,cv2.MORPH_OPEN,ker)
        band=np.zeros_like(op); band[t0-70:t1+70,:]=op[t0-70:t1+70,:]
        dist=cv2.distanceTransform(band,cv2.DIST_L2,5)
        mx=ndi.maximum_filter(dist,size=13)
        pk=(dist==mx)&(dist>=4.2)
        lab,n=ndi.label(pk)
        cs=ndi.center_of_mass(pk,lab,range(1,n+1))
        for (cy,cx) in sorted(cs,key=lambda c:c[1]):
            if not (x0<=cx<x1): continue
            bot=np.polyval(fits[4],cx); top=np.polyval(fits[0],cx); sp=(bot-top)/4
            pos=(bot-cy)/(sp/2)   # half-steps above bottom line
            k=int(round(pos))
            nm=SC[clef][4+k] if 0<=4+k<17 else '?'
            res.append((clef,cx,cy,pos,nm))
            d.ellipse([cx-4,cy-4,cx+4,cy+4],outline=(255,0,0),width=2)
            d.text((cx+6,cy-6),nm+'%+.1f'%(pos-k),fill=(0,0,255))
    c=rgb.crop((x0,0,x1,im.height)); 
    # stack bands
    (t0,t1),(b0,b1)=BANDS[s]
    a=c.crop((0,t0-70,c.width,t1+70)); b=c.crop((0,b0-70,c.width,b1+70))
    st=Image.new('RGB',(c.width,a.height+b.height+4),(128,128,128)); st.paste(a,(0,0)); st.paste(b,(0,a.height+4))
    st=st.resize((int(st.width*z),int(st.height*z)),Image.LANCZOS); st.save(out)
    for r in res: print(r[0],round(r[1]),round(r[2]),round(r[3],2),r[4])
if __name__=='__main__':
    s,x0,x1=map(int,sys.argv[1:4]); detect(s,x0,x1,'h%d_%d.png'%(s,x0),float(sys.argv[4]) if len(sys.argv)>4 else 3)
