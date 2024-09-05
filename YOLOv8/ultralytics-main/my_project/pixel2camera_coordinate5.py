import cv2
import socket
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

def format_message(data):
    try:
        # 分割物件和目標
        object_data, destination_data = data.split(';')
        
        # 處理物件的部分
        object_parts = object_data.split(',', 1)  # Only split into two parts
        object_label = object_parts[0]
        object_coordinates = object_parts[1]
        x, y, z = object_coordinates.strip('()').split(',')
        formatted_object = f"{object_label} {x} {y} {z}"

        # 處理目標的部分
        destination_parts = destination_data.split(',', 1)  # Only split into two parts
        destination_label = destination_parts[0]
        destination_coordinates = destination_parts[1]
        dx, dy, dz = destination_coordinates.strip('()').split(',')
        formatted_destination = f"{destination_label} {dx} {dy} {dz}"

        return formatted_object, formatted_destination

    except ValueError as e:
        print(f"Error in format_message: {e}")
        return None, None

def send_data_to_server(data):
    # 設定伺服器的 IP 地址和端口
    server_ip = '192.168.145.176'
    server_port = 1000   
    # 創建一個 TCP 客戶端 socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 連接到伺服器
        client.connect((server_ip, server_port))
        
        # 傳送資料到伺服器
        client.send(data.encode())  # 編碼為位元組並傳送
        
        # 接收伺服器的回覆
        response = client.recv(1024).decode()
        print("伺服器回應:", response)
    
    except Exception as e:
        print("無法連接到伺服器:", e)
    
    finally:
        # 關閉連接
        client.close()

# 新的物件要加入 unique_results 時進行檢查
def add_object_to_results(label, x_corrected, y_corrected, z=50, threshold=10):
    # 遍歷已存在的物件來檢查是否有相似的座標
    for key, value in unique_results.items():
        _, coords = value.split(',')
        x_existing, y_existing, z_existing = map(int, coords.strip('()').split(','))

        # 計算座標之間的歐氏距離
        distance = math.sqrt((x_corrected - x_existing) ** 2 + (y_corrected - y_existing) ** 2)

        if distance < threshold:
            print(f"Found similar object: {label} at ({x_corrected}, {y_corrected}) is close to {key} at ({x_existing}, {y_existing})")
            # 如果座標接近，選擇保留現有的或替換
            return
    
    # 如果沒有接近的物件，則加入 unique_results
    unique_results[label] = f"{label},({int(x_corrected)},{int(y_corrected)},{z})"    
# def add_object_to_results(label, corrected_coordinates):
#     x_corrected, y_corrected = corrected_coordinates[:2]
#     z_value = 50  # 固定的 z 值

#     # 創建結果字符串
#     result_string = f"{label},({int(x_corrected)},{int(y_corrected)},{z_value})"
    
#     # 將結果加入到 unique_results 中
#     if label in unique_results:
#         existing_coords = unique_results[label]
#         existing_label, existing_coords_str = existing_coords.split(',', 1)
#         print(1)
#         print(existing_label,existing_coords_str)
#         # 拆分現有的座標部分
#         existing_x, existing_y, existing_z = map(int, existing_coords_str.strip('()').split(','))
#         print(1)
#         print(existing_x, existing_y, existing_z)
#         new_x, new_y, new_z = map(int, existing_coords_str.strip('()').split(','))
#         print(new_x, new_y, new_z)
#         # 如果新座標與現有座標太接近，則不更新
#         if abs(existing_x - new_x) < 1 and abs(existing_y - new_y) < 1:
#             return

#     # 如果沒有發生重複，則直接更新
#     unique_results[label] = result_string
        
# unique_results = set()#存儲並過濾重複的結果
unique_results = {}#存儲並過濾重複的結果
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
            results1 = model1(frame, show=False,conf=0.8)#number detect
            results2 = model2(frame, show=False,conf=0.8)#cube detect

            #unique_results = set()
            for result1, result2 in zip(results1, results2):
                boxes1 = result1.boxes.xyxy.cpu().numpy()
                boxes2 = result2.boxes.xyxy.cpu().numpy()

                confidences1 = result1.boxes.conf.cpu().numpy()
                confidences2 = result2.boxes.conf.cpu().numpy()

                class_ids1 = result1.boxes.cls.cpu().numpy()
                class_ids2 = result2.boxes.cls.cpu().numpy()

                #unique_results = set()
                for box1, confidence1, class_id1 in zip(boxes1, confidences1, class_ids1):
                    for box2, confidence2, class_id2 in zip(boxes2, confidences2, class_ids2):
                        x_center1, y_center1 = get_center_coordinates(box1)
                        label1 = result1.names[int(class_id1)]

                        x_center2, y_center2 = get_center_coordinates(box2)
                        label2 = result2.names[int(class_id2)]

                        camera_coordinates1 = pixel_to_camera_coordinates(x_center1, y_center1, mtx, dist, default_depth, scale_factor=100)
                        camera_coordinates2 = pixel_to_camera_coordinates(x_center2, y_center2, mtx, dist, default_depth, scale_factor=100)

                        # Correction factor
                        correction_factor = 1.02
                        x_corrected1 = (camera_coordinates1[0] - (0.03 * 100) * correction_factor) if camera_coordinates1[0] >= 0 else (camera_coordinates1[0] + (0.03 * 100) * correction_factor)
                        y_corrected1 = (camera_coordinates1[1] - (0.03 * 100) * correction_factor) if camera_coordinates1[1] >= 0 else (camera_coordinates1[1] + (0.03 * 100) * correction_factor)
                        x_corrected2 = (camera_coordinates2[0] - (0.03 * 100) * correction_factor) if camera_coordinates2[0] >= 0 else (camera_coordinates2[0] + (0.03 * 100) * correction_factor)
                        y_corrected2 = (camera_coordinates2[1] - (0.03 * 100) * correction_factor) if camera_coordinates2[1] >= 0 else (camera_coordinates2[1] + (0.03 * 100) * correction_factor)

                        cv2.rectangle(frame, (int(box1[0]), int(box1[1])), (int(box1[2]), int(box1[3])), (0, 255, 0), 2)
                        cv2.circle(frame, (int(x_center1), int(y_center1)), 5, (0, 0, 255), -1)
                        cv2.putText(frame, label1, (int(box1[0]), int(box1[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                        cv2.rectangle(frame, (int(box2[0]), int(box2[1])), (int(box2[2]), int(box2[3])), (255, 0, 0), 2)
                        cv2.circle(frame, (int(x_center2), int(y_center2)), 5, (0, 0, 255), -1)
                        cv2.putText(frame, label2, (int(box2[0]), int(box2[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                        
                        
                        # object_info1 = (f"{label2},({int(x_corrected2)},{int(y_corrected2)},{50})")
                        # object_info2 = (f"{label1},({int(x_corrected1)},{int(y_corrected1)},{50})")
                        # unique_results.add(object_info1)
                        # unique_results.add(object_info2)
                        # print(unique_results)
                        unique_results[label2] = f"{label2},({int(x_corrected2)},{int(y_corrected2)},{50})"
                        unique_results[label1] = f"{label1},({int(x_corrected1)},{int(y_corrected1)},{50})"
            print(list(unique_results.values()))
            #             add_object_to_results(label2,[x_corrected2, y_corrected2])
            #             add_object_to_results(label1,[x_corrected1, y_corrected1])
            # print(list(unique_results.values()))  

            screen_width = 1500
            screen_height = 800
            window_width = screen_width // 2
            window_height = screen_height // 2
            cv2.namedWindow('YOLOv8 Detection',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('YOLOv8 Detection',window_width,window_height)
            cv2.imshow('YOLOv8 Detection', frame)
            cv2.waitKey(50)

            print("可選擇的物件和目標列表:")
            # for idx, item in enumerate(unique_results):
            #     print(f"{idx + 1}: {item}")
            for idx, item in enumerate(unique_results.values()):
                print(f"{idx + 1}: {item}")

            # 要求使用者選擇物件和目標
            object_choice = int(input("請選擇物件 (輸入數字): ")) - 1
            destination_choice = int(input("請選擇目標 (輸入數字): ")) - 1

            # 將選擇結果轉換成清單以便取用
            # unique_results_list = list(unique_results)
            unique_results_list = list(unique_results.values())
            # 確認選擇有效
            if 0 <= object_choice < len(unique_results_list) and 0 <= destination_choice < len(unique_results_list):
                object_list = unique_results_list[object_choice]
                destination_list = unique_results_list[destination_choice]
                
                # 將物件和目標資訊合併成一個字串
                data_to_send = f"{object_list};{destination_list}"

                # 將資料轉成手臂端可接收的格式
                formatted_object, formatted_destination = format_message(data_to_send)

                # 將資料傳給server
                if formatted_object and formatted_destination:
                    # send_data_to_server(formatted_object)
                    # send_data_to_server(formatted_destination)
                    combined_data = f"{formatted_object} {formatted_destination}"
                    send_data_to_server(combined_data)
                
            else:
                print("選擇無效，請重新運行程式並選擇有效的選項。")
            # screen_width = 1500
            # screen_height = 800
            # window_width = screen_width // 2
            # window_height = screen_height // 2
            # cv2.namedWindow('YOLOv8 Detection',cv2.WINDOW_NORMAL)
            # cv2.resizeWindow('YOLOv8 Detection',window_width,window_height)
            # cv2.imshow('YOLOv8 Detection', frame)
            # cv2.waitKey(50)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
