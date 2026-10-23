import sys
from PIL import Image
from heads import BANDS
R={1:[(395,1005),(1005,1320),(1320,1960),(1960,2175)],2:[(405,990),(990,1360),(1360,1930),(1930,2165)]}
def comp(k,sa,ia,sb,ib,out,W=1500):
    parts=[]
    for idx in (0,1):
        for s,i in ((sa,ia),(sb,ib)):
            im=Image.open('crops/d%d.png'%s).convert('L')
            x0,x1=R[s][i]; t0,t1=BANDS[s][idx]
            c=im.crop((x0,t0-45,x1,t1+45)).resize((W,int((t1-t0+90)*W/(x1-x0))),Image.LANCZOS)
            parts.append(c)
    H=sum(p.height for p in parts)+3*5
    o=Image.new('L',(W,H),150); y=0
    for p in parts: o.paste(p,(0,y)); y+=p.height+5
    o.save(out)
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    comp(0,1,a,2,b,'cmp_%d.png'%(a+1))
