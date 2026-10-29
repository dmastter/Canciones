import sys, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,'C:/Users/ESB0001672/Canciones_work')
from w2 import best_angle
from w3 import staves_in
def main(page,y0,y1,x0,x1,n_st,win,zoom,outp,start=0,lyr=6.5,over=100):
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
            if len(st)==n_st: break
        if len(st)!=n_st: print('window',x,'staves',len(st),'expected',n_st)
        strips=[]
        for i,s in enumerate(st):
            sp=(s[4]-s[0])/4
            t=int(s[0]-5*sp);b=int(s[4]+lyr*sp)
            strips.append(im.crop((x,t,xe,b)))
        H=sum(s.height for s in strips)
        out=Image.new('RGB',(xe-x,H),(255,255,255));yy=0;d=ImageDraw.Draw(out)
        for i,s in enumerate(strips):
            out.paste(s,(0,yy));yy+=s.height
            d.line([(0,yy-1),(xe-x,yy-1)],fill=(0,0,255),width=1)
        out=out.resize((int(out.width*zoom),int(out.height*zoom)),Image.LANCZOS)
        out.save(f'{outp}_{n}.png');print(f'{outp}_{n}.png x{x}-{xe}',out.size)
        n+=1
        if xe>=W: break
        x+=win-over
if __name__=='__main__':
    a=sys.argv
    main(a[1],int(a[2]),int(a[3]),int(a[4]),int(a[5]),int(a[6]),int(a[7]),float(a[8]),a[9])
