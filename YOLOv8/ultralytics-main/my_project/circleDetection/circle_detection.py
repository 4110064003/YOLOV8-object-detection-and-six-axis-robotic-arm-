#畫面中圓形的偵測和圓心的標註，與本專題無關
import cv2
import numpy as np

def filter_circles(circles, min_distance, min_radius, max_radius):
    filtered_circles = []
    for i in range(len(circles[0])):
        circle = circles[0][i]
        # 檢查半徑範圍
        if min_radius <= circle[2] <= max_radius:
            is_valid = True
            for j in range(len(filtered_circles)):
                if np.linalg.norm(circle[:2] - filtered_circles[j][:2]) < min_distance:
                    is_valid = False
                    break
            if is_valid:
                filtered_circles.append(circle)
    return np.array(filtered_circles)

# 讀取圖像
image = cv2.imread(r"D:\ultralytics-main\my_project\circle2.jpg", cv2.IMREAD_GRAYSCALE)
if image is None:
    print("Image is not found or could not be loaded.")
    exit()

# 使用霍夫變換檢測圓形
circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                           param1=50, param2=30, minRadius=0, maxRadius=0)
if circles is None:
    print("Circle is not found.")
    exit()

# 假設 circles 是檢測到的圓形
filtered_circles = filter_circles(circles, min_distance=20, min_radius=10, max_radius=50)
for circle in filtered_circles:
    center = (int(circle[0]), int(circle[1]))  # 確保圓心座標是整數
    radius = int(circle[2])  # 確保半徑是整數
    print(f"Filtered circle center: ({circle[0]}, {circle[1]}), radius: {circle[2]}")
    cv2.circle(image, center, radius, (0, 255, 0), 2)  # 繪製圓形
    cv2.circle(image, center, 2, (255, 0, 0), 3)  # 繪製圓心

# 創建視窗並調整大小
cv2.namedWindow('Detected Circles', cv2.WINDOW_NORMAL)  # 創建可調整大小的視窗
cv2.resizeWindow('Detected Circles', 600, 600)  # 設定視窗大小

cv2.imshow('Detected Circles', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 假設你已經有了這些變數
mtx = np.array([
    [927.49874472, 0.0, 638.97945312],
    [0.0, 925.50712525, 385.43000942],
    [0.0, 0.0, 1.0]
])  # 内参矩阵

# 旋转向量
rvecs = [
    np.array([[-0.0365353], [-0.01703883], [0.00259986]]),
    np.array([[0.00168653], [0.24732506], [-0.00858347]]),
    np.array([[0.13800783], [-0.34731576], [0.04911687]]),
    np.array([[0.01583372], [-0.03008439], [0.01061453]]),
    np.array([[0.03130002], [0.32110227], [-0.0016625]]),
    np.array([[0.00032374], [-0.18844096], [0.01931206]]),
    np.array([[0.40932833], [0.02043491], [-0.000857]]),
    np.array([[0.0153074], [-0.20078217], [0.01590655]]),
    np.array([[-0.0145390049], [0.274370061], [-0.0000784489406]]),
    np.array([[0.3348518], [-0.05959935], [0.01987335]]),
    np.array([[-0.01687612], [0.04256186], [-0.00630748]]),
    np.array([[-0.04835192], [-0.26383995], [-0.00189974]]),
    np.array([[0.00185724], [0.34123147], [0.00734889]]),
    np.array([[0.31681871], [0.01193171], [-0.00361693]]),
    np.array([[0.06283209], [-0.04646789], [0.00464032]]),
    np.array([[0.40996877], [-0.07222524], [0.02910445]])
]

# 位移向量
tvecs = [
    np.array([[-229.3834985], [-138.28186232], [429.85150704]]),
    np.array([[-266.98063411], [-124.16079933], [451.8061335]]),
    np.array([[-233.14422638], [-144.35977198], [433.7742916]]),
    np.array([[65.56824297], [-142.19819892], [458.20616616]]),
    np.array([[41.75254221], [-130.45633663], [476.14302157]]),
    np.array([[62.16223465], [-135.825482], [454.37703867]]),
    np.array([[46.14489825], [-122.38095905], [424.49089905]]),
    np.array([[116.79749145], [-3.06144167], [471.98611508]]),
    np.array([[63.20117339], [-19.79738634], [508.34196773]]),
    np.array([[67.98732544], [9.49775805], [434.42701384]]),
    np.array([[-262.83977328], [-11.16334881], [481.31236886]]),
    np.array([[-232.63436367], [-28.04115522], [420.52033923]]),
    np.array([[-310.81970323], [-8.84333482], [516.20169393]]),
    np.array([[-270.33036519], [-144.30603452], [461.37579749]]),
    np.array([[80.5664633], [-0.361447739], [442.682441]]),
    np.array([[-254.06301433], [18.91126074], [440.39487633]])
]

# 將旋轉向量轉換為旋轉矩陣
rotation_matrices = []

for rvec in rvecs:
    rotation_matrix, _ = cv2.Rodrigues(rvec)
    rotation_matrices.append(rotation_matrix)

# 計算三維點
points_3d = []

for i in range(len(rvecs)):
    proj_matrix = np.hstack((rotation_matrices[i], tvecs[i]))
    # 假設 imgpoints 是從檢測的圓形中獲取的二維點
    imgpoints = np.array([[circle[0], circle[1]] for circle in filtered_circles]).T
    points_3d_temp = cv2.triangulatePoints(mtx @ proj_matrix,
                                            mtx @ np.hstack((np.eye(3), np.zeros((3, 1)))),
                                            imgpoints, imgpoints)
    points_3d.append(points_3d_temp)

# 將齊次坐標轉換為非齊次坐標
points_3d = [p / p[3] for p in points_3d]

# 打印三維點
for i, p in enumerate(points_3d):
    print(f"3D Points {i + 1}: {p[:3].T}")  # 只顯示 x, y, z 坐標

# 將三維點投影到二維平面
projected_points = []
for point in points_3d:
    # 使用內參矩陣將三維點投影到二維平面
    point_2d = mtx @ point[:3]  # 只取 x, y, z
    point_2d /= point_2d[2]  # 齊次坐標轉換
    # 確保轉換為標量
    projected_points.append((int(point_2d[0]), int(point_2d[1])))

# 在圖像上繪製投影的點
for (x, y) in projected_points:
    cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # 繪製綠色圓點

# 顯示結果
cv2.namedWindow('Projected Points', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Projected Points', 600, 600)
cv2.imshow('Projected Points', image)
cv2.waitKey(0)
cv2.destroyAllWindows()