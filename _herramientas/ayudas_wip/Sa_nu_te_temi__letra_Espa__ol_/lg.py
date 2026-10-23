import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
SC={"T":["A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4","F4","G4","A4","B4","C5"],
    "B":["C2","D2","E2","F2","G2","A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4"]}
def fit(a,y0,y1):
    # a: bool dark array window; find best 5-line comb in [y0,y1]
    prof=a.mean(axis=1)
    best=None
    for sp in np.arange(14,40,0.5):
        for st in range(y0,int(y1-4*sp)):
            ys=(st+np.arange(5)*sp).round().astype(int)
            sc=sum(prof[max(0,y-1):y+2].max() for y in ys)
            if best is None or sc>best[0]: best=(sc,st,sp)
    return best
def run(path,x0,x1,staff,clef,y0,y1,zoom,out):
    im=Image.open(path).convert('L')
    w=im.crop((x0,0,x1,im.height))
    a=np.asarray(w)<128
    sc,st,sp=fit(a,y0,y1)
    print('fit',sc,st,sp)
    rgb=Image.merge('RGB',(w,w,w))
    d=ImageDraw.Draw(rgb)
    names=SC[clef]
    bot=st+4*sp
    for k in range(-4,13):
        y=bot-k*sp/2
        nm=names[4+k] if 0<=4+k<len(names) else '?'
        if k%2==0:
            col=(255,0,0) if 0<=k<=8 else (0,160,0)
        else: col=(0,100,255)
        for x in range(0,rgb.width,6):
            d.line([(x,y),(x+2,y)],fill=col)
        d.text((2,y-6),nm,fill=(160,0,160))
        d.text((rgb.width-22,y-6),nm,fill=(160,0,160))
    top=int(y0-3*sp); bt=int(y1+3*sp)
    rgb=rgb.crop((0,max(0,top),rgb.width,bt))
    rgb=rgb.resize((int(rgb.width*zoom),int(rgb.height*zoom)),Image.LANCZOS)
    rgb.save(out)
if __name__=='__main__':
    p,x0,x1,clef,y0,y1,z,out=sys.argv[1:9]
    run(p,int(x0),int(x1),0,clef,int(y0),int(y1),float(z),out)
