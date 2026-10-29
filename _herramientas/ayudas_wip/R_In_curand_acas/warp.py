import numpy as np, sys, json
from PIL import Image
import scipy.ndimage as nd
from norm import norm
def staff_offsets(n, st, xs, win=40, rng=14):
    dark=1-n
    ox=[];pts=[]
    for x in xs:
        sl=dark[:, max(0,x-win):x+win].mean(axis=1)
        sl=nd.gaussian_filter1d(sl,1.2)
        best=None
        # search global shift d in [-rng,rng] maximizing sum of sl at the 5 lines
        for d in np.arange(-rng,rng+0.1,0.5):
            s=sum(np.interp(y+d,np.arange(len(sl)),sl) for y in st)
            if best is None or s>best[0]: best=(s,d)
        ox.append(x);pts.append(best[1])
    return np.array(ox),np.array(pts)
def make(i, tst, bst):
    n=norm(i); H,W=n.shape
    xs=np.arange(100,W-60,40)
    src=np.asarray(Image.open(f'ds{i}.png').convert('L')).astype(float)
    out=src.copy(); xs_all=np.arange(W)
    mid=int((tst[4]+bst[0])/2)
    for st,(r0,r1) in zip((tst,bst),((0,mid),(mid,H))):
        ox,o=staff_offsets(n,st,xs)
        o=nd.median_filter(o,size=5)
        off=np.interp(xs_all,ox,o); off=nd.gaussian_filter1d(off,25)
        print('offsets',np.round(o[::5],1))
        for x in range(W):
            col=src[r0:r1,x]
            yy=np.arange(r1-r0)+off[x]
            out[r0:r1,x]=np.interp(yy,np.arange(r1-r0),col)
    Image.fromarray(out.astype('uint8')).save(f'wd{i}.png')
if __name__=='__main__':
    make(int(sys.argv[1]),json.loads(sys.argv[2]),json.loads(sys.argv[3]))
