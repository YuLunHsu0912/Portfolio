import numpy as np
import cv2
import struct
import math
import random
from scipy.ndimage import gaussian_filter
def gradient_x(image):
    gradient=np.zeros((image.shape[0],image.shape[1]),dtype=float)
    for a in range(image.shape[0]):
        for b in range(image.shape[1]-1):
            gradient[a][b]=float(image[a][b+1])-float(image[a][b])
    return gradient
def gradient_y(image):
    gradient = np.zeros((image.shape[0], image.shape[1]), dtype=float)
    for a in range(image.shape[0]-1):
        for b in range(image.shape[1] ):
            gradient[a][b] = float(image[a+1][b ]) - float(image[a][b])
    return gradient
def featureDetection(filename,number):
    """pyramid做到三層"""
    image1=[]
    image2=[]
    image3=[]
    for a in range(int(number)):
        image1.append(cv2.imread(filename[a],cv2.IMREAD_GRAYSCALE))
        image2.append(cv2.resize(image1[a], (int(image1[a].shape[1] / 2), int(image1[a].shape[0] / 2))))
        image3.append(cv2.resize(image1[a], (int(image1[a].shape[1] / 4), int(image1[a].shape[0] / 4))))
        image2[a] = gaussian_filter(image2[a], sigma=1)
        image3[a] = gaussian_filter(image3[a], sigma=1)
        """gaussian filter"""
    image=[]
    image.append(image1)
    image.append(image2)
    image.append(image3)
    """pyramid做到三層"""
    """compute cornerResponse"""
    Response1=[]
    Response2=[]
    Response3=[]
    """gradient"""
    for a in range(int(number)):
        """照片數"""
        for b in range(3):
            """pyramid為3"""
            Ix = np.zeros((image[b][a].shape[0], image[b][a].shape[1]), dtype=float)
            Iy=  np.zeros((image[b][a].shape[0],image[b][a].shape[1]),dtype=float)

            Ix = gradient_x(image[b][a])
            Ix = gaussian_filter(Ix, sigma=1.0)
            Iy = gradient_y(image[b][a])
            Iy = gaussian_filter(Iy, sigma=1.0)
            Ix2 = np.zeros((image[b][a].shape[0], image[b][a].shape[1]), dtype=float)
            Iy2 = np.zeros((image[b][a].shape[0], image[b][a].shape[1]), dtype=float)
            IxIy = np.zeros((image[b][a].shape[0], image[b][a].shape[1]), dtype=float)
            for x in range(image[b][a].shape[0]):
                for y in range(image[b][a].shape[1]):
                    Ix2[x][y] = float(Ix[x][y]) * float(Ix[x][y])
                    Iy2[x][y] = float(Iy[x][y]) * float(Iy[x][y])
                    IxIy[x][y] = float(Ix[x][y]) * float(Iy[x][y])
            Ix2 = gaussian_filter(Ix2, sigma=1.5)
            Iy2 = gaussian_filter(Iy2, sigma=1.5)
            IxIy = gaussian_filter(IxIy, sigma=1.5)
            Temp=np.zeros((image[b][a].shape[0], image[b][a].shape[1]), dtype=float)
            for x in range(image[b][a].shape[0]):
                for y in range(image[b][a].shape[1]):
                    if(Ix2[x][y]+Iy2[x][y]==0):
                        Temp[x][y]=0.0
                    else:
                        Temp[x][y]=(Ix2[x][y]*Iy2[x][y]-IxIy[x][y]*IxIy[x][y])/(Ix2[x][y]+Iy2[x][y])
            if(b==0):
                Response1.append(Temp)
            elif(b==1):
                Response2.append(Temp)
            elif(b==2):
                Response3.append(Temp)

    Response=[]
    Response.append(Response1)
    Response.append(Response2)
    Response.append(Response3)
    import plotly.express as px
    fig = px.imshow(Response[0][0])
    fig.show()

    """compute cornerResponse"""
    """findfeatures, threshold=10.0"""
    feature1=[]
    feature2=[]
    feature3=[]
    for a in range(int(number)):
        for b in range(3):
            temp=np.zeros((Response[b][a].shape[0], Response[b][a].shape[1]),dtype=bool)
            for x in range(Response[b][a].shape[0]):
                for y in range(image[b][a].shape[1]):
                    if(Response[b][a][x][y]>10.0):
                        temp[x][y]=True
                    for r_1 in range(-1,2):
                        for r_2 in range(-1,2):
                            if(x+r_1>=0 and x+r_1<image[b][a].shape[0]):
                                if(y+r_2>=0 and y+r_2<image[b][a].shape[1]):
                                    if(Response[b][a][x+r_1][y+r_2]>Response[b][a][x][y]):
                                         temp[x][y]=False

            if (b == 0):
                feature1.append(temp)
            elif (b == 1):
                feature2.append(temp)
            elif (b == 2):
                feature3.append(temp)
    feature = []
    feature.append(feature1)
    feature.append(feature2)
    feature.append(feature3)

    """投影所有層的feature到原始平面"""
    Final=[]
    size=np.zeros(int(number),dtype=int)
    map=np.zeros((feature[0][a].shape[0],feature[0][a].shape[1]),dtype=bool)
    for a in range(int(number)):
        FinalTemp=[]
        for x in range(feature[0][a].shape[0]):
            for y in range(feature[0][a].shape[1]):
                if(feature[0][a][x][y]==True):
                    temp=[x,y,0,Response[0][a][x][y]]
                    FinalTemp.append(temp)
                    size[a]=size[a]+1
                    map[x][y]=True
        for x in range(feature[1][a].shape[0]):
            for y in range(feature[1][a].shape[1]):
                if(feature[1][a][x][y]==True and feature[0][a][2*x][2*y]!=True):
                    temp=[2*x,2*y,1,Response[1][a][x][y]]
                    FinalTemp.append(temp)
                    size[a] = size[a] + 1
                    map[x*2][y*2] = True
        for x in range(feature[2][a].shape[0]):
            for y in range(feature[2][a].shape[1]):
                if(feature[2][a][x][y]==True and (feature[1][a][2*x][2*y]!=True and feature[0][a][4*x][4*y]!=True)):
                    temp=[4*x,4*y,2,Response[2][a][x][y]]
                    FinalTemp.append(temp)
                    size[a] = size[a] + 1
                    map[x * 4][y * 4] = True
        Final.append(FinalTemp)
        """總共有number張圖"""
    for a in range(int(number)):
        for first in range(size[a]-1):
            for second in range(first+1,size[a]):
                if(Final[a][first][3]<Final[a][second][3]):
                    temp=np.copy(Final[a][second])
                    Final[a][second]=np.copy(Final[a][first])
                    Final[a][first]=np.copy(temp)

    """print before nonmaximal"""
    intermediate=np.zeros((feature[0][a].shape[0],feature[0][a].shape[1]),dtype=int)
    img=cv2.imread(filename[0])
    for a in range(size[0]):
        cv2.circle(img,(int(Final[0][a][1]),int(Final[0][a][0])),1,(0,255,0),4)
    cv2.imwrite('intermediate1.jpg', img)

    """nonmaximal suppression"""
    FiveHundred=[]
    for a in range(int(number)):
        Yes = np.ones((size[a]), dtype=bool)
        featureNum=500
        current=size[a]
        r=3
        while(current>featureNum):
            for first in range(size[a]):
                """fisrt為現在是選定的點"""
                for second in range(size[a]):
                    """second是現在要取消的點"""
                    if(first!=second):
                        if(Yes[first]==True and Yes[second]==True):
                            if(float((Final[a][first][0]-Final[a][second][0])*(Final[a][first][0]-Final[a][second][0])+(Final[a][first][1]-Final[a][second][1])*(Final[a][first][1]-Final[a][second][1]))<=float(r*r)):
                                if(Final[a][first][3]>Final[a][second][3]):
                                    Yes[second]=False
                                else :
                                    Yes[fisrt] = False
                                current=current-1
                    if(current<=featureNum):
                        break
                if(current<=featureNum):
                    break
            r=r+1
            if(r==max(feature[0][a].shape[0],feature[0][a].shape[1])):
                break

        FiveHundred.append(Yes)
    """print after intermediate"""
    intermediate2 = np.zeros((feature[0][a].shape[0], feature[0][a].shape[1]), dtype=int)
    img2 = cv2.imread(filename[0])
    for a in range(size[0]):
        if(FiveHundred[0][a]==True):
            cv2.circle(img2, (int(Final[0][a][1]), int(Final[0][a][0])), 1, (0, 255, 255), 4)
    cv2.imwrite('intermediate2.jpg', img2)
    """nonmaximal suppression"""


    """Orientation assignment and descriptor"""
    description=[]
    for a in range(int(number)):
        """第0層"""
        featurenumber=0
        descriptiontemp=[]
        level0Ix= gradient_x(image[0][a])
        level0Iy= gradient_y(image[0][a])
        level0Ix= gaussian_filter(level0Ix, sigma=4.5)
        level0Iy = gaussian_filter(level0Iy, sigma=4.5)
        for x in range(size[a]):
            if(FiveHundred[a][x]==True):
                featurenumber=featurenumber+1
                nowx=int(Final[a][x][0])
                nowy=int(Final[a][x][1])
                distance = math.sqrt(level0Ix[nowx][nowy] * level0Ix[nowx][nowy] + level0Iy[nowx][nowy] * level0Iy[nowx][nowy])
                cos = level0Ix[nowx][nowy] / distance
                sin = level0Iy[nowx][nowy] / distance
                window=np.zeros((40,40),dtype=float)
                for u in range(-20,20):
                    for v in range(-20,20):
                        realu=nowx+int(cos*float(u)-sin*float(v))
                        realv=nowy+int(sin*float(u)+cos*float(v))
                        if((realu>=0 and realv>=0)and(realu<image[0][a].shape[0] and realv<image[0][a].shape[1])):

                            window[u+20][v+20]=image[0][a][realu][realv]
                        else:
                            window[u+20][v+20]=-1
                des = np.zeros((8, 8), dtype=float)
                for u in range(8):
                    for v in range(8):
                        count=0
                        sum=0.0
                        for hor in range(5):
                            for ver in range(5):
                               if(window[u*5+hor][v*5+ver]!=-1):
                                    sum=sum+window[u*5+hor][v*5+ver]
                                    count=count+1
                        if(count!=0):
                            des[u][v]=sum/float(count)
                        else:
                            des[u][v]=-100
                counting=0
                mean=0.0
                for u in range(8):
                    for v in range(8):
                        if(des[u][v]!=-100):
                            mean+=des[u][v]
                            counting=counting+1
                if(counting!=0):
                    mean=mean/float(counting)
                std=0.0
                for u in range(8):
                    for v in range(8):
                        std=std+math.pow((des[u][v]-mean),2)
                if (counting != 0):
                    std = std / float(counting)
                for u in range(8):
                    for v in range(8):
                        if (des[u][v] != -100):
                            des[u][v]=(des[u][v]-mean)/std

                temp=[nowx,nowy,Final[a][x][2],Final[a][x][3],cos,sin,des]
                descriptiontemp.append(temp)
        print(featurenumber)
        description.append(descriptiontemp)
        """Orientation assignment and descriptor"""
    """end"""
    return description, size



def featureMatching(filename,description,number):
    matchedposterior=[]
    for a in range(int(number)-1):
        match=[]
        for ant in range(500):
            best=0
            distance=10000000.0
            for post in range(500):
                temp=0.0
                for c in range(64):
                    temp=temp+math.pow((float(description[a][ant][6][int(c/8)][int(c%8)])-float(description[a+1][post][6][int(c/8)][int(c%8)])),2)
                temp=math.sqrt(temp)
                if(temp<distance):
                    best=post
                    distance=temp
            if(distance>0.7):
                best=-1
            match.append(best)
        matchedposterior.append(match)
    for a in range(int(number)-1):
        print("第",a+1,"張照片與第",a+2,"張照片的對應關係")
        for b in range(500):
            print(matchedposterior[a][b])





"""MAIN"""
print("請輸入要偵測的照片數量")
number=input()
filename=[]
a=0
for a in range(int(number)):
    print("請輸入檔案名稱")
    temp1=input()
    filename.append(temp1)


description,size=featureDetection(filename,number)
for a in range(int(number)):
    print("第",a+1,"照片的特徵點")
    print("x=")
    for b in range(500):

        print(description[a][b][0])
    print("y=")
    for b in range(500):

        print( description[a][b][1])
featureMatching(filename,description,number)

"""EndOfMAIN"""














