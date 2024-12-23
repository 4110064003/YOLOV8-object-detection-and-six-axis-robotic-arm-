import cv2
import numpy as np
import socket
from ultralytics import YOLO
import os
import time
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsScene, QGraphicsView,QLabel
from PyQt5.QtWidgets import QListWidget, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from UI import Ui_MainWindow

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# YOLO 模型
model1 = YOLO('numberv10.pt')  # 數字偵測
model2 = YOLO('cubev1.pt')  # 方塊顏色偵測

# 相機內參
mtx = np.array([[723.67637467, 0.0, 355.05402153], [0.0, 725.23755317, 241.22181201], [0.0, 0.0, 1.0]])
dist = np.array([-2.51361765e-01, 5.22063658e-01, -5.27509826e-04, -9.97607324e-06, -1.52992367e+00])
default_depth = 1.0
unique_results = {}
unique_objects = {}
unique_destinations = {}

# UI 介面類別
class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,cap, objects_list, destinations_list):
        super().__init__()
        self.setupUi(self)

        # 打開攝像頭
        # self.cap = cv2.VideoCapture(1) 
        self.cap = cap

        # 儲存當前的影像
        self.current_frame = None

        # 設置計時器來定期更新影像
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 每 30 毫秒更新一次

        # 加載 YOLOv8 模型
        self.model1 = YOLO('numberv10.pt')  # 數字偵測
        self.model2 = YOLO('cubev1.pt')  # 方塊顏色偵測

        self.videoLabel.setScaledContents(True)# 啟用 QLabel 的縮放功能
        self.imageLabel.setScaledContents(True)

        # 連接按鈕事件
        self.startButton.clicked.connect(self.capture_image)
        self.confirmButton.clicked.connect(self.confirm_selection)
        self.closeButton.clicked.connect(self.close_application)

        # 初始化偵測結果列表
        self.objects_list = objects_list
        self.destinations_list = destinations_list

        self.state_machine = StateMachine(self)

        for obj in self.objects_list:
            self.ObjectListWidget.addItem(obj)

        for tgt in self.destinations_list:
            self.TargetListWidget.addItem(tgt)
        
    def confirm_selection(self):
        selected_object = self.ObjectListWidget.currentItem()
        selected_target = self.TargetListWidget.currentItem()

        if selected_object and selected_target:
            self.selected_object = selected_object.text()
            self.selected_target = selected_target.text()
            QMessageBox.information(self, "選擇結果", f"您選擇了物件: {self.selected_object}\n目標: {self.selected_target}")
            
            # 通知狀態機選擇已完成
            self.state_machine.set_input_data(self.selected_object,self.selected_target)
            #self.close()
        else:
            QMessageBox.warning(self, "錯誤", "請選擇物件和目標！")

    def update_frame(self):
        # 讀取攝像頭影像
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame  # 儲存當前影像
            if self.current_frame is not None:
                frame = cv2.resize(self.current_frame, (640, 480))
                center_x = self.current_frame.shape[1] // 2
                center_y = self.current_frame.shape[0] // 2
                cv2.circle(self.current_frame, (center_x, center_y), 5, (0, 0, 255), -1)
            # 將影像從 BGR 轉換為 RGB 格式
            rgb_image = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w

            # 將 OpenCV 影像轉換為 Qt 支援的 QImage
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)

            # 將 QPixmap 設置到 QLabel 上
            self.videoLabel.setPixmap(pixmap)

    def update_detection_lists(self):
        global unique_objects, unique_destinations
        self.objects_list = list(unique_objects.values())
        self.destinations_list = list(unique_destinations.values())
        self.ObjectListWidget.clear()
        self.TargetListWidget.clear()
        for obj in self.objects_list:
            self.ObjectListWidget.addItem(obj)
        for tgt in self.destinations_list:
            self.TargetListWidget.addItem(tgt)


    def capture_image(self):
        if self.current_frame is not None:

            # 影像增強
            enhanced_frame = self.enhance_image(self.current_frame)

            # 儲存影像增強後的影像為檔案
            cv2.imwrite('captured_image.jpg', enhanced_frame)
            # print("影像已擷取並儲存為 'captured_image.jpg'")
            # # 顯示影像到新視窗
            # cv2.imshow("Captured Image", self.current_frame)

            # results = self.model(enhanced_frame)# 使用 YOLOv8 進行目標辨識
            # result_frame = results[0].plot()# 在辨識結果上繪製邊框和標籤

            global unique_objects, unique_destinations
            unique_results.clear()
            unique_objects.clear()
            unique_destinations.clear()

            # 分別存儲模型1和模型2的檢測框、置信度和標籤
            boxes1, confidences1, labels1 = [], [], []
            boxes2, confidences2, labels2 = [], [], []

            # 模型1偵測
            results1 = self.model1(enhanced_frame, show=False, conf=0.85)
            for result1 in results1:
                boxes = result1.boxes.xyxy.cpu().numpy()
                confidences = result1.boxes.conf.cpu().numpy()
                class_ids = result1.boxes.cls.cpu().numpy()
                for box, confidence, class_id in zip(boxes, confidences, class_ids):
                    boxes1.append([int(box[0]), int(box[1]), int(box[2] - box[0]), int(box[3] - box[1])])  # NMS 需要左上角座標和寬高格式
                    confidences1.append(float(confidence))
                    labels1.append(result1.names[int(class_id)])

            # 模型2偵測
            results2 = self.model2(enhanced_frame, show=False, conf=0.7)
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
                cv2.rectangle(enhanced_frame, (x, y), (x + w, y + h), (142, 26, 255), 2)
                cv2.circle(enhanced_frame, (int(x_center), int(y_center)), 5, (0, 0, 255), -1)
                cv2.putText(enhanced_frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (142, 26, 255), 2)

            for box, confidence, label in zip(selected_boxes2, selected_confidences2, labels2):
                x, y, w, h = box
                x_center, y_center = get_center_coordinates([x, y, x + w, y + h])
                camera_coordinates = pixel_to_camera_coordinates(x_center, y_center)
                unique_results[label] = f"{label},({int(camera_coordinates[0])},{int(camera_coordinates[1])},{50})"
                
                # 顯示框和標籤
                cv2.rectangle(enhanced_frame, (x, y), (x + w, y + h), (142, 26, 255), 2)
                cv2.circle(enhanced_frame, (int(x_center), int(y_center)), 5, (0, 0, 255), -1)
                cv2.putText(enhanced_frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (142, 26, 255), 2)
            
            #object 和 destination 物件分別存入unique_objects 和 unique_destinations 當中
            for result in results1:
                for box, cls in zip(result.boxes.xyxy.cpu().numpy(), result.boxes.cls.cpu().numpy()):
                    label = result.names[int(cls)]
                    x_center, y_center = pixel_to_camera_coordinates((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
                    unique_destinations[label] = f"{label},({int(x_center)},{int(y_center)},50)"

            for result in results2:
                for box, cls in zip(result.boxes.xyxy.cpu().numpy(), result.boxes.cls.cpu().numpy()):
                    label = result.names[int(cls)]
                    x_center, y_center = pixel_to_camera_coordinates((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
                    unique_objects[label] = f"{label},({int(x_center)},{int(y_center)},50)"
            
            if enhanced_frame is not None:
                # 將辨識結果影像轉換為 QImage 格式
                rgb_result_image = cv2.cvtColor(enhanced_frame,cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_result_image.shape
                bytes_per_line = ch * w
                qt_result_image = QImage(rgb_result_image, w, h, bytes_per_line, QImage.Format_RGB888)
                result_pixmap = QPixmap.fromImage(qt_result_image)

                # 將 QPixmap 設置到 QLabel 上
                self.imageLabel.setPixmap(result_pixmap)
                self.imageLabel.setScaledContents(True)# 啟用 QLabel 的縮放功能
            else:
                print("No frame available for processing.")
                
        self.objects_list = list(unique_objects.values())
        self.destinations_list = list(unique_destinations.values())
        self.update_detection_lists()

        print("偵測結果:", list(unique_results.values()))
        #return enhanced_frame

    # 調整影像增強
    # def enhance_image(self, frame):
    #     return cv2.convertScaleAbs(frame, alpha=1, beta=20)

    #直方圖均衡化:透過調整影像的像素值分布來增強對比度，提升暗區的細節。
    # def enhance_image(self, frame):
    #     # 自動調整亮度與對比度
    #     lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    #     l, a, b = cv2.split(lab)

    #     # 自適應直方圖均衡化
    #     clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    #     l = clahe.apply(l)

    #     lab = cv2.merge((l, a, b))
    #     enhanced_frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    #     return enhanced_frame

    def enhance_image(self,frame,brightness_boost=15):

        # 將影像轉換為灰階
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 將影像轉換為 LAB 色彩空間
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # 使用高斯模糊估計光線分布
        #blurred = cv2.GaussianBlur(gray, (101, 101), 0)
        blurred = cv2.GaussianBlur(l, (101, 101), 0)

        # 計算遮罩來校正亮度
        mask = np.mean(blurred) / (blurred + 1e-5)  # 防止除以 0
        mask = np.clip(mask, 0.5, 2)  # 限制調整幅度

        # 將遮罩應用於原始影像
        # enhanced_frame = np.zeros_like(frame)
        # for c in range(3):  # 對每個通道進行校正
        #     enhanced_frame[:, :, c] = frame[:, :, c] * mask

        # enhanced_frame+=brightness_boost
        # enhanced_frame = np.clip(enhanced_frame,0,255)

        # 應用遮罩和亮度增強
        enhanced_l = l * mask
        enhanced_l += brightness_boost
        enhanced_l = np.clip(enhanced_l, 0, 255).astype(np.uint8)

        # 合併增強後的亮度與原始的色彩通道
        lab = cv2.merge((enhanced_l, a, b))

        # 轉回 BGR 色彩空間
        enhanced_frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        return enhanced_frame

    def close_application(self):
        # 顯示確認對話框（可選）
        reply = QMessageBox.question(
            self, "退出程式", "你確定要關閉程式嗎？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            print("程式結束")
            self.close()  # 關閉主視窗
            sys.exit(0)  # 退出程式


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

def initialize_camera(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Camera with index {camera_index} could not be opened.")
        return None
    return cap

def send_to_server(object_choice, destination_choice):
    if object_choice is None or destination_choice is None:
        print("Error: Object or destination is not selected.")
        return
    formatted_object, formatted_destination = format_message(f"{object_choice};{destination_choice}")
    combined_data = f"{formatted_object} {formatted_destination}"
    print("Data sent to server.")
    send_data_to_server(combined_data)

class StateMachine:
    def __init__(self, main_window):
        self.state = "capture"
        self.main_window = main_window #StateMachine 透過 self.main_window 訪問主視窗的屬性和方法
        self.selected_object = None
        self.selected_target = None
    
    def set_input_data(self,selected_object,selected_target):
        # 更新選擇的物件和目標
        self.selected_object = selected_object
        self.selected_target = selected_target
        if self.state == "capture":
            self.run_next_input_step()

    def run_next_input_step(self):
        if self.selected_object and self.selected_target:
            print(f"處理已選物件:{self.selected_object}和目標:{self.selected_target}")

            send_to_server(self.selected_object,self.selected_target)

            self.state = "capture"
            print("已完成,狀態返回至 'capture' ")
        else:
            print("等待使用者選擇物件和目標")

    def run(self):
        if self.state == "capture":
            self.main_window.update_frame()
        # elif self.state == "process":
        #     self.main_window.capture_image()
        #     # self.state = "input"
        # elif self.state == "input":
        #     print("進入input 狀態，等待使用者選擇物件和目標")
        #     # selected_object = self.state_machine.selected_object
        #     # selected_target = self.state_machine.selected_target
        #     selected_object = self.main_window.selected_object #selected_object 是訊息本身
        #     selected_target = self.main_window.selected_target #selected_target 是訊息本身

        #     # Find the index of the selected object(object_choice) and target(destination_choice)
        #     object_choice = self.objects_list.index(selected_object) if selected_object in objects_list else -1
        #     destination_choice = self.destinations_list.index(selected_target) if selected_target in destinations_list else -1
        #     print(object_choice)

        #     if 0 <= object_choice < len(self.objects_list) and 0 <= destination_choice < len(self.destinations_list):
        #         send_to_server(selected_object, selected_target)
        #         self.state = "capture"
        #     else:
        #         print("選擇無效，請重新選擇有效的選項。")
        else:
            print("Unknown state.")



def main():
    app = QApplication(sys.argv)
    cap = initialize_camera(1)#攝像頭初始化並傳MainWindow
    if not cap:
        print("Error: Could not initialize the camera.")
        return

    objects_list, destinations_list = [], []
    unique_results.clear()

    main_window = MainWindow(cap, objects_list, destinations_list)
    main_window.show()

    state_machine = StateMachine(main_window)

    while True:
        state_machine.run()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    sys.exit(app.exec_())

    
if __name__ == "__main__":
    main()
