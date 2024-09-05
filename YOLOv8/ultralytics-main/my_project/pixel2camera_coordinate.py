import cv2
import numpy as np
from ultralytics import YOLO

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

model = YOLO('numberv10.pt')

# Camera intrinsic matrix (example values, need to be calibrated for your camera)
mtx = np.array([
    [723.67637467, 0.0, 355.05402153],
    [0.0, 725.23755317, 241.22181201],
    [0.0, 0.0, 1.0]
])  # Camera intrinsic matrix (in pixels)

dist = np.array([-2.51361765e-01, 5.22063658e-01, -5.27509826e-04,  -9.97607324e-06, -1.52992367e+00])  # Distortion coefficients

# Define a default depth value (in meters)
default_depth = 1.0

def get_center_coordinates(box):
    x1, y1, x2, y2 = box
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    return x_center, y_center

def pixel_to_camera_coordinates(x_center, y_center, mtx, dist, default_depth,scale_factor=1.0):
    # Convert pixel coordinates to normalized camera coordinates
    uv_point = np.array([[x_center, y_center]], dtype=np.float32).reshape(-1, 1, 2)
    uv_point = cv2.undistortPoints(uv_point, mtx, dist, P=mtx)
    uv_point = np.append(uv_point[0][0], [1.0])  # Homogeneous coordinates

    # Assume the depth value (z) is known or set to a default value
    z = default_depth

    # Convert to camera coordinates
    camera_coordinates = np.dot(np.linalg.inv(mtx), uv_point * z)

    return (camera_coordinates * scale_factor).flatten()

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

                    camera_coordinates = pixel_to_camera_coordinates(
                        x_center, y_center, mtx, dist, default_depth,scale_factor=100
                    )
                    print(f"Center coordinates (camera): ({camera_coordinates[0]:.2f}, {camera_coordinates[1]:.2f}, {camera_coordinates[2]:.2f})")
                    #線性修正
                    correction_factor = 1.02 
                    if(camera_coordinates[0]>=0):
                        x_corrected = (camera_coordinates[0] -(0.03 * 100) * correction_factor)
                    else:
                        x_corrected = (camera_coordinates[0] + 0.03 * 100) * correction_factor

                    if(camera_coordinates[1]>=0):
                        y_corrected = (camera_coordinates[1] - 0.03 * 100) * correction_factor
                    else:
                        y_corrected = (camera_coordinates[1] + 0.03 * 100) * correction_factor

                    if(camera_coordinates[2]>=0):
                        z_corrected = (camera_coordinates[2] - 0.03 * 100) * correction_factor
                    else:
                        z_corrected = (camera_coordinates[2] + 0.03 * 100) * correction_factor
                        
                    # #x_corrected = (camera_coordinates[0] - 0.03) * correction_factor
                    # y_corrected = (camera_coordinates[1] - 0.03) * correction_factor
                    # z_corrected = camera_coordinates[2] * correction_factor

                    print(f"Corrected Center coordinates (camera): ({x_corrected:.2f}, {y_corrected:.2f}, {z_corrected:.2f})")

                    
                    cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
                    cv2.circle(frame, (int(x_center), int(y_center)), 5, (0, 0, 255), -1)
                    cv2.putText(frame, label, (int(box[0]), int(box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

            cv2.imshow('YOLOv8 Detection', frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
