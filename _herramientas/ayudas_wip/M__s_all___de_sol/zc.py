import sys
from PIL import Image
# uso: zc.py crop x0 y0 x1 y1 zoom out
p,x0,y0,x1,y1,z,out=sys.argv[1:8]
x0,y0,x1,y1=map(int,(x0,y0,x1,y1)); z=float(z)
im=Image.open(p).convert('L').crop((x0,y0,x1,y1))
im=im.resize((int(im.width*z),int(im.height*z)),Image.LANCZOS)
im.save(out)
