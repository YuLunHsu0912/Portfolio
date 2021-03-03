import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
def w(z):
    if(z<=127):
        return z+1
    else :
        return 256-z

img1 = cv2.imread('3.jpg')
img2=cv2.imread('4.jpg')
img3=cv2.imread('5.jpg')
img4=cv2.imread('6.jpg')
img5=cv2.imread('7.jpg')

(B1, G1, R1) = cv2.split(img1)
(B2, G2, R2) = cv2.split(img2)
(B3, G3, R3) = cv2.split(img3)
(B4, G4, R4) = cv2.split(img4)
(B5, G5, R5) = cv2.split(img5)

#把bgr放入z分別做三條response curve
pixel = 50
picture = 10  # depends on actual
z = np.zeros((930, 5))
z2 =np.zeros((930, 5))
z3 =np.zeros((930, 5))
#長的在後面
x=0
y=0
a=0
while x <6240:
    y = 0
    while y<4160:
        z[a][0]=B1[y][x]
        z[a][1] = B2[y][x]
        z[a][2] = B3[y][x]
        z[a][3] = B4[y][x]
        z[a][4] = B5[y][x]
        z2[a][0] = G1[y][x]
        z2[a][1] = G2[y][x]
        z2[a][2] = G3[y][x]
        z2[a][3] = G4[y][x]
        z2[a][4] = G5[y][x]
        z3[a][0] = R1[y][x]
        z3[a][1] = R2[y][x]
        z3[a][2] = R3[y][x]
        z3[a][3] = R4[y][x]
        z3[a][4] = R5[y][x]
        a=a+1
        y=y+int(4160/30)
    x=x+int(6240/30)
B = [math.log(1/13),math.log(1/10),math.log(1/4),math.log(3/5),math.log(1)]
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
    if(x[a]-(x[a-1]+x[a+1]+x[a-2]+x[a+2])/4>1):
        x[a]=(x[a-1]+x[a+1]+x[a-2]+x[a+2])/4
    if (x2[a] - (x2[a - 1] + x2[a + 1]+x2[a-2]+x2[a+2]) / 4 > 1):
        x2[a] = (x2[a - 1] + x2[a + 1]+x2[a-2]+x2[a+2]) / 4
    if (x3[a] - (x3[a - 1] + x3[a + 1]+x3[a-2]+x3[a+2]) / 4 > 1):
        x3[a] = (x3[a - 1] + x2[a + 1]+x3[a-2]+x3[a+2]) / 4

FinalB=np.zeros((416, 624),dtype=float)
FinalG=np.zeros((416, 624),dtype=float)
FinalR=np.zeros((416, 624),dtype=float)
b=0
while b < 6240:
    a=0
    while a <4160:
        FinalB[int(a / 10)][int(b / 10)] = x2[B1[a][b]] - B[0]
        a=a+10
    b=b+10
b=0
while b < 6240:
    a=0
    while a <4160:
        FinalG[int(a / 10)][int(b / 10)] = x2[G1[a][b]] - B[0]
        a=a+10
    b=b+10

b=0
while b < 6240:
    a=0
    while a <4160:
        FinalR[int(a / 10)][int(b / 10)] = x3[R1[a][b]] - B[0]

        a=a+10
    b=b+10

Bmax=FinalB[int(1529/10)][int(6033/10)]
Gmax=FinalG[int(1529/10)][int(6033/10)]
Rmax=FinalR[int(1529/10)][int(6033/10)]
AnsB=np.zeros((416,624),np.uint8(1))
AnsG=np.zeros((416,624),np.uint8(1))
AnsR=np.zeros((416,624),np.uint8(1))
b=0
while b<624:
    a=0
    while a<416:
        AnsB[a][b]=int(255*(FinalB[a][b]/(1+FinalB[a][b]))*(1+FinalB[a][b]/(Bmax)/Bmax))
        AnsG[a][b] = int(255 * (FinalG[a][b] / (1 + FinalG[a][b])) * (1 + FinalG[a][b] / (Gmax ) / Gmax ))
        AnsR[a][b] = int(255 * (FinalR[a][b] / (1 + FinalR[a][b])) * (1 + FinalR[a][b] / (Rmax ) / Rmax ))
        a=a+1
    b=b+1

merge=cv2.merge([AnsB,AnsG,AnsR])
cv2.imwrite('tree.jpg',merge)







