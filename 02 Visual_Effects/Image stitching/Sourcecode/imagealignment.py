import numpy as np
import cv2
import math
x=[]

def translate(image, x, y):
    M = np.float32([[1, 0, x], [0, 1, y]])
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return shifted


def imageAlignment(img1, img2,first):
    newx = img2.shape[0] + max(x[first][1],0)
    newy = img2.shape[1] + x[first][0]

    if(x[first][1]<0):
        img2 = translate(img2, 0, x[first][1])


    # 按下任意鍵則關閉所有視窗
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    mix=np.zeros((int(newx),int(newy),3), np.uint8)
    for a in range(img1.shape[0]):
        for b in range(img1.shape[1]):
            mix[a][b]=img1[a][b]
    for a in range(img2.shape[0]):
        for b in range(img2.shape[1]):
            if(a<=img1.shape[0]-x[first][1] and b <= img1.shape[1]-x[first][0]):
                mix[a + x[first][1]][b + x[first][0]]=mix[a + x[first][1]][b + x[first][0]]*(1-b/(img1.shape[1]-x[first][0]))+img2[a][b]*(b/(img1.shape[1]-x[first][0]))
            else:
                mix[a+x[first][1]][b+x[first][0]]=img2[a][b]
    return mix





print("請輸入要合併的照片數量")
number=input()
filename=[]
focalLength=[]
a=0
for a in range(int(number)):
    print("請輸入檔案名稱")
    temp1=input()
    filename.append(temp1)
for a in range(int(number)-1):
    print("請依序輸入dx, dy")
    temp1=input()
    temp2=input()
    x.append([int(temp1),int(temp2)])
mix=cv2.imread(filename[int(number)-1])
a=int(number)-2
while a >=0:
    img=cv2.imread(filename[a])
    mix=imageAlignment(img,mix,a)
    a=a-1
cv2.imwrite("panorama.jpg",mix)


"""
x.append([205,13])
x.append([119,-2])
x.append([256,8])
x.append([205,7])
x.append([181,5])
x.append([216,6])"""