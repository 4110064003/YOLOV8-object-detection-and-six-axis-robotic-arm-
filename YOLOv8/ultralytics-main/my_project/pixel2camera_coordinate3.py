import cv2
import numpy as np
from ultralytics import YOLO

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

model1 = YOLO('numberv10.pt')#number detect
model2 = YOLO('cubev1.pt')#cube detect

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

        screen_width = 1500
        screen_height = 800
        window_width = screen_width // 2
        window_height = screen_height // 2
        cv2.namedWindow('Press "s" to capture an image (or "q" to quit)',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Press "s" to capture an image (or "q" to quit)',window_width,window_height)
        cv2.imshow('Press "s" to capture an image (or "q" to quit)', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):  # 's' key is pressed
            unique_results = set()#存儲並過濾重複的結果
            results1 = model1(frame, show=False,conf=0.7)#number detect
            results2 = model2(frame, show=False,conf=0.7)#cube detect
           
            for result1 in results1:
                for result2 in results2:

                    boxes1 = result1.boxes.xyxy.cpu().numpy()
                    confidences1 = result1.boxes.conf.cpu().numpy()
                    class_ids1 = result1.boxes.cls.cpu().numpy()

                    boxes2 = result2.boxes.xyxy.cpu().numpy()
                    confidences2 = result2.boxes.conf.cpu().numpy()
                    class_ids2 = result2.boxes.cls.cpu().numpy()

                    for box1, confidence1, class_id1 in zip(boxes1, confidences1, class_ids1):
                        for box2, confidence2, class_id2 in zip(boxes2, confidences2, class_ids2):

                            x_center1, y_center1 = get_center_coordinates(box1)
                            label1 = result1.names[int(class_id1)]

                            x_center2, y_center2 = get_center_coordinates(box2)
                            label2 = result2.names[int(class_id2)]
                            # print(f"Detected object: Label {label2}, Confidence {confidence2:.2f}")
                            # print(f"Center coordinates (pixels): ({x_center2:.2f}, {y_center2:.2f})")

                            camera_coordinates1 = pixel_to_camera_coordinates(
                                x_center1, y_center1, mtx, dist, default_depth,scale_factor=100
                            )
                            camera_coordinates2 = pixel_to_camera_coordinates(
                                x_center2, y_center2, mtx, dist, default_depth,scale_factor=100
                            )
                        
                            #線性修正
                            correction_factor = 1.02 
                            if(camera_coordinates1[0]>=0):
                                x_corrected1 = (camera_coordinates1[0] - (0.03 * 100) * correction_factor)
                            else:
                                x_corrected1 = (camera_coordinates1[0] + (0.03 * 100) * correction_factor)

                            if(camera_coordinates1[1]>=0):
                                y_corrected1 = (camera_coordinates1[1] - (0.03 * 100) * correction_factor)
                            else:
                                y_corrected1 = (camera_coordinates1[1] + (0.03 * 100) * correction_factor)

                            if(camera_coordinates1[2]>=0):
                                z_corrected1 = (camera_coordinates1[2] - (0.03 * 100) * correction_factor)
                            else:
                                z_corrected1 = (camera_coordinates1[2] + (0.03 * 100) * correction_factor)
                            if(camera_coordinates2[0]>=0):
                                x_corrected2 = (camera_coordinates2[0] - (0.03 * 100) * correction_factor)
                            else:
                                x_corrected2 = (camera_coordinates2[0] + (0.03 * 100) * correction_factor)

                            if(camera_coordinates2[1]>=0):
                                y_corrected2 = (camera_coordinates2[1] - (0.03 * 100) * correction_factor)
                            else:
                                y_corrected2 = (camera_coordinates2[1] + (0.03 * 100) * correction_factor)

                            # if(camera_coordinates2[2]>=0):
                            #     z_corrected2 = (camera_coordinates2[2] - (0.03 * 100) * correction_factor)
                            # else:
                            #     z_corrected2 = (camera_coordinates2[2] + (0.03 * 100) * correction_factor)    

                            object_info1 = (f"{label2},({int(x_corrected2)},{int(y_corrected2)})")
                            object_info2 = (f"{label1},({int(x_corrected1)},{int(y_corrected1)})")
                            # transmission_string = object_info1 + "|" + object_info2
                            # unique_results.add(transmission_string)
                            unique_results.add(object_info1)
                            unique_results.add(object_info2)
                            
                            cv2.rectangle(frame, (int(box1[0]), int(box1[1])), (int(box1[2]), int(box1[3])), (100, 100, 100), 2)
                            cv2.circle(frame, (int(x_center1), int(y_center1)), 5, (0, 0, 255), -1)
                            cv2.putText(frame, label1, (int(box1[0]), int(box1[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 2)

                            cv2.rectangle(frame, (int(box2[0]), int(box2[1])), (int(box2[2]), int(box2[3])), (200, 200, 200), 2)
                            cv2.circle(frame, (int(x_center2), int(y_center2)), 5, (0, 0, 255), -1)
                            cv2.putText(frame, label2, (int(box2[0]), int(box2[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 2)
            screen_width = 1500
            screen_height = 800
            window_width = screen_width // 2
            window_height = screen_height // 2
            cv2.namedWindow('YOLOv8 Detection',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('YOLOv8 Detection',window_width,window_height)
            cv2.imshow('YOLOv8 Detection', frame)

            for result in unique_results:
                print(result)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
