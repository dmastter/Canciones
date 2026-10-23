import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'C:/Users/ESB0001672/Canciones_work')
from guide2 import fit, T, B
def render(path, x0, x1, zoom, out, clefs='TB'):
    im0 = Image.open(path).convert('L'); st = fit(im0.convert('RGB'), len(clefs))
    a = np.asarray(im0).copy(); dark = a < 150
    clean = a.copy()
    H, W = a.shape
    for px, py, sp in st:
        for j in range(5):
            for x in range(W):
                yl = float(np.interp(x, px, py)) + j*sp
                yi = int(round(yl)); h = 4
                if yi-h-3 < 0 or yi+h+3 >= H: continue
                if (not dark[yi-h-2, x]) and (not dark[yi+h+2, x]) :
                    clean[yi-h:yi+h+1, x] = 255
                elif (not dark[yi-h-3, x]) and (not dark[yi+h+3,x]):
                    clean[yi-h:yi+h+1, x] = 255
    im = Image.merge('RGB', [Image.fromarray(clean)]*3)
    d = ImageDraw.Draw(im); font = ImageFont.truetype('arial.ttf', 12)
    for (px, py, sp), cl in zip(st, clefs):
        names = T if cl=='T' else B
        for k in range(-6, 15):
            ya = lambda x, k=k, px=px, py=py, sp=sp: float(np.interp(x, px, py)) + 4*sp - k*sp/2
            line = (k % 2 == 0)
            col = (235,120,120) if (line and 0<=k<=8) else ((120,200,120) if line else (170,190,240))
            for xx in range(x0, x1, 6):
                d.point((xx, ya(xx)), fill=col)
            for xx in (x0+2, x1-24):
                nm = names[4+k] if 0<=4+k<len(names) else ''
                if nm and (line or True): d.text((xx, ya(xx)-6), nm, fill=(150,0,150), font=font)
    im = im.crop((x0, 0, x1, im.height)); im = im.resize((int(im.width*zoom), int(im.height*zoom)), Image.LANCZOS)
    im.save(out)
if __name__=='__main__':
    render(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5])
