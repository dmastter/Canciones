import sys, numpy as np
from PIL import Image
def comb(a, x0, x1):
    f = a[:, x0:x1].mean(axis=1)
    H = len(f); res = []
    best = []
    for sp in np.arange(15, 27, 0.5):
        for y0 in range(0, int(H - 4*sp)):
            ys = [int(round(y0 + i*sp)) for i in range(5)]
            s = sum(f[max(0,y-1):y+2].mean() for y in ys)
            best.append((s, y0, sp))
    return best
def find_staves(a, x0, x1, n=2):
    best = sorted(comb(a, x0, x1), reverse=True)
    out = []
    for s, y0, sp in best:
        if all(abs(y0 - o[1]) > 4*o[2] + 10 for o in out):
            out.append((s, y0, sp))
        if len(out) == n: break
    return sorted(out, key=lambda t: t[1])
if __name__ == '__main__':
    p = sys.argv[1]; n = int(sys.argv[2])
    im = Image.open(p).convert('L'); a = (np.asarray(im) < 150).astype(float)
    W = a.shape[1]
    for x0 in range(150, W-300, 400):
        print(x0, [(round(s,2), y0, sp) for s, y0, sp in find_staves(a, x0, x0+300, n)])
