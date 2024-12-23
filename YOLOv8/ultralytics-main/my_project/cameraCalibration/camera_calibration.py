#使用
import numpy as np
import cv2

# 初始化参数
board_cols = 7  #橫向角點個數(行數-1)
board_rows = 4  #直向角點個數(列數-1)
square_size = 35.0   #一小方格邊長

# 准备物体点
objp = np.zeros((board_cols * board_rows, 3), np.float32)#三維點座標
objp[:, :2] = np.mgrid[0:board_cols, 0:board_rows].T.reshape(-1, 2)
objp *= square_size

# 打印物体点以确认
print("Object Points:")
print(objp)

# 存储棋盘格的三维点和图像平面的二维点
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

# 读取标定图片
image_nums = 31
for i in range(1,image_nums):
    # 更換成電腦上標定圖像的路徑
    img = cv2.imread(r"D:\camera_calibration\chessboard2\image_%d.jpg" % i)
    #img = cv2.imread(r"C:\Users\acer\Downloads\test2.jpg")
    if img is None:
        print(f"Image {i} not found or could not be loaded.")
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow(f"Gray Image {i}", gray)
    cv2.waitKey(100)  # 显示0.5秒
    cv2.destroyAllWindows()
    # 調整灰度圖像對比圖
    #gray = cv2.equalizeHist(gray)
    #cv2.imshow(f"Equalized Gray Image {i}", gray)
    #cv2.waitKey(500)

    # 自動獲取圖像寬高
    h, w = gray.shape

    # 提取棋盤格角點
    ret, corners = cv2.findChessboardCorners(gray, (board_cols, board_rows), None)

    if ret:
        print("Find %dth images' corners..." % i)
        objpoints.append(objp)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # 繪製棋盤格角點
        img = cv2.drawChessboardCorners(img, (board_cols, board_rows), corners2, ret)
        cv2.imshow("img", img)
        cv2.waitKey(1000)
    else:
        print(f"Could not find corners in {i}th image.")

# 相機標定
if len(objpoints) == 0 or len(imgpoints) == 0:
    print("No corners found in any images.")
else:
    ret1, mtx, dist, rvecs1, tvecs1 = cv2.calibrateCamera(objpoints, imgpoints, (w, h), None, None)
    print("ret", ret1)
    print("mtx:", mtx)  # 內參矩陣
    print("dist", dist)  # 畸变系数
    print("rvecs1",rvecs1)  #   旋轉矩陣
    print("tvecs1",tvecs1)  #   平移向量
cv2.destroyAllWindows()
