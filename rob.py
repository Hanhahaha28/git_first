import cv2
import numpy as np

# 球半徑
radius = 28

# 導入桌子圖
table = cv2.imread("combine.png")

# 球座標：[白球、目標球、其他障礙球...]
balls = np.array([
    [120, 740],  # 白球
    [310, 810],  # 目標球
    [200, 550],  # 障礙球1
    [400, 925],  # 障礙球2
])

white_ball = balls[0]
target_ball = balls[1]

# 標示球
for i in balls:
    cv2.circle(table, i, 10, (255, 0, 0), -1)

# 洞座標
hole = np.array([
    [0, 0], [500, 0], [500, 1000],
    [0, 1000], [0, 500], [500, 500]
])

# 標示洞口
for i in hole:
    cv2.circle(table, i, 10, (255, 0, 0), -1)

# 碰撞檢查函數
def collide(w_v, t_v, ball):
    v_ab = (w_v[1] - t_v[1], -w_v[0] + t_v[0])
    dv_ab = np.linalg.norm(v_ab)
    dis = abs((w_v[1] - t_v[1]) * ball[0] + (-w_v[0] + t_v[0]) * ball[1] + t_v[1] * w_v[0] - t_v[0] * w_v[1]) / dv_ab

    v_oab = (w_v[0] - t_v[0], w_v[1] - t_v[1])
    dv_oab = np.linalg.norm(v_oab)

    v_bw = (ball[0] - w_v[0], ball[1] - w_v[1])
    v_bt = (ball[0] - t_v[0], ball[1] - t_v[1])
    dv_bw = np.linalg.norm(v_bw)
    dv_bt = np.linalg.norm(v_bt)

    if dis < 56:
        if dv_bw > dv_oab or dv_bt > dv_oab:
            return 1
        else:
            return 0
    else:
        return 1

# 判斷路線是否完全暢通
def path_clear(w_v, t_v, others):
    for ball in others:
        if collide(w_v, t_v, ball) == 0:
            return 0
    return 1

# 計算角度陣列
theta = np.empty(6, dtype=float)

# 白球到目標球向量
v1 = np.subtract(target_ball, white_ball)
dv1 = np.linalg.norm(v1)

# 檢查每個洞口
for i in range(len(hole)):
    v = np.subtract(hole[i], target_ball)
    dv = np.linalg.norm(v)
    dot = np.dot(v, v1) / (dv * dv1)
    theta[i] = np.degrees(np.arccos(dot))

    if theta[i] < 80:
        # 確認所有障礙球是否都不擋路
        other_balls = balls[2:]
        clear_to_target = path_clear(white_ball, target_ball, other_balls)
        clear_to_hole = path_clear(target_ball, hole[i], other_balls)

        if clear_to_target and clear_to_hole:
            # 計算假想球位置（白球要打的位置）
            vv = v / dv
            f_x = target_ball[0] - int(vv[0] * 2 * radius)
            f_y = target_ball[1] - int(vv[1] * 2 * radius)

            # 畫假想球與路徑
            cv2.circle(table, (f_x, f_y), 28, (255, 255, 255), 2)
            cv2.arrowedLine(table, white_ball, (f_x, f_y), (255, 0, 0), 5)
            cv2.arrowedLine(table, target_ball, hole[i], (255, 0, 0), 5)

# 旋轉畫面
table = cv2.rotate(table, cv2.ROTATE_90_CLOCKWISE)

cv2.imshow("direct", table)
cv2.waitKey(0)
cv2.destroyAllWindows()
