import sys
from batch2 import *
# uso: zz.py sys nst sel clefs x0 y0 x1 y1 z out
sysn=sys.argv[1]; nst=int(sys.argv[2]); sel=[int(c) for c in sys.argv[3]]; clefs=sys.argv[4]
x0,y0,x1,y1=map(int,sys.argv[5:9]); z=float(sys.argv[9]); out=sys.argv[10]
models=sysmodel(f'crops/{sysn}.png',nst)
render(f'crops/{sysn}.png',models,sel,clefs,(x0,y0,x1,y1),z,out)
