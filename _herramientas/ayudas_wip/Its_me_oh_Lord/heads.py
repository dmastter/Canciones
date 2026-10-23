import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0,'C:/Users/ESB0001672/Canciones_work')
from guide2 import fit, T, B
def run(path, x0=0, x1=None):
    im0 = Image.open(path).convert('L'); st = fit(im0.convert('RGB'), 2)
    a = np.asarray(im0); dark = a < 150; H, W = a.shape
    clean = dark.copy()
    for px, py, sp in st:
        for j in range(5):
            for x in range(W):
                yi = int(round(float(np.interp(x, px, py)) + j*sp)); h=4
                if yi-h-3<0 or yi+h+3>=H: continue
                if (not dark[yi-h-2,x] and not dark[yi+h+2,x]) or (not dark[yi-h-3,x] and not dark[yi+h+3,x]):
                    clean[yi-h:yi+h+1, x] = False
    op = ndi.binary_opening(clean, structure=np.ones((9,9)))
    lab, n = ndi.label(op)
    objs = ndi.find_objects(lab)
    res = []
    for i, sl in enumerate(objs):
        ys, xs = sl; cy = (ys.start+ys.stop)/2; cx = (xs.start+xs.stop)/2
        h = ys.stop-ys.start; w = xs.stop-xs.start
        if x1 and not (x0 <= cx < x1): continue
        # staff assign
        best=None
        for si,(px,py,sp) in enumerate(st):
            top = float(np.interp(cx, px, py)); bot = top+4*sp; mid=(top+bot)/2
            d = abs(cy-mid)
            if best is None or d<best[0]: best=(d,si,top,bot,sp)
        _, si, top, bot, sp = best
        # step: 0 = bottom line, +1 per half space
        def step(y): return (bot - y)/(sp/2)
        res.append((cx, si, step(ys.start+ (sp*0.5 if h>sp*1.3 else h/2)), step(ys.stop-(sp*0.5 if h>sp*1.3 else h/2)), h/sp, w/sp))
    res.sort()
    names = {0:T, 1:B}
    for cx, si, s_top, s_bot, hh, ww in res:
        def nm(s):
            k=int(round(s)); idx=4+k
            return names[si][idx] if 0<=idx<len(names[si]) else str(k)
        if ww<0.7 or hh<0.7: continue
        if abs(s_top)>20: continue
        print(f"x={cx:6.0f} {'TB'[si]} top={nm(s_top)}({s_top:4.1f}) bot={nm(s_bot)}({s_bot:4.1f}) h={hh:.1f} w={ww:.1f}")
if __name__=='__main__':
    run(sys.argv[1], int(sys.argv[2]) if len(sys.argv)>2 else 0, int(sys.argv[3]) if len(sys.argv)>3 else None)
