import numpy as np
import cv2
import struct
import math
from scipy.ndimage import gaussian_filter

def imageWarping(filename,focalLength,number):

    image=[]
    for a in range(int(number)):
        image.append(cv2.imread(filename[a]))
    warped=[]
    for a in range(int(number)):
        temp=cv2.imread(filename[a])
        f=float(focalLength[a])
        middlex=int(image[a].shape[0]/2)
        middley=int(image[a].shape[1]/2)
        """inverse x=tan(x'/f)*f y=y'/f*sqrt(x^2+f^2)"""
        """x and y相反了嗚嗚"""
        for hor in range(image[a].shape[0]):
            for ver in range(image[a].shape[1]):
                temp[hor][ver]=[0,0,0]
                x_1=hor-middlex
                y_1=ver-middley
                y=f*math.tan(float(y_1)/float(f))
                x=middlex+float(x_1)/f*math.sqrt(y*y+f*f)
                y=y+middley
                if((x>=0 and x<image[a].shape[0]-1)and(y>=0 and y<image[a].shape[1]-1)):
                    floorx=int(math.floor(x))
                    floory =int(math.floor(y))
                    ceilx=floorx+1
                    ceily=floory+1
                    r=image[a][floorx][floory][0]*(float(ceilx)-x)*(float(ceily)-y)+image[a][ceilx][ceily][0]*(x-float(floorx))*(y-float(floory))+image[a][floorx][ceily][0]*(float(ceilx)-x)*(y-float(floory))+image[a][ceilx][floory][0]*(x-float(floorx))*(float(ceily)-y)
                    g=image[a][floorx][floory][1]*(float(ceilx)-x)*(float(ceily)-y)+image[a][ceilx][ceily][1]*(x-float(floorx))*(y-float(floory))+image[a][floorx][ceily][1]*(float(ceilx)-x)*(y-float(floory))+image[a][ceilx][floory][1]*(x-float(floorx))*(float(ceily)-y)
                    b=image[a][floorx][floory][2]*(float(ceilx)-x)*(float(ceily)-y)+image[a][ceilx][ceily][2]*(x-float(floorx))*(y-float(floory))+image[a][floorx][ceily][2]*(float(ceilx)-x)*(y-float(floory))+image[a][ceilx][floory][2]*(x-float(floorx))*(float(ceily)-y)
                    temp[hor][ver]=[int(r),int(g),int(b)]
        """for now in range(500):
            x=description[a][now][1]-middley
            y=description[a][now][0]-middlex
            description[a][now][1]=float(f)*math.atan(x/float(f))
            description[a][now][0]=f*y/math.sqrt(x*x+f*f)
            description[a][now][1]=middley+int(description[a][now][1])
            description[a][now][0]=middlex+int(description[a][now][0])"""

        warped.append(temp)
    for a in range(int(number)):
        filename[a] = filename[a].replace(".jpg", "AW.jpg")
        cv2.imwrite(filename[a], warped[a])
    """for now in range(500):
        temp[description[a][now][0]][description[a][now][1]]=[255,255,255]
        warped[0][description[a][now][0]][description[a][now][1]][0]=255
        warped[0][description[a][now][0]][description[a][now][1]][1]=255
        warped[0][description[a][now][0]][description[a][now][1]][2]= 255"""


"""MAIN"""
print("請輸入要投影的照片數量")
number=input()
filename=[]
focalLength=[]
a=0
for a in range(int(number)):
    print("請輸入檔案名稱, 照片focalLength")
    temp1=input()
    filename.append(temp1)
    temp2=input()
    focalLength.append(temp2)

imageWarping(filename,focalLength,number)




"""EndOfMAIN"""








"""EndOfMAIN"""














