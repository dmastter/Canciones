import sys, numpy as np
from PIL import Image
def clusters(rows):
    g=[];cur=[]
    for r in rows:
        if cur and r-cur[-1]>2: g.append(cur);cur=[]
        cur.append(r)
    if cur:g.append(cur)
    return [sum(c)/len(c) for c in g]
for s,n in [(1,1),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2)]:
    im=Image.open(f'd/p1_s{s}.png').convert('L'); a=np.asarray(im)<150; H,W=a.shape
    wins=[]
    for xc in range(120,2400,30):
        fr=a[:,xc-50:xc+50].mean(axis=1); wins.append((xc,clusters(np.where(fr>0.6)[0])))
    good=[c for x,c in wins if len(c)==5*n]
    ref=np.median(np.array(good),axis=0)
    out=[]
    for k in range(n):
        top=int(ref[k*5])+4; bot=int(ref[k*5+4])-4
        col=a[top:bot,:].mean(axis=0)
        xs=np.where(col>0.92)[0]
        grp=[];cur=[]
        for x in xs:
            if cur and x-cur[-1]>3: grp.append(cur);cur=[]
            cur.append(x)
        if cur:grp.append(cur)
        out.append([round(sum(g)/len(g)) for g in grp])
    print(s,[int(r) for r in ref[[0,4]]] , out)
