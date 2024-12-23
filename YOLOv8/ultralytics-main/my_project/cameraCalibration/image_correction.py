import cv2
import numpy as np

# 读取标定后的参数
mtx = np.array([
    [927.49874472, 0.0, 638.97945312],
    [0.0, 925.50712525, 385.43000942],
    [0.0, 0.0, 1.0]
])
print("mtx:")# 内参矩阵
print(mtx)

dist = np.array([
    [-1.78869187e-01,  5.84782295e-01,  1.26929886e-03, -2.15256821e-04, -6.42509309e-01]
])  
print("dist:")
print(dist)# 畸变系数
# 读取待校正的图像
img = cv2.imread("D:\camera_calibration\Image\image_16.jpg")
h, w = img.shape[:2]

# 获取校正映射
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)

# 应用映射进行校正
dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

# 裁剪图像
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]

cv2.imshow('calibrated_image', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
