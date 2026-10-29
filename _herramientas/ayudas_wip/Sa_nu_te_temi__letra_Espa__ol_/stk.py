import sys
from PIL import Image, ImageDraw
BANDS={1:((99,181),(663,746)),2:((108,188),(670,753)),3:((104,188),(432,515)),4:((112,198),(461,544))}
def make(s,x0,x1,z=3.5,pad=60,out=None):
    im=Image.open('crops/d%d.png'%s).convert('L')
    (t0,t1),(b0,b1)=BANDS[s]
    a=im.crop((x0,t0-pad,x1,t1+pad)); b=im.crop((x0,b0-pad,x1,b1+pad))
    W=x1-x0
    c=Image.new('L',(W,a.height+b.height+6),128)
    c.paste(a,(0,0)); c.paste(b,(0,a.height+6))
    c=c.resize((int(W*z),int(c.height*z)),Image.LANCZOS).convert('RGB')
    d=ImageDraw.Draw(c)
    for x in range((x0//50+1)*50,x1,50):
        X=(x-x0)*z; d.line([(X,0),(X,14)],fill=(255,0,0),width=2); d.text((X+3,0),str(x),fill=(255,0,0))
    c.save(out or 'st%d_%d.png'%(s,x0))
if __name__=='__main__':
    s,x0,x1=map(int,sys.argv[1:4]); make(s,x0,x1)
