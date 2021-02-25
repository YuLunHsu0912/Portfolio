import cv2
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import plotly.express as px
def w(z):
    if(z<=127):
        return z+1
    else :
        return 256-z

print("請輸入7張圖的檔案名：")
filename=input()
img1 = cv2.imread(filename)
filename=input()
img2=cv2.imread(filename)
filename=input()
img3=cv2.imread(filename)
filename=input()
img4=cv2.imread(filename)
filename=input()
img5=cv2.imread(filename)
filename=input()
img6=cv2.imread(filename)
filename=input()
img7=cv2.imread(filename)
(B1, G1, R1) = cv2.split(img1)
(B2, G2, R2) = cv2.split(img2)
(B3, G3, R3) = cv2.split(img3)
(B4, G4, R4) = cv2.split(img4)
(B5, G5, R5) = cv2.split(img5)
(B6, G6, R6) = cv2.split(img6)
(B7, G7, R7) = cv2.split(img7)
#把bgr放入z分別做三條response curve
pixel = 50
picture = 10  # depends on actual
z = np.zeros((400, 7))
z2 =np.zeros((400, 7))
z3 =np.zeros((400, 7))
#長的在後面
x=0
a=0
while x <6240:
    y = 0
    while y<4160:
        z[a][0]=B1[y][x]
        z[a][1] = B2[y][x]
        z[a][2] = B3[y][x]
        z[a][3] = B4[y][x]
        z[a][4] = B5[y][x]
        z[a][5] = B6[y][x]
        z[a][6] = B7[y][x]
        z2[a][0] = G1[y][x]
        z2[a][1] = G2[y][x]
        z2[a][2] = G3[y][x]
        z2[a][3] = G4[y][x]
        z2[a][4] = G5[y][x]
        z2[a][5] = G6[y][x]
        z2[a][6] = G7[y][x]
        z3[a][0] = R1[y][x]
        z3[a][1] = R2[y][x]
        z3[a][2] = R3[y][x]
        z3[a][3] = R4[y][x]
        z3[a][4] = R5[y][x]
        z3[a][5] = R6[y][x]
        z3[a][6] = R7[y][x]
        a=a+1
        y = y + int(4160 / 20)
    x = x + int(6240 / 20)
print("請依序輸入圖片的曝光時間")
temp=np.zeros(7,float)
for a in range(0,7):
    temp[a]=float(input())
B = [math.log(float(temp[0])),math.log(float(temp[1])),math.log(float(temp[2])),math.log(float(temp[3])),math.log(float(temp[4])),math.log(float(temp[5])),math.log(float(temp[6]))]
print("請輸入完成後的檔案名")
file=input()
n = 256
A = np.zeros((z.shape[0]*z.shape[1]+n+1, n+z.shape[0]))
b = np.zeros((A.shape[0], 1))
A2= np.zeros((z.shape[0]*z.shape[1]+n+1, n+z.shape[0]))
b2= np.zeros((A.shape[0], 1))
A3= np.zeros((z.shape[0]*z.shape[1]+n+1, n+z.shape[0]))
b3= np.zeros((A.shape[0], 1))

#python從0開始
k = 0

for i in range(0,z.shape[0]-1):
    for j in range(0,z.shape[1]-1):
        temp=int(w(z[i][j]+1))
        A[k][int(z[i][j])+1] = temp
        A[k][n+i] = -temp
        b[k][0]=temp*B[j]
        #B
        temp = int(w(z2[i][j] + 1))
        A2[k][int(z2[i][j]) + 1] = temp
        A2[k][n + i] = -temp
        b2[k][0] = temp * B[j]
        #G
        temp = int(w(z3[i][j] + 1))
        A3[k][int(z3[i][j]) + 1] = temp
        A3[k][n + i] = -temp
        b3[k][0] = temp * B[j]
        #R
        k=k+1

A[k][128]=1
A2[k][128]=1
A3[k][128]=1
k=k+1

for i in range(0,n-3):
    A[k][i]=w(i+1)
    A[k][i+1]=-2*w(i+1)
    A[k][i+2]=w(i+1)
    A2[k][i] = w(i + 1)
    A2[k][i + 1] = -2 * w(i + 1)
    A2[k][i + 2] = w(i + 1)
    A3[k][i] = w(i + 1)
    A3[k][i + 1] = -2 * w(i + 1)
    A3[k][i + 2] = w(i + 1)
invA=np.linalg.pinv(A)
invA2=np.linalg.pinv(A2)
invA3=np.linalg.pinv(A3)
x = np.dot(invA, b)
x2=np.dot(invA2, b2)
x3=np.dot(invA3, b3)

for a in range(3,253):
    if(x[a]-(x[a-1]+x[a+1]+x[a-2]+x[a+2]+x[a-3]+x[a+3])/6>1):
        x[a]=(x[a-1]+x[a+1]+x[a-2]+x[a+2]+x[a-3]+x[a+3])/6
    if (x2[a] - (x2[a - 1] + x2[a + 1]+x2[a-2]+x2[a+2]+x2[a+3]+x2[a-3]) / 6 > 1):
        x2[a] = (x2[a - 1] + x2[a + 1]+x2[a-2]+x2[a+2]+x2[a+3]+x2[a-3]) / 6
    if (x3[a] - (x3[a - 1] + x3[a + 1]+x3[a-2]+x3[a+2]+x3[a+3]+x3[a-3]) / 6 > 1):
        x3[a] = (x3[a - 1] + x2[a + 1]+x3[a-2]+x3[a+2]+x3[a+3]+x3[a-3]) / 6


FinalB = np.zeros((1040, 1560), dtype=float)
FinalG = np.zeros((1040, 1560), dtype=float)
FinalR = np.zeros((1040, 1560), dtype=float)
b=0
while b < 6240:
    a=0
    while a <4160:
        top = float(w(B1[a][b]) * (x[B1[a][b]] - B[0]) + w(B2[a][b]) * (x[B2[a][b]] - B[1]) + w(B3[a][b]) * (
                    x[B3[a][b]] - B[2]) + w(B4[a][b]) * (x[B4[a][b]] - B[3]) + w(B5[a][b]) * (x[B5[a][b]] - B[4]) + w(
            B6[a][b]) * (x[B6[a][b]] - B[5]) + w(B7[a][b]) * (x[B7[a][b]] - B[6]))
        down = float(w(B1[a][b]) + w(B2[a][b]) + w(B3[a][b]) + w(B4[a][b]) + w(B5[a][b]) + w(B6[a][b]) + w(B7[a][b]))
        FinalB[int(a / 4)][int(b / 4)] = top / down
        a=a+4
    b=b+4
b=0
while b < 6240:
    a=0
    while a <4160:
        top = float(w(G1[a][b]) * (x2[G1[a][b]] - B[0]) + w(G2[a][b]) * (x2[G2[a][b]] - B[1]) + w(G3[a][b]) * (
                    x2[G3[a][b]] - B[2]) + w(G4[a][b]) * (x2[G4[a][b]] - B[3]) + w(G5[a][b]) * (
                                x2[G5[a][b]] - B[4]) + w(G6[a][b]) * (x2[G6[a][b]] - B[5]) + w(G7[a][b]) * (
                                x2[G7[a][b]] - B[6]))
        down = float(w(G1[a][b]) + w(G2[a][b]) + w(G3[a][b]) + w(G4[a][b]) + w(G5[a][b]) + w(G6[a][b]) + w(G7[a][b]))
        FinalG[int(a / 4)][int(b / 4)] = top / down
        a=a+4
    b=b+4

b=0
while b < 6240:
    a=0
    while a <4160:
        top = float(w(R1[a][b]) * (x3[R1[a][b]] - B[0]) + w(R2[a][b]) * (x3[R2[a][b]] - B[1]) + w(R3[a][b]) * (
                    x3[R3[a][b]] - B[2]) + w(R4[a][b]) * (x3[R4[a][b]] - B[3]) + w(R5[a][b]) * (
                                x3[R5[a][b]] - B[4]) + w(R6[a][b]) * (x3[R6[a][b]] - B[5]) + w(R7[a][b]) * (
                                x3[R7[a][b]] - B[6]))
        down = float(w(R1[a][b]) + w(R2[a][b]) + w(R3[a][b]) + w(R4[a][b]) + w(R5[a][b]) + w(R6[a][b]) + w(R7[a][b]))
        FinalR[int(a / 4)][int(b / 4)] = top / down
        a=a+4
    b=b+4

Bmean=math.exp(np.mean(FinalB))
Gmean=math.exp(np.mean(FinalG))
Rmean=math.exp(np.mean(FinalR))
Bmax=math.exp(np.max(FinalB))
Gmax=math.exp(np.max(FinalG))
Rmax=math.exp(np.max(FinalR))
AnsB=np.zeros((1040,1560),np.uint8(1))
AnsG=np.zeros((1040,1560),np.uint8(1))
AnsR=np.zeros((1040,1560),np.uint8(1))
Bmax=Bmax/Bmean
Gmax=Gmax/Gmean
Rmax=Rmax/Rmean
b=0
while b<1560:
    a=0
    while a<1040:
        LB=1*math.exp(FinalB[a][b])/Bmean
        LG = 1*math.exp(FinalG[a][b])/ Gmean
        LR = 1*math.exp(FinalR[a][b])/ Rmean
        AnsB[a][b]=int(255*LB/(1+LB)*(1+LB/Bmax/Bmax))
        AnsG[a][b] = int(255*LG/(1+LG)*(1+LG/Gmax/Gmax))
        AnsR[a][b] = int(255*LR /(1+LR )*(1+LR /Rmax/Rmax))
        a=a+1
    b=b+1


merge=cv2.merge([AnsB,AnsG,AnsR])
cv2.imwrite(file,merge)

HDR=np.zeros((1040,1560,3),dtype=float)
a=0
while a < 1040:
    b=0
    while b<1506:
        HDR[a][b][0]=math.exp(FinalB[a][b])
        HDR[a][b][1] = math.exp(FinalG[a][b])
        HDR[a][b][2] = math.exp(FinalR[a][b])
        b=b+1
    a=a+1
file=file.replace(".jpg",".hdr")
cv2.imwrite(file,HDR)






