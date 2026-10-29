import numpy as np, cv2
def lines_track2(bw,t0,t1,deg=2):
    k=cv2.getStructuringElement(cv2.MORPH_RECT,(45,1))
    lm=cv2.morphologyEx(bw,cv2.MORPH_OPEN,k)
    H,W=bw.shape
    rows=[];xs=[]
    for x in range(W):
        col=lm[max(0,t0-25):t1+26,x]>0
        idx=np.where(col)[0]
        if len(idx)==0: continue
        groups=np.split(idx,np.where(np.diff(idx)>1)[0]+1)
        cs=[g.mean()+max(0,t0-25) for g in groups if 3<=len(g)<=11]
        if len(cs)==5:
            d=np.diff(cs)
            if d.min()>16 and d.max()<27: rows.append(cs); xs.append(x)
    rows=np.array(rows); xs=np.array(xs)
    fits=[]
    for j in range(5):
        p=np.polyfit(xs,rows[:,j],deg)
        r=rows[:,j]-np.polyval(p,xs); k2=abs(r)<2.5*r.std()+0.5
        p=np.polyfit(xs[k2],rows[k2,j],deg); fits.append(p)
    return fits,len(xs)
