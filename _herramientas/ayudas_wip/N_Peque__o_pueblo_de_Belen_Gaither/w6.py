import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'C:/Users/ESB0001672/Canciones_work')
from guide import SCALE
from w2 import best_angle
from w3 import staves_in
from scipy.ndimage import median_filter
font=ImageFont.truetype('arial.ttf',14)
def track(a,rough,sp0):
    # a: boolean array (h,w); rough: y of staff top line; returns arrays y0[x], sp[x]
    h,w=a.shape;SL=50
    xs=[];Y=[];S=[]
    for xc in range(0,w,SL//2):
        sl=a[:,max(0,xc-SL):xc+SL]
        p=sl.sum(axis=1).astype(float)
        best=None
        for sp in np.arange(sp0*0.9,sp0*1.1,0.25):
            for y0 in np.arange(rough-0.8*sp0,rough+0.8*sp0,0.5):
                ys=y0+np.arange(5)*sp
                if ys[-1]>=h-1 or y0<1: continue
                sc=sum(p[int(round(y))-1:int(round(y))+2].sum() for y in ys)
                if best is None or sc>best[0]: best=(sc,y0,sp)
        xs.append(xc);Y.append(best[1]);S.append(best[2])
    Y=median_filter(np.array(Y),size=5,mode='nearest');S=median_filter(np.array(S),size=5,mode='nearest')
    return np.interp(np.arange(w),xs,Y),np.interp(np.arange(w),xs,S)
def main(page,y0,y1,x0,x1,clefs,win,zoom,outp,start=0,over=100,lyr=6.5,labels=True):
    im=Image.open(page).convert('RGB').crop((x0,y0,x1,y1))
    a=np.asarray(im.convert('L'))<140
    ang=best_angle(a[:,150:-50])
    im=im.rotate(ang,resample=Image.BICUBIC,fillcolor=(255,255,255))
    a=np.asarray(im.convert('L'))<140
    W=im.width;n=0;x=start
    while x<W:
        xe=min(W,x+win)
        p=a[:,x:xe].sum(axis=1).astype(float)
        for f in (0.5,0.4,0.3,0.25):
            st=staves_in(p,max(p.max()*f,f*0.8*(xe-x)))
            if len(st)==len(clefs): break
        if len(st)!=len(clefs): print('window',x,'staves',len(st),'expected',len(clefs))
        strips=[]
        for s,cl in zip(st,clefs):
            sp0=(s[4]-s[0])/4;names=SCALE[cl]
            t=int(s[0]-5*sp0);b=int(s[4]+lyr*sp0)
            sub=a[t:b,x:xe]
            Yt,St=track(sub,s[0]-t,sp0)
            w=im.crop((x,t,xe,b)).resize((int((xe-x)*zoom),int((b-t)*zoom)),Image.LANCZOS);d=ImageDraw.Draw(w)
            for k in range(-4,13):
                pts=[]
                for xx in range(0,xe-x,10):
                    yb=Yt[xx]+4*St[xx]
                    pts.append((xx*zoom,(yb-k*St[xx]/2)*zoom))
                if k%2==0:
                    col=(255,90,90) if 0<=k<=8 else (90,190,90)
                    d.line(pts,fill=col,width=1)
                nm=names[4+k] if 0<=4+k<len(names) else '?'
                for xx in (2,(xe-x)*zoom-28):
                    yy=pts[min(len(pts)-1,int(xx/zoom)//10)][1]
                    d.text((xx,yy-7),nm,fill=(160,0,160),font=font)
            strips.append(w)
        H=sum(s.height for s in strips)
        out=Image.new('RGB',(int((xe-x)*zoom),H),(255,255,255));yy=0;dd=ImageDraw.Draw(out)
        for s in strips:
            out.paste(s,(0,yy));yy+=s.height;dd.line([(0,yy-1),(out.width,yy-1)],fill=(0,0,255))
        out.save(f'{outp}_{n}.png');print(f'{outp}_{n}.png x{x}-{xe}',out.size)
        n+=1
        if xe>=W: break
        x+=win-over
if __name__=='__main__':
    a=sys.argv
    main(a[1],int(a[2]),int(a[3]),int(a[4]),int(a[5]),a[6],int(a[7]),float(a[8]),a[9],labels=(a[10] if len(a)>10 else True))
