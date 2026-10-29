import sys,json
sys.path.insert(0,'../..')
from PIL import Image, ImageDraw, ImageFont
from guide import SCALE
def run(i, staves, clefs, x0, x1, zoom, src='ds'):
    im=Image.open(f'{src}{i}.png').convert('RGB')
    d=ImageDraw.Draw(im); font=ImageFont.truetype('arial.ttf',13)
    W=im.width
    for st,cl in zip(staves,clefs):
        sp=(st[4]-st[0])/4; names=SCALE[cl]
        for k in range(-5,14):
            y=st[4]-k*sp/2
            nm=names[4+k] if 0<=4+k<len(names) else '?'
            if k%2==0:
                col=(220,0,0) if 0<=k<=8 else (0,150,0)
                d.line([(0,y),(W,y)],fill=col,width=1)
            else:
                for x in range(0,W,12): d.line([(x,y),(x+5,y)],fill=(0,90,220),width=1)
            for x in range(x0+2, x1, 250): d.text((x,y-7),nm,fill=(120,0,120),font=font)
    im=im.crop((x0,0,x1,im.height)); im=im.resize((int(im.width*zoom),int(im.height*zoom)),Image.LANCZOS)
    out=f'g{i}_{x0}.png'; im.save(out); print(out,im.size)
if __name__=='__main__':
    i=int(sys.argv[1]); st=json.loads(sys.argv[2]); cl=sys.argv[3]
    run(i,st,cl,int(sys.argv[4]),int(sys.argv[5]),float(sys.argv[6]))
