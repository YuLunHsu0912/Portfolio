import numpy as np
import cv2
import math
import random
description=[]
anterior=[]
def imageMatching(filename,number,focalLength):
    inliers = []
    for a in range(int(number)):
        image=cv2.imread(filename[a])
        f=float(focalLength[a])
        middlex=int(image.shape[0]/2)
        middley=int(image.shape[1]/2)

        for now in range(500):
            x=description[a][now][1]-middley
            y=description[a][now][0]-middlex
            description[a][now][1]=float(f)*math.atan(x/float(f))
            description[a][now][0]=f*y/math.sqrt(x*x+f*f)
            description[a][now][1]=middley+int(description[a][now][1])
            description[a][now][0]=middlex+int(description[a][now][0])
    for a in range(int(number)-1):
        inlier = np.zeros((500, 1))
        best = np.zeros((4, 1), dtype=float)
        bestinlier = 0
        for k in range(20):
            now1 = random.randint(0, 499)
            while (anterior[a][now1] == -1 ):
                now1 = random.randint(0, 499)

            post1 = anterior[a][now1]
            dx=description[a+1][post1][1]-description[a][now1][1]
            dy=description[a+1][post1][0]-description[a][now1][0]
            count = 0
            for temp in range(500):
                if (anterior[a][temp] != -1):
                    x1 = description[a][temp][1]
                    y1 = description[a][temp][0]
                    post = anterior[a][temp]
                    truex = description[a+1][post][1]
                    truey = description[a+1][post][0]
                    nowx = x1 +dx
                    nowy = y1 + dy
                    if (math.pow((nowx - truex), 2) < 30 and math.pow((nowy - truey), 2) < 30):
                        count = count + 1
            if (count > bestinlier):
                bestinlier = count
                best = np.copy([dx,dy])
        for temp in range(500):
            if (anterior[a][temp] != -1):
                x1 = description[a][temp][1]
                y1 = description[a][temp][0]
                post = anterior[a][temp]
                truex = description[a+1][post][1]
                truey = description[a+1][post][0]
                nowx = x1 +best[0]
                nowy = y1 +best[1]
                if (math.pow((nowx - truex), 2) < 30 and math.pow((nowy - truey), 2) < 30):
                    inlier[temp] = 1
        inliers.append(inlier)

    for a in range(int(number)):
        f=float(focalLength[a])
        img=cv2.imread(filename[a])
        middlex = int(img.shape[0] / 2)
        middley = int(img.shape[1] / 2)
        for now in range(500):
            x = description[a][now][1] - middley
            y = description[a][now][0] - middlex
            description[a][now][1] = int(float(f) * math.atan(x / float(f)))
            description[a][now][0] = int(f * y / math.sqrt(x * x + f * f))
            description[a][now][1] = middley + int(description[a][now][1])
            description[a][now][0] = middlex + int(description[a][now][0])

    for a in range(int(number) - 1):
        count=0
        dx=0.0
        dy=0.0
        for b in range(500):
            if(inliers[a][b]==1):
                dx=dx+description[a + 1][anterior[a][b]][1]-description[a][b][1]
                dy=dy+description[a + 1][anterior[a][b]][0]-description[a][b][0]
                count=count+1
        dx=dx/float(count)
        dy=dy/float(count)
        print(-dx,-dy)


    for now in range(int(number) - 1):
        img1 = cv2.imread(filename[now], cv2.IMREAD_COLOR)
        img2 = cv2.imread(filename[now+1], cv2.IMREAD_COLOR)
        htitch = np.hstack((img1, img2))
        for a in range(500):
            if (inliers[now][a] == 1):
                post = anterior[now][a]
                cv2.line(htitch, (description[now][a][1], description[now][a][0]),
                             (description[now+1][post][1] + img1.shape[1], description[now+1][post][0]), (255, 255, 255))
                cv2.circle(htitch,(description[now][a][1], description[now][a][0]),1, (0, 255, 255),4)
                cv2.circle(htitch, (description[now+1][post][1] + img1.shape[1], description[now+1][post][0]),1, (0, 255, 255), 4)

        filename[now] = filename[now].replace(".jpg", "AM.jpg")
        cv2.imwrite(filename[now], htitch)




print("請輸入要偵測的照片數量")
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
for a in range(int(number)):
    print("請輸入第",a+1,"個檔案的特徵點座標")
    temp2=[]
    temp=np.zeros([500,2])
    print("請輸入x座標")
    for b in range(500):
        x=input()
        temp[b][0]=int(x)
    print("請輸入y座標")
    for b in range(500):
        y = input()
        temp[b][1] = int(y)
    for b in range(500):
        temp2.append([temp[b][0],temp[b][1]])
    description.append(temp2)
for a in range(int(number)-1):
    print("請輸入第",a+1,"個檔案與第",a+2,"個檔案對應的特徵點")
    temp=[]
    for b in range(500):
        c=input()
        temp.append(int(c))
    anterior.append(temp)

imageMatching(filename,number,focalLength)

"""img=cv2.imread("7.jpg")
img=cv2.resize(img, (int(img.shape[1] / 10), int(img.shape[0] / 10)))
cv2.imwrite("7small.jpg",img)"""




