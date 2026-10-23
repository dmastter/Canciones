import sys, numpy as np
from PIL import Image
from batch2 import *
def run(sysn,nst,layout,z=2.0):
    path=f'crops/{sysn}.png'
    models=sysmodel(path,nst)
    H=Image.open(path).height; W=Image.open(path).width
    xm=W/2
    def top(j): return np.polyval(models[j][0],xm)
    def bot_(j): return np.polyval(models[j][4],xm)
    wins=[(0,700),(600,1300),(1200,1900),(1800,W)]
    if nst==4:
        v=(max(0,int(top(0)-80)),int(bot_(1)+70)); p=(int(top(2)-90),min(H,int(bot_(3)+120)))
        print(sysn,'v',v,'p',p)
        for i,(a,b) in enumerate(wins):
            render(path,models,[0,1],layout[:2],(a,v[0],b,v[1]),z,f'w/{sysn}_v{i}.png')
            render(path,models,[2,3],layout[2:],(a,p[0],b,p[1]),z,f'w/{sysn}_p{i}.png')
    else:
        p=(max(0,int(top(0)-90)),min(H,int(bot_(1)+120)))
        print(sysn,'p',p)
        for i,(a,b) in enumerate(wins):
            render(path,models,[0,1],layout,(a,p[0],b,p[1]),z,f'w/{sysn}_p{i}.png')
if __name__=='__main__':
    run(sys.argv[1],int(sys.argv[2]),sys.argv[3],float(sys.argv[4]) if len(sys.argv)>4 else 2.0)
