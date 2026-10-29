import sys,json
sys.path.insert(0,'../..')
from PIL import Image, ImageDraw, ImageFont
from guide import SCALE
def run(i, tst, bst, x0, x1, zoom=2.4, src='wd', pad=60, tilt=(0,0)):
    im=Image.open(f'{src}{i}.png').convert('RGB')
    parts=[]
    for st,cl,tl in ((tst,'T',tilt[0]),(bst,'B',tilt[1])):
        y0=int(st[0]-pad-30); y1=int(st[4]+pad)
        c=im.crop((x0,max(y0,0),x1,y1)).convert('RGB')
        d=ImageDraw.Draw(c); font=ImageFont.truetype('arial.ttf',12)
        sp=(st[4]-st[0])/4; names=SCALE[cl]
        for k in range(-3,12):
            y=st[4]-k*sp/2-max(y0,0)
            nm=names[4+k] if 0<=4+k<len(names) else ''
            for xx in range(0,x1-x0):
                yy=y+tl*(xx+x0-1000)/1000  # tilt: px per 1000 px
                if k%2==0 and 0<=k<=8:
                    d.point((xx,yy),fill=(255,0,0))
                elif k%2==0:
                    if xx%6<3: d.point((xx,yy),fill=(0,170,0))
            d.text((2,y-7),nm,fill=(160,0,160),font=font)
            d.text((x1-x0-30,y-7),nm,fill=(160,0,160),font=font)
        parts.append(c)
    h=sum(p.height for p in parts)+10
    out=Image.new('RGB',(parts[0].width,h),'white'); y=0
    for p in parts: out.paste(p,(0,y)); y+=p.height+10
    out=out.resize((int(out.width*zoom),int(out.height*zoom)),Image.LANCZOS)
    fn=f'seg{i}_{x0}.png'; out.save(fn); print(fn,out.size)
if __name__=='__main__':
    a=sys.argv
    tilt=(float(a[7]),float(a[8])) if len(a)>8 else (0,0)
    run(int(a[1]),json.loads(a[2]),json.loads(a[3]),int(a[4]),int(a[5]),float(a[6]) if len(a)>6 else 2.4,tilt=tilt)
