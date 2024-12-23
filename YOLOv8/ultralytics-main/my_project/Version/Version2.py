import cv2
import numpy as np
import socket
from ultralytics import YOLO
import os
import time

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# YOLO 模型
model1 = YOLO('numberv10.pt')  # 數字偵測
model2 = YOLO('cubev1.pt')  # 方塊顏色偵測

# 相機內參
mtx = np.array([[723.67637467, 0.0, 355.05402153], [0.0, 725.23755317, 241.22181201], [0.0, 0.0, 1.0]])
dist = np.array([-2.51361765e-01, 5.22063658e-01, -5.27509826e-04, -9.97607324e-06, -1.52992367e+00])
default_depth = 1.0
unique_results = {}

# 非極大值抑制函數
def apply_nms(boxes, confidences, threshold=0.5):
    # 應用 NMS 來過濾框
    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=threshold)
    
    # 確保 indices 是一維列表
    if len(indices) == 0:
        return [], []  # 如果沒有框，返回空列表
    elif isinstance(indices, tuple):  # 檢查是否為 tuple 結構
        indices = indices[0]
    
    # 提取索引並選取框和置信度
    selected_boxes = [boxes[i] for i in indices.flatten()]
    selected_confidences = [confidences[i] for i in indices.flatten()]
    return selected_boxes, selected_confidences

# 擷取畫面函數
def capture_frame(cap):
    ret, frame = cap.read()
    if ret:
        return frame
    else:
        return None
    
# 計算物件中心座標
def get_center_coordinates(box):
    # the coordinates of the bounding box
    # x1,y1 are the top-left corner of the bounding box
    # x2,y2 are the bottom-right corner of the bounding box
    x1, y1, x2, y2 = box
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    return x_center, y_center

# 將偵測到的中心座標從像素轉換到相機座標
def pixel_to_camera_coordinates(x_center, y_center):
    # 比例換算示例
    pixels_per_cm = 13.3  # 假設您已測量每厘米的像素數
    x_camera = x_center / pixels_per_cm
    y_camera = (480-y_center) / pixels_per_cm
    x_camera-=24
    y_camera-=18
    scale = 10
    x_camera = x_camera * scale
    y_camera = y_camera * scale
    return x_camera,y_camera#輸出結果已經轉換成機械臂座標了


# 輔助函數
def correct_coordinates(value, correction_factor):
    return (value - (0.03 * 100) * correction_factor) if value >= 0 else (value + (0.03 * 100) * correction_factor)

# 調整影像增強
def enhance_image(frame):
    return cv2.convertScaleAbs(frame, alpha=1, beta=10)

# 處理擷取的畫面
def process_frame(frame):
    global unique_results
    unique_results.clear()  # 每次偵測前清空 unique_results
    enhanced_frame = enhance_image(frame)

    # # 存儲模型1和模型2的檢測框和置信度
    # boxes = []
    # confidences = []
    # labels = []

    # 分別存儲模型1和模型2的檢測框、置信度和標籤
    boxes1, confidences1, labels1 = [], [], []
    boxes2, confidences2, labels2 = [], [], []

    # 模型1偵測
    results1 = model1(enhanced_frame, show=False, conf=0.8)
    for result1 in results1:
        boxes = result1.boxes.xyxy.cpu().numpy()
        confidences = result1.boxes.conf.cpu().numpy()
        class_ids = result1.boxes.cls.cpu().numpy()
        for box, confidence, class_id in zip(boxes, confidences, class_ids):
            boxes1.append([int(box[0]), int(box[1]), int(box[2] - box[0]), int(box[3] - box[1])])  # NMS 需要左上角座標和寬高格式
            confidences1.append(float(confidence))
            labels1.append(result1.names[int(class_id)])

    # 模型2偵測
    results2 = model2(enhanced_frame, show=False, conf=0.7)
    for result2 in results2:
        boxes = result2.boxes.xyxy.cpu().numpy()
        confidences = result2.boxes.conf.cpu().numpy()
        class_ids = result2.boxes.cls.cpu().numpy()
        for box, confidence, class_id in zip(boxes, confidences, class_ids):
            boxes2.append([int(box[0]), int(box[1]), int(box[2] - box[0]), int(box[3] - box[1])])
            confidences2.append(float(confidence))
            labels2.append(result2.names[int(class_id)])

    # 應用非極大值抑制
    selected_boxes1, selected_confidences1 = apply_nms(boxes1, confidences1, threshold=0.5)
    selected_boxes2, selected_confidences2 = apply_nms(boxes2, confidences2, threshold=0.5)

    # 繪製經過 NMS 過濾的框
    for box, confidence, label in zip(selected_boxes1, selected_confidences1, labels1):
        x, y, w, h = box
        x_center, y_center = get_center_coordinates([x, y, x + w, y + h])
        camera_coordinates = pixel_to_camera_coordinates(x_center, y_center)
        unique_results[label] = f"{label},({int(camera_coordinates[0])},{int(camera_coordinates[1])},{50})"
        
        # 顯示框和標籤
        cv2.rectangle(enhanced_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(enhanced_frame, (int(x_center), int(y_center)), 5, (0, 0, 255), -1)
        cv2.putText(enhanced_frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    for box, confidence, label in zip(selected_boxes2, selected_confidences2, labels2):
        x, y, w, h = box
        x_center, y_center = get_center_coordinates([x, y, x + w, y + h])
        camera_coordinates = pixel_to_camera_coordinates(x_center, y_center)
        unique_results[label] = f"{label},({int(camera_coordinates[0])},{int(camera_coordinates[1])},{50})"
        
        # 顯示框和標籤
        cv2.rectangle(enhanced_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(enhanced_frame, (int(x_center), int(y_center)), 5, (0, 0, 255), -1)
        cv2.putText(enhanced_frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    print("偵測結果:", list(unique_results.values()))
    return enhanced_frame

# 調整影像增強
def enhance_image(frame):
    return cv2.convertScaleAbs(frame, alpha=1, beta=20)

# Function that change the format befor sending messages  to the server(robotARM)
# Let the robotARM easier to break down the messages  
def format_message(data):
    try:
        # data_to_send = f"{object_list};{destination_list}"
        # formatted_object, formatted_destination = format_message(data_to_send)
        object_data, destination_data = data.split(';')
        
        # for example
        # object_list = unique_results_list[object_choice]
        # object_choice index "red" , object_list "red,(15,42,50)"
        # syntex : string.split(separator, maxsplit)

        # object information
        object_parts = object_data.split(',', 1)  # ['red','(15,42,50)']
        object_label = object_parts[0] # red 
        object_coordinates = object_parts[1] # (15,42,50)
        # strip removes specified characters from a string 
        x, y, z = object_coordinates.strip('()').split(',') # ['15','42','50']
        # retuen this formatted string and send to robotARM
        formatted_object = f"{object_label} {x} {y} {z}" # "red 15 42 50 "

        # destination information
        destination_parts = destination_data.split(',', 1)  
        destination_label = destination_parts[0]
        destination_coordinates = destination_parts[1] 
        dx, dy, dz = destination_coordinates.strip('()').split(',')
        formatted_destination = f"{destination_label} {dx} {dy} {dz}"

        return formatted_object, formatted_destination

    #return error messages 
    except ValueError as e:
        print(f"Error in format_message: {e}")
        return None, None

# Function that set up a TCP client
def send_data_to_server(data):

    # check out  the IP address and port of the server 
    server_ip = '192.168.203.176'
    server_port = 2000 

    # The beginning of TCP flow 
    # stage 1 : Create a socket TCP client 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # stage 2 : Try to connect to the server (server is listening ...)
        client.connect((server_ip, server_port))
        
        # stage 3 : Send data to the server (server had accept the connect require)
        # when using sockets for network communication ,data must be sent in bytes
        # Convert string into bytes object
        client.send(data.encode())
        client.settimeout(5)  # 設置 5 秒超時
        while True:
            try:
                response = client.recv(1024).decode()
                if response:
                    print("伺服器回應:", response)
                    if response == "complete":
                        print("接收完畢，結束連線。")
                        break
                else:
                    print("Server 斷開連接")
                    break
            except socket.timeout:
                print("接收數據超時，斷開連接")
                break
            time.sleep(10)  # 每次迭代延遲 100 毫秒

    #return error messages 
    except Exception as e:
        print("無法連接到伺服器:", e)
    
    finally:
        # The end of TCP flow
        # stage 5 : close the TCP service 
        print("結束連線")
        client.close()

# 主函數
def main():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Could not open video source.")
        exit()

    state = "capture"  # 初始狀態設為擷取影像
    object_choice = -1
    destination_choice = -1
    unique_results_list = []

    while True:
        if state == "capture":
            frame = capture_frame(cap)
            if frame is not None:
                frame = cv2.resize(frame, (640, 480))
                center_x = frame.shape[1] // 2
                center_y = frame.shape[0] // 2
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
                cv2.imshow('Press "s" to capture an image (or "q" to quit)', frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # 切換狀態到處理影像
                    state = "process"

        elif state == "process":
            # 對影像進行處理
            frame = process_frame(frame)
            cv2.imshow('YOLOv8 Detection', frame)
            cv2.waitKey(50)

            print("可選擇的物件和目標列表:")
            unique_results_list = list(unique_results.values())
            for idx, item in enumerate(unique_results_list):
                print(f"{idx + 1}: {item}")

            # 切換狀態到等待輸入
            state = "input"

        elif state == "input":
            # 確保輸入不會阻塞影像擷取
            try:
                object_choice = int(input("請選擇物件 (輸入數字): ")) - 1
                destination_choice = int(input("請選擇目標 (輸入數字): ")) - 1
            except ValueError:
                print("輸入無效，請輸入數字")
                continue

            if 0 <= object_choice < len(unique_results_list) and 0 <= destination_choice < len(unique_results_list):
                state = "send"
            else:
                print("選擇無效，請重新選擇有效的選項。")

        elif state == "send":
            object_list = unique_results_list[object_choice]
            destination_list = unique_results_list[destination_choice]

            # 格式化並傳送資料
            data_to_send = f"{object_list};{destination_list}"
            formatted_object, formatted_destination = format_message(data_to_send)

            if formatted_object and formatted_destination:
                combined_data = f"{formatted_object} {formatted_destination}"
                print("Data sent to server.")
                send_data_to_server(combined_data)
                
            
            # 重置狀態到擷取影像
            state = "capture"
            object_choice = -1
            destination_choice = -1
            unique_results_list.clear()

    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
