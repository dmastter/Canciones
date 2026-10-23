import numpy as np, cv2
from PIL import Image
from scipy import ndimage as ndi
from heads import BANDS, SC
from lt2 import lines_track2
def dets(s,thr=5.0,pad=55):
    im=Image.open('crops/d%d.png'%s).convert('L'); g=np.asarray(im)
    _,bw=cv2.threshold(g,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    out={}
    for idx,clef in ((0,'T'),(1,'B')):
        t0,t1=BANDS[s][idx]
        fits,_=lines_track2(bw,t0,t1)
        ker=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,11))
        op=cv2.morphologyEx(bw,cv2.MORPH_OPEN,ker)
        band=np.zeros_like(op); band[t0-pad:t1+pad,:]=op[t0-pad:t1+pad,:]
        dist=cv2.distanceTransform(band,cv2.DIST_L2,5)
        mx=ndi.maximum_filter(dist,size=11)
        pk=(dist==mx)&(dist>=thr)
        lab,n=ndi.label(pk); cs=ndi.center_of_mass(pk,lab,range(1,n+1))
        L=[]
        for (cy,cx) in sorted(cs,key=lambda c:c[1]):
            bot=np.polyval(fits[4],cx); sp=(bot-np.polyval(fits[0],cx))/4
            pos=(bot-cy)/(sp/2); k=int(round(pos))
            L.append((round(cx),k,round(pos-k,1)))
        out[clef]=L
    return out
if __name__=='__main__':
    import sys
    a=dets(int(sys.argv[1])); b=dets(int(sys.argv[2]))
    for clef in 'TB':
        print(clef)
        for x,k,o in a[clef]:
            m=[(bx,bk,bo) for bx,bk,bo in b[clef] if abs(bx-x)<25]
            flag='' if any(bk==k for bx,bk,bo in m) else '  <<< DIFF'
            print(x,k,o,'|',m,flag)
