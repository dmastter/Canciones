import numpy as np, sys
from PIL import Image
for i in range(1,7):
    im=Image.open(f'sys{i}.png').convert('L')
    best=None
    for ang in np.arange(-3,3.01,0.1):
        r=im.rotate(ang,resample=Image.BICUBIC,fillcolor=255)
        a=np.asarray(r)<140
        p=a.sum(axis=1).astype(float)
        s=(np.diff(p)**2).sum()
        if best is None or s>best[0]: best=(s,ang)
    print(i,best[1])
    im.rotate(best[1],resample=Image.BICUBIC,fillcolor=255).convert('RGB').save(f'ds{i}.png')
