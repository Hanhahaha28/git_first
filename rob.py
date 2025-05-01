import cv2
import numpy as np

# 球半徑
radius = 28

# 導入桌子
table = cv2.imread("combine.png")

# 球座標標示
balls = np.array([
    [120, 740],  # 白球
    [310, 810],  # 目標球（先打）
    [400, 925],  # 其他球（干擾球）
    [350, 550]   # 其他球（干擾球）
])

white_ball = balls[0]
target_ball = balls[1]
other_balls = balls[2:]

for i in balls:
    cv2.circle(table, i, 10, (255, 0, 0), -1)

# 洞座標標示
holes = np.array([[0,0], [500,0], [500,1000], [0,1000], [0,500], [500,500]])
for i in holes:
    cv2.circle(table, i, 10, (255, 0, 0), -1)

# 計算向量長度
def vec_len(v):
    return np.linalg.norm(v)

# 檢查路徑上是否有阻擋

def is_path_clear(start, end, all_balls, ignore=None):
    v_line = np.array([end[1] - start[1], start[0] - end[0]])
    line_len = vec_len(v_line)
    for ball in all_balls:
        if ignore is not None and (ball == ignore).all():
            continue
        if (ball == start).all() or (ball == end).all():
            continue
        dis = abs((end[1]-start[1])*ball[0] + (start[0]-end[0])*ball[1] + (end[0]*start[1] - start[0]*end[1])) / line_len
        if dis < radius*2:
            proj_len = np.dot(np.subtract(ball, start), np.subtract(end, start)) / vec_len(np.subtract(end, start))
            if 0 < proj_len < vec_len(np.subtract(end, start)):
                return False
    return True

# 主流程：組合球判斷
for other in other_balls:
    for hole in holes:

        # 1. 其他球 -> 洞 路徑要乾淨
        if not is_path_clear(other, hole, balls, ignore=other):
            continue

        # 2. 目標球 -> 其他球 路徑要乾淨
        if not is_path_clear(target_ball, other, balls, ignore=target_ball):
            continue

        # 3. 白球 -> 目標球 路徑要乾淨
        if not is_path_clear(white_ball, target_ball, balls, ignore=white_ball):
            continue

        # 4. 角度檢查 (目標球打其他球方向合理)
        to_other_vec = np.subtract(other, target_ball)
        to_hole_vec = np.subtract(hole, other)
        angle = np.degrees(np.arccos(np.clip(np.dot(to_other_vec, to_hole_vec) / (vec_len(to_other_vec) * vec_len(to_hole_vec)), -1.0, 1.0)))

        if angle > 30:  # 角度太歪，不適合組合球
            continue

        # 5. 畫出所有路徑
        cv2.arrowedLine(table, white_ball, target_ball, (0, 255, 255), 5)  # 白球到目標球
        cv2.arrowedLine(table, target_ball, other, (0, 255, 255), 5)      # 目標球到其他球
        cv2.arrowedLine(table, other, hole, (200, 0, 0), 5)               # 其他球到洞

        # 標記提示
        cv2.circle(table, (other[0], other[1]), radius, (255, 0, 255), 3)
        cv2.circle(table, (target_ball[0], target_ball[1]), radius, (255, 255, 255), 3)

# 旋轉圖片
result = cv2.rotate(table, cv2.ROTATE_90_CLOCKWISE)

cv2.imshow("combo_shot", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
