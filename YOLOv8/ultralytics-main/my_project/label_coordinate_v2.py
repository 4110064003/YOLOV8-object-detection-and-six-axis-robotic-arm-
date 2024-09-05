#目標檢測並繪製圖像中心像素座標+轉換成世界座標-函式化(失敗))
import cv2
import numpy as np
from ultralytics import YOLO

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

model = YOLO('numberv10.pt')

mtx = np.array([
    [731.16432251, 0.0, 359.48897199],
    [0.0, 730.40723576, 248.13841344],
    [0.0, 0.0, 1.0]
])# 内参矩阵(單位:像素))

dist = np.array([
    [0,0,0,0,0]
]) # 畸变系数

rvec = np.array([[ 0.32623864], [-0.08227388], [-0.02670312]])#旋轉向量(單位:毫米))

tvec = np.array([[7.72379069],[-175.40563787],[703.983487]])#平移向量

# mtx = np.array([
#     [927.49874472, 0.0, 638.97945312],
#     [0.0, 925.50712525, 385.43000942],
#     [0.0, 0.0, 1.0]
# ])# 内参矩阵(單位:像素))

# dist = np.array([
#     [-1.78869187e-01,5.84782295e-01,1.26929886e-03,-2.15256821e-04,-6.42509309e-01]
# ]) # 畸变系数

# rvec = np.array([[ -0.0365353], [-0.01703883], [ 0.00259986]])#旋轉向量(單位:毫米))

# tvec = np.array([[-229.3834985],[-138.28186232],[429.85150704]])#平移向量

def get_center_coordinates(box):
    x1, y1, x2, y2 = box
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    return x_center, y_center

def pixel_to_world_coordinates(x_center, y_center, mtx, dist, rvec, tvec,scale_factor=1.0):
    # Convert pixel coordinates to normalized camera coordinates
    uv_point = np.array([[x_center, y_center]], dtype=np.float32).reshape(-1, 1, 2)
    uv_point = cv2.undistortPoints(uv_point, mtx, dist, P=mtx)
    uv_point = np.append(uv_point[0][0], [1.0])   # Homogeneous coordinates

    # Convert camera coordinates to world coordinates
    rotation_matrix, _ = cv2.Rodrigues(rvec)
    camera_coordinates = np.dot(np.linalg.inv(mtx), uv_point)
    world_coordinates = np.dot(rotation_matrix.T, (camera_coordinates - tvec))

    return (world_coordinates * scale_factor).flatten()
def main():
    # Open a video capture object (source=1 indicates the first camera)
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Could not open video source.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        cv2.imshow('Press "s" to capture an image (or "q" to quit)', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):  # 's' key is pressed
            results = model(frame, show=False)

            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()
                confidences = result.boxes.conf.cpu().numpy()
                class_ids = result.boxes.cls.cpu().numpy()

                for box, confidence, class_id in zip(boxes, confidences, class_ids):
                    x_center, y_center = get_center_coordinates(box)
                    label = result.names[int(class_id)]
                    print(f"Detected object: Label {label}, Confidence {confidence:.2f}")
                    print(f"Center coordinates (pixels): ({x_center:.2f}, {y_center:.2f})")

                    world_coordinates = pixel_to_world_coordinates(
                        x_center, y_center, mtx, dist, rvec, tvec,scale_factor=1
                    )
                    print(f"Center coordinates (world): ({world_coordinates[0]:.2f}, {world_coordinates[1]:.2f}, {world_coordinates[2]:.2f})")

                    cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
                    cv2.circle(frame, (int(x_center), int(y_center)), 5, (0, 0, 255), -1)
                    cv2.putText(frame, label, (int(box[0]), int(box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            cv2.imshow('YOLOv8 Detection', frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
