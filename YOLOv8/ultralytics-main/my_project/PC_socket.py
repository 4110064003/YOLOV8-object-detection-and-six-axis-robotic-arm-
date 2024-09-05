from ultralytics import YOLO
import socket
import cv2
cap = cv2.VideoCapture(0)

ESP32_IP = '192.168.1.100'
ESP32_PORT = 1000

client_socket = socket.socket(socket.AF_INET,socket.SOCKET_STREAM)#create socket object
client_socket.connect((ESP32_IP,ESP32_PORT))#connect to EPS32

def send_command_to_esp32(command):
    client_socket.sendall(command.encode())

model = YOLO('best (13).pt')#Load a pretrained YOLOv8s model

def get_mask_center(mask):#calculate the center of mask
    moments = cv2.moments(mask)
    cx = int(moments['m10']/moments['m00'])
    cy = int(moments['m01']/moments['m00'])
    return cx,cy

while True:
    ret,frame = cap.read()
    if not ret:
        break
    
    results = model(source=frame,show=True,conf=0.3,save=True)#Run inference on the source 
    red_mask = None
    circle1_mask = None
    for result in results:#results is a image , result include many boxes for detect object
        for detection in result.masks.data:#detection include confidence and class_id
            confidence = detection.conf
            class_id = detection.cls
            if detection.confidence>0.3:
                mask = detection.mask.cpu().numpy()
                if class_id == 'red':
                    red_mask = mask
                elif class_id == 'circle1':
                    circle1_mask = mask
                else:
                    continue
    if red_mask is not None and circle1_mask is not None:
        red_center = get_mask_center(red_mask)
        circle1_center = get_mask_center(circle1_mask)
        command = f'MOVE_RED_BOX{red_center[0]}{red_center[1]} TO {circle1_center[0]}{circle1_center[1]}'#f-string format
        send_command_to_esp32(command)

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

client_socket.close()