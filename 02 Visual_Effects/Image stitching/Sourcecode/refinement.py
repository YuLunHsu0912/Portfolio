import numpy as np
import cv2
import math
import numpy as np


print("input one of photos stitched")
before=input()
print("input stitched photo")
after=input()

img1=cv2.imread(before)
img2=cv2.imread(after)
diff=img2.shape[0]-img1.shape[0]

new=np.zeros((img2.shape[0],img2.shape[1],3), np.uint8)

m=float(diff)/float(img2.shape[1])

for a in range(img2.shape[0]):
    for b in range(img2.shape[1]):
        new[a][b]=img2[int(a-m*a)][b]

remove=int(img2.shape[0]*0.05)

new2=np.zeros((img2.shape[0]-2*remove,img2.shape[1],3), np.uint8)
for a in range(new2.shape[0]):
    for b in range(new2.shape[1]):
        new2[a][b]=new[a+remove][b]

cv2.imwrite("panoramaAR.jpg",new2)
