import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


#球半徑
radius = 28

#導入桌子
table=cv2.imread("direct.jpg")

#球座標標示
balls=np.array([[140,360],  #白球
                [380,430]]) #目標球
white_ball=balls[0]
target_ball=balls[1]
for i in balls:
    cv2.circle(table,i,10,(255,0,0),-1)

#洞座標標示
hole=np.array([[0,0],[500,0],[500,1000],[0,1000],[0,500],[500,500]])
for i in hole:
    cv2.circle(table,i,10,(255,0,0),-1)

#角度
theta=np.empty(6, dtype=float)

#計算向量/長度
v1=np.subtract(balls[1],balls[0])
dv1 = np.linalg.norm(v1)
for i in range(int(len(hole))):
    v=np.subtract(hole[i],balls[1])
    dv = np.linalg.norm(v)

    #內積/角度
    dot=(np.dot(v,v1))/(dv*dv1)
    theta[i]=np.degrees(np.arccos(dot))
    print(theta)

#找最小角度
min_theta=min(theta)
print(min_theta)


if(min_theta<60):
        
        #單位向量
        vv=v/dv  

        #計算假想球位置
        f_x=target_ball[0]-int(vv[0]*2*radius)
        f_y=target_ball[1]-int(vv[1]*2*radius)

       #畫出假想球
        cv2.circle(table,(f_x,f_y),28,(255,255,255),2)

        #畫出路徑
        cv2.arrowedLine(table,balls[0],(f_x,f_y),(255,0,0),5)
        cv2.arrowedLine(table,balls[1],hole[i],(255,0,0),5)

#順時針旋轉90度
table = cv2.rotate(table, cv2.ROTATE_90_CLOCKWISE)

cv2.imshow("direct",table)
cv2.waitKey(0)
cv2.destroyAllWindows()
