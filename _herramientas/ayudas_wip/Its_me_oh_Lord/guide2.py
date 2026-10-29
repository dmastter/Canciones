import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, 'C:/Users/ESB0001672/Canciones_work')
from staffdet import find_staves
T = ["A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4","F4","G4","A4","B4","C5"]  # idx4 = bottom line E3
B = ["C2","D2","E2","F2","G2","A2","B2","C3","D3","E3","F3","G3","A3","B3","C4","D4","E4"]  # idx4 = G2
def fit(im, n=2):
    a = (np.asarray(im.convert('L')) < 150).astype(float)
    W = a.shape[1]; xs=[]; ys=[[] for _ in range(n)]; sps=[[] for _ in range(n)]
    for x0 in range(150, W-250, 150):
        r = find_staves(a, x0, x0+250, n)
        if len(r) < n: continue
        xs.append(x0+125)
        for i,(s,y0,sp) in enumerate(r): ys[i].append(y0); sps[i].append(sp)
    res=[]
    A=a
    out=[]
    for i in range(n):
        c0=np.polyfit(xs, ys[i], 1); sp=float(np.median(sps[i]))
        px=[];py=[]
        for x0 in range(100, W-100, 60):
            f=A[:, x0:x0+120].mean(axis=1); best=None
            for y0 in np.arange(np.polyval(c0,x0+60)-9, np.polyval(c0,x0+60)+9, 0.5):
                sc=sum(f[max(0,int(round(y0+j*sp))-1):int(round(y0+j*sp))+2].mean() for j in range(5))
                if best is None or sc>best[0]: best=(sc,y0)
            px.append(x0+60); py.append(best[1])
        py=np.convolve(np.pad(py,2,mode='edge'),np.ones(5)/5,mode='valid')
        out.append((px,py,sp))
    return out
    for i in range(n):
        c = np.polyfit(xs, ys[i], 1)
        # robust: refit dropping outliers
        resid = np.array(ys[i]) - np.polyval(c, xs)
        keep = np.abs(resid) < 6
        c = np.polyfit(np.array(xs)[keep], np.array(ys[i])[keep], 1)
        res.append((c, float(np.median(sps[i]))))
    return res
def render(path, x0, x1, zoom, clefs='TB', out=None):
    im = Image.open(path).convert('RGB'); st = fit(im, len(clefs))
    d = ImageDraw.Draw(im); font = ImageFont.truetype('arial.ttf', 12)
    for (px, py, sp), cl in zip(st, clefs):
        names = T if cl=='T' else B
        for x in range(0, im.width, 1):
            pass
        for k in range(-5, 13):
            for xx in range(x0, x1, 1):
                pass
            ya = lambda x, px=px, py=py, sp=sp, k=k: float(np.interp(x, px, py)) + 4*sp - k*sp/2
            col = (220,0,0) if (k%2==0 and 0<=k<=8) else ((0,150,0) if k%2==0 else (0,90,220))
            pts = [(x, ya(x)) for x in range(x0, x1, 20)]
            if k%2==0: d.line(pts, fill=col, width=1)
            else:
                for xx in range(x0, x1, 10): d.line([(xx, ya(xx)), (xx+4, ya(xx))], fill=col)
            nm = names[4+k] if 0<=4+k<len(names) else '?'
            d.text((x0+2, ya(x0+2)-7), nm, fill=(140,0,140), font=font)
            d.text((x1-22, ya(x1-22)-7), nm, fill=(140,0,140), font=font)
    im = im.crop((x0, 0, x1, im.height)); im = im.resize((int(im.width*zoom), int(im.height*zoom)), Image.LANCZOS)
    im.save(out)
if __name__ == '__main__':
    p, x0, x1, z, o = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    render(p, x0, x1, z, 'TB', o)
