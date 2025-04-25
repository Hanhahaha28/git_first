import cv2
import numpy as np

#球半徑
radius = 28

#導入桌子
table=cv2.imread("combine.png")

#球座標標示
balls=np.array([[120, 740],  #白球
                [310, 810],  #目標球
                [350, 750],  #其他球
                [400, 925]]) 
white_ball=balls[0]
target_ball=balls[1]
for i in balls:
    cv2.circle(table,i,10,(255,0,0),-1)

#洞座標標示
hole=np.array([[0,0],[500,0],[500,1000],[0,1000],[0,500],[500,500]])
for i in hole:
    cv2.circle(table,i,10,(255,0,0),-1)

#碰撞檢測
def collide(w_v, t_v, ball):
    
    #計算點到直線
    v_ab = (w_v[1]-t_v[1], -w_v[0]+t_v[0])
    dv_ab=np.linalg.norm(v_ab)
    dis = abs((w_v[1]-t_v[1])*ball[0]+(-w_v[0]+t_v[0])*ball[1]+t_v[1]*w_v[0]-t_v[0]*w_v[1])/dv_ab

    #計算兩目標的向量及距離
    v_oab = (w_v[0]-t_v[0],w_v[1]-t_v[1])
    dv_oab = np.linalg.norm(v_oab)

    #計算他球與兩目標的向量及距離
    v_bw = (ball[0]-w_v[0],ball[1]-w_v[1])
    v_bt = (ball[0]-t_v[0],ball[1]-t_v[1])
    dv_bw = np.linalg.norm(v_bw)
    dv_bt = np.linalg.norm(v_bt)

    print("障礙球到a", dv_bt)
    print("障礙球到b", dv_bw)
    print("a和b的距離",dv_oab)

    #淘汰：先篩選出點到直線距離<56，並淘汰他球到任意目標<兩目標距離的球路
    if(dis < 56):
        if(dv_bw > dv_oab or dv_bt > dv_oab):
             return 1
        else:
             return 0
    else:
         return 1
    
#角度
theta=np.empty(6, dtype=float)

#計算向量/長度
v1 = np.subtract(balls[1],balls[0])
dv1 = np.linalg.norm(v1)
for i in range(int(len(hole))):
    v=np.subtract(hole[i],balls[1])
    dv = np.linalg.norm(v)

    #內積/角度
    dot=(np.dot(v,v1))/(dv*dv1)
    theta[i]=np.degrees(np.arccos(dot))
    #print(theta)
    print(f"第{i+1}個洞: {hole[i]}")


    print("白球到目標球")
    test = collide(white_ball,target_ball,balls[2])
    print("目標球到洞")
    test_h = collide(target_ball, hole[i], balls[2])
    
    if(theta[i] < 80 ):
        
        if(test and test_h):
    
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