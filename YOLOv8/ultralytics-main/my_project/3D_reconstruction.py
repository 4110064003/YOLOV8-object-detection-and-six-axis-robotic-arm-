#相機標定棋盤格角點回推其三維座標

import numpy as np
import cv2

# # Initialization parameters
# board_cols = 7  # Number of columns in the chessboard
# board_rows = 4  # Number of rows in the chessboard
# square_size = 35.0  # Size of each chessboard square

board_cols = 7  # Number of columns in the chessboard
board_rows = 5  # Number of rows in the chessboard
square_size = 33.0  # Size of each chessboard square

# Prepare object points
objp = np.zeros((board_cols * board_rows, 3), np.float32)
objp[:, :2] = np.mgrid[0:board_cols, 0:board_rows].T.reshape(-1, 2)
objp *= square_size

print("Object Points:")
print(objp)

# Store 3D points in real-world space and 2D points in image plane
objpoints = []  # 3D points
imgpoints = []  # 2D points

# Read calibration images
image_nums = 17
for i in range(1, image_nums):
    img_path = f"D:\\camera_calibration\\Image\\image_{i}.jpg"  # Update this path as needed
    #img_path = r"D:\camera_calibration\chessboard\image_%d.jpg" % i
    img = cv2.imread(img_path)
    
    if img is None:
        print(f"Image {i} not found or could not be loaded.")
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow(f"Gray Image {i}", gray)
    cv2.waitKey(100)  # Display for 0.1 seconds

    h, w = gray.shape

    # Find chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (board_cols, board_rows), None)
    
    if ret:
        print(f"Found corners in image {i}...")
        objpoints.append(objp)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        img = cv2.drawChessboardCorners(img, (board_cols, board_rows), corners2, ret)
        cv2.imshow("img", img)
        cv2.waitKey(100)
    else:
        print(f"Could not find corners in image {i}.")

# Camera calibration
if len(objpoints) == 0 or len(imgpoints) == 0:
    print("No corners found in any images.")
else:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (w, h), None, None)
    
    # Print camera parameters
    print("ret:", ret)
    print("Camera Matrix:\n", mtx)
    print("Distortion Coefficients:\n", dist)
    print("Rotation Vectors:\n", rvecs)
    print("Translation Vectors:\n", tvecs)

    # Calculate reprojection error
    total_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
        total_error += error
    print("Total reprojection error: ", total_error / len(objpoints))

# Assume using the first set of rotation and translation vectors to compute 3D points
rvec = rvecs[0]
tvec = tvecs[0]

# Convert to 3D coordinates
R, _ = cv2.Rodrigues(rvec)
proj_matrix = np.hstack((R, tvec))
points_3d = cv2.triangulatePoints(mtx @ proj_matrix, mtx @ np.hstack((np.eye(3), np.zeros((3, 1)))), imgpoints[0], imgpoints[0])
points_3d /= points_3d[3]  # Normalize

print("3D points:", points_3d.T)

cv2.destroyAllWindows()
