import sys
from PIL import Image, ImageDraw
T=["A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4","F4","G4","A4","B4","C5"]
B=["C2","D2","E2","F2","G2","A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4"]
ST={1:(282,362,824,904),2:(1103,1185,1672,1758),3:(1962,2050,2303,2390),4:(2663,2752,3029,3117)}
def run(s,which,x0,x1,zoom=2.5):
    im=Image.open("p1r.png").convert("RGB")
    t0,t1,b0,b1=ST[s]
    top,bot=(t0,t1) if which=="T" else (b0,b1)
    sc=T if which=="T" else B
    sp=(bot-top)/4
    d=ImageDraw.Draw(im)
    for k in range(-5,14):
        y=bot-k*sp/2
        name=sc[4+k] if 0<=4+k<len(sc) else "?"
        if k%2==0:
            col=(255,0,0) if 0<=k<=8 else (0,160,0)
            d.line([(x0,y),(x1,y)],fill=col,width=1)
        else:
            for x in range(x0,x1,10): d.line([(x,y),(x+4,y)],fill=(0,90,255),width=1)
        for x in range(x0+4,x1,200): d.text((x,y-5),name,fill=(160,0,160))
    c=im.crop((x0,int(top-sp*3.5),x1,int(bot+sp*3.5)))
    c=c.resize((int(c.width*zoom),int(c.height*zoom)),Image.LANCZOS)
    c.save(f"g{s}{which}_{x0}.png")
s,w,x0,x1=int(sys.argv[1]),sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
run(s,w,x0,x1,float(sys.argv[5]) if len(sys.argv)>5 else 2.5)
