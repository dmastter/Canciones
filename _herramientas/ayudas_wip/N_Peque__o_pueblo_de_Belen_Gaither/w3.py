import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'C:/Users/ESB0001672/Canciones_work')
from guide import SCALE
from w2 import best_angle, groups
font=ImageFont.truetype('arial.ttf',12)
def staves_in(p,thr):
    cen=groups(p,thr);st=[];i=0
    while i+4<len(cen):
        c=cen[i:i+5];g=np.diff(c)
        if g.max()-g.min()<4 and 8<g.mean()<60: st.append(c);i+=5
        else: i+=1
    return st
def main(page,y0,y1,x0,x1,clefs,win,zoom,outp,ang=None,start=0,lyr=5.5):
    im=Image.open(page).convert('RGB').crop((x0,y0,x1,y1))
    a=np.asarray(im.convert('L'))<140
    if ang is None: ang=best_angle(a[:,150:-50])
    im=im.rotate(ang,resample=Image.BICUBIC,fillcolor=(255,255,255))
    a=np.asarray(im.convert('L'))<140
    print('ang',round(ang,1),im.size)
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
            t=int(s[0]-4.5*sp);b=int(s[4]+lyr*sp)
            w=im.crop((x,t,xe,b)).copy();d=ImageDraw.Draw(w)
            for k in range(-4,13):
                y=s[4]-k*sp/2-t
                if k%2==0:
                    d.line([(0,y),(w.width,y)],fill=(255,120,120) if 0<=k<=8 else (120,200,120),width=1)
                nm=names[4+k] if 0<=4+k<len(names) else '?'
                for xx in (2,w.width-28):
                    d.text((xx,y-6),nm,fill=(160,0,160),font=font)
            strips.append(w)
        H=sum(s.height for s in strips)
        out=Image.new('RGB',(xe-x,H),(255,255,255));yy=0
        for s in strips: out.paste(s,(0,yy));yy+=s.height
        out=out.resize((int(out.width*zoom),int(out.height*zoom)),Image.LANCZOS)
        out.save(f'{outp}_{n}.png');print(f'{outp}_{n}.png x{x}-{xe}',out.size)
        n+=1
        if xe>=W: break
        x+=win-80
if __name__=='__main__':
    a=sys.argv
    main(a[1],int(a[2]),int(a[3]),int(a[4]),int(a[5]),a[6],int(a[7]),float(a[8]),a[9])
