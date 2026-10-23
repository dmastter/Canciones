import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'C:/Users/ESB0001672/Canciones_work')
from guide import SCALE
from w2 import best_angle, groups
from w3 import staves_in
font=ImageFont.truetype('arial.ttf',15)
def fit_staff(strip):
    a=np.asarray(strip.convert('L'))<140
    best=None
    for ang in np.arange(-3,3.01,0.1):
        r=np.asarray(Image.fromarray((a*255).astype('uint8')).rotate(ang,resample=Image.BILINEAR,fillcolor=0))>100
        p=r.sum(axis=1).astype(float)
        s=(p**2).sum()
        if best is None or s>best[0]: best=(s,ang,p)
    return best[1]
def main(page,y0,y1,x0,x1,clefs,win,zoom,outp,start=0,lyr=5.5,step=None):
    im=Image.open(page).convert('RGB').crop((x0,y0,x1,y1))
    a=np.asarray(im.convert('L'))<140
    ang=best_angle(a[:,150:-50])
    im=im.rotate(ang,resample=Image.BICUBIC,fillcolor=(255,255,255))
    a=np.asarray(im.convert('L'))<140
    W=im.width;n=0;x=start
    while x<W:
        xe=min(W,x+win)
        p=a[:,x:xe].sum(axis=1).astype(float)
        st=None
        for f in (0.5,0.4,0.3,0.25):
            st=staves_in(p,max(p.max()*f,f*0.8*(xe-x)))
            if len(st)==len(clefs): break
        if len(st)!=len(clefs): print('window',x,'staves',len(st),'expected',len(clefs))
        strips=[]
        for s,cl in zip(st,clefs):
            sp=(s[4]-s[0])/4;names=SCALE[cl]
            t=int(s[0]-6*sp);b=int(s[4]+lyr*sp)
            w=im.crop((x,t,xe,b))
            ang2=fit_staff(w.crop((0,int(4*sp),w.width,int(10*sp))))
            w=w.rotate(ang2,resample=Image.BICUBIC,fillcolor=(255,255,255))
            aa=np.asarray(w.convert('L'))<140
            pp=aa.sum(axis=1).astype(float)
            ss=None
            for f in (0.5,0.4,0.3):
                ss=staves_in(pp,max(pp.max()*f,0.3*w.width))
                if ss: break
            if not ss: print('fail strip');strips.append(w);continue
            s2=ss[0]
            sp=(s2[4]-s2[0])/4
            d=ImageDraw.Draw(w)
            for k in range(-4,13):
                y=s2[4]-k*sp/2
                if k%2==0:
                    d.line([(0,y),(w.width,y)],fill=(255,110,110) if 0<=k<=8 else (110,200,110),width=1)
                nm=names[4+k] if 0<=4+k<len(names) else '?'
                for xx in (2,w.width//2,w.width-30):
                    d.rectangle([xx-1,y-8,xx+26,y+8],fill=(255,255,255))
                    d.text((xx,y-8),nm,fill=(160,0,160),font=font)
            strips.append(w)
        H=sum(s.height for s in strips)
        out=Image.new('RGB',(xe-x,H),(255,255,255));yy=0
        for s in strips: out.paste(s,(0,yy));yy+=s.height
        out=out.resize((int(out.width*zoom),int(out.height*zoom)),Image.LANCZOS)
        out.save(f'{outp}_{n}.png');print(f'{outp}_{n}.png x{x}-{xe}',out.size)
        n+=1
        if xe>=W: break
        x+=win-(step if step else 80)
if __name__=='__main__':
    a=sys.argv
    main(a[1],int(a[2]),int(a[3]),int(a[4]),int(a[5]),a[6],int(a[7]),float(a[8]),a[9])
