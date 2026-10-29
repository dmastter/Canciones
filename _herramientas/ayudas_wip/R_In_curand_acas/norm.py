import numpy as np
from PIL import Image, ImageFilter
import scipy.ndimage as nd
def norm(i):
    im=np.asarray(Image.open(f'ds{i}.png').convert('L')).astype(float)
    bg=nd.gaussian_filter(nd.maximum_filter(im,size=25),15)
    n=np.clip(im/bg,0,1)
    return n
if __name__=='__main__':
    for i in range(1,7):
        n=norm(i)
        Image.fromarray((n*255).astype('uint8')).save(f'nn{i}.png')
        a=n<0.8
        # horizontal line score: fraction of dark pixels in row over x 300..1850, smoothed
        p=a[:,300:1850].mean(axis=1)
        pk=[y for y in range(1,len(p)-1) if p[y]>0.25 and p[y]>=p[y-1] and p[y]>=p[y+1]]
        print(i,pk)
