import cv2
import numpy as np
import math

print("請輸入要比對的照片數量")
number=input()
filename=[]
a=0
for a in range(int(number)):
    print("請輸入檔案名稱")
    temp=input()
    filename.append(temp)

img=cv2.imread(filename[0],cv2.IMREAD_GRAYSCALE)

width = img.shape[1]
height = img.shape[0]
def check (level, image , shift):
    divide=pow(2,level)
    new = cv2.resize(img, (int(width / divide), int(height / divide)))
    width2 = image.shape[1]
    height2 = image.shape[0]
    new2= cv2.resize(image , (int(width2 / divide), int(height2 / divide)))

    mean, std = cv2.meanStdDev(new)
    mean2, std2 = cv2.meanStdDev(new2)
    new[np.where(new < mean - 20)] = 0
    new[np.where(new >= mean + 20)] = 255
    new[np.where(abs(new - 127.5) != 127.5)] = 0
    new2[np.where(new2 < mean2 - 20)] = 0
    new2[np.where(new2 >= mean2 + 20)] = 255
    new2[np.where(abs(new2 - 127.5) != 127.5)] = 0


    diff=0
    if(shift==0):
        for x in range((int(height / divide)-1)):#4160
            for y in range((int(width / divide)-1)):#6240
                if(new[x][y]!=new2[x][y]):
                    diff=diff+1
    elif(shift==1):#左上
        for x in range(int(height / divide)-2):
            for y in range(int(width / divide)-2):
                if(new[x][y]!=new2[x+1][y+1]):
                    diff=diff+1
    elif(shift==2):#上
        for x in range(int(height / divide)-2):
            for y in range(int(width / divide)-1):
                if(new[x][y]!=new2[x+1][y]):
                    diff=diff+1
    elif(shift==3):#右上
        for x in range(0,int(height / divide)-2):
            for y in range(1,int(width / divide)-1):
                if(new[x][y]!=new2[x+1][y-1]):
                    diff=diff+1
    elif(shift==4):#左
        for x in range(int(height / divide)-1):
            for y in range(int(width / divide)-2):
                if(new[x][y]!=new2[x][y+1]):
                    diff=diff+1
    elif(shift==5):#右
        for x in range(int(height / divide)-1):
            for y in range(1,int(width / divide)-1):
                if(new[x][y]!=new2[x][y-1]):
                    diff=diff+1
    elif(shift==6):#左下
        for x in range(1,int(height / divide)-1):
            for y in range(int(width / divide)-2):
                if(new[x][y]!=new2[x-1][y+1]):
                    diff=diff+1
    elif(shift==7):#下
        for x in range(1,int(height / divide)-1):
            for y in range(int(width / divide)-1):
                if(new[x][y]!=new2[x-1][y]):
                    diff=diff+1
    elif(shift==8):#右下
        for x in range(1,int(height / divide)-1):
            for y in range(1,int(width / divide)-1):
                if(new[x][y]!=new2[x-1][y-1]):
                    diff=diff+1
    return diff
def translate(image, x, y):
    M = np.float32([[1, 0, x], [0, 1, y]])
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return shifted

def MTB(level, image):
    if(level==10):
        diff = 6240*4160
        ans = 0
        for shift in range(9):
            temp = check(level, image, shift)
            if ( temp < diff ) :
                diff = temp
                ans = shift
        if(ans==0):
            return 0, 0, 0, 0, 0, 0, 0, 0
        elif(ans==1):
            return 1, 0, 0, 0, 0, 0, 0, 0
        elif(ans==2):
            return 0, 1, 0, 0, 0, 0, 0, 0
        elif(ans==3):
            return 0, 0, 1, 0, 0, 0, 0, 0
        elif(ans==4):
            return 0, 0, 0, 1, 0, 0, 0, 0
        elif(ans==5):
            return 0, 0, 0, 0, 1, 0, 0, 0
        elif(ans==6):
            return 0, 0, 0, 0, 0, 1, 0, 0
        elif(ans==7):
            return 0, 0, 0, 0, 0, 0, 1, 0
        elif(ans==8):
            return 0, 0, 0, 0, 0, 0, 0, 1
    else:
        a, b, c, d, e, f, g, h = MTB(level+1, image)
        a=2*a
        b=2*b
        c=2*c
        d=2*d
        e=2*e
        f=2*f
        g=2*g
        h=2*h
        x=0-a+c-d+e-f+h
        y=0-a-b-c+f+g+h
        now=translate(image, x, y)
        diff = 6240 * 4160
        ans = 0
        for shift in range(9):
            temp = check(level, now, shift)
            if (temp < diff):
                diff = temp
                ans = shift
        if (ans == 0):
            return a, b, c, d, e, f, g, h
        elif (ans == 1):
            return a+1, b, c, d, e, f, g, h
        elif (ans == 2):
            return a, b+1, c, d, e, f, g, h
        elif (ans == 3):
            return a, b, c+1, d, e, f, g, h
        elif (ans == 4):
            return a, b, c, d+1, e, f, g, h
        elif (ans == 5):
            return a, b, c, d, e+1, f, g, h
        elif (ans == 6):
            return a, b, c, d, e, f+1, g, h
        elif (ans == 7):
            return a, b, c, d, e, f, g+1, h
        elif (ans == 8):
            return a, b, c, d, e, f, g, h+1



for count in range(1,int(number)):
    temp=cv2.imread(filename[count],cv2.IMREAD_GRAYSCALE)
    a, b, c, d, e, f, g, h = MTB(0, temp)
    x = 0 - a + c - d + e - f + h
    y = 0 - a - b - c + f + g + h
    now=cv2.imread(filename[count])
    now = translate(now, x, y)
    filename[count] = filename[count].replace(".jpg", "afterMTB.jpg")
    cv2.imwrite(filename[count], now)







