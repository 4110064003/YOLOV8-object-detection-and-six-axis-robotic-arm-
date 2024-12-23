import cv2
import socket
import numpy as np
from ultralytics import YOLO
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# number detect
model1 = YOLO('numberv10.pt')
# cube detect
model2 = YOLO('cubev1.pt')

#Camera intrinsic matrix in pixels (example values, need to be calibrated for your camera)
mtx = np.array([
     [723.67637467, 0.0, 355.05402153],
     [0.0, 725.23755317, 241.22181201],
     [0.0, 0.0, 1.0]
])


dist = np.array([-2.51361765e-01, 5.22063658e-01, -5.27509826e-04, -9.97607324e-06, -1.52992367e+00])  # Distortion coefficients


# Define a default depth value in meters (we don't have depth information)
default_depth = 0.9

# Function that calculate detected object's center coordinate in pixel
def get_center_coordinates(box):
    x1, y1, x2, y2 = box
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    return x_center, y_center

# Function that turns the detected object's center point coordinates from pixel to camera
def pixel_to_camera_coordinates(x_center, y_center):
    x_camera = (320-x_center)*22/19
    y_camera = (y_center-240)*22/19
    return x_camera,y_camera

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
    server_ip = '192.168.145.176'
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
        
        # stage 4 : Client receive the response from server after successfully sending data 
        response = client.recv(1024).decode()
        # Print out the response 
        print("伺服器回應:", response)

    #return error messages 
    except Exception as e:
        print("無法連接到伺服器:", e)
    
    finally:
        # The end of TCP flow
        # stage 5 : close the TCP service 
        client.close()
        
unique_results = {}

def main():
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Could not open video source.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        height, width, _ = frame.shape
        center_x = width // 2
        center_y = height // 2
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
        text = f"Center: ({center_x}, {center_y})"
        cv2.putText(frame, text, (center_x + 10, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.imshow('Press "s" to capture an image (or "q" to quit)', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            unique_results.clear()
            # Run detection once on pressing 's'
            results1 = model1(frame, show=False, conf=0.8)
            results2 = model2(frame, show=False, conf=0.8)

            # Check if any objects were detected
            boxes1_detected = any(len(result.boxes.xyxy) > 0 for result in results1)
            boxes2_detected = any(len(result.boxes.xyxy) > 0 for result in results2)

            if not boxes1_detected and not boxes2_detected:
                print("No objects detected on the interface. Please try again...")
                continue  # Continue to the next frame for detection

            print("Objects detected. Proceeding with further processing...")

            for result1, result2 in zip(results1, results2):
                boxes1 = result1.boxes.xyxy.cpu().numpy()
                boxes2 = result2.boxes.xyxy.cpu().numpy()
                confidences1 = result1.boxes.conf.cpu().numpy()
                confidences2 = result2.boxes.conf.cpu().numpy()
                class_ids1 = result1.boxes.cls.cpu().numpy()
                class_ids2 = result2.boxes.cls.cpu().numpy()

                for box1, confidence1, class_id1 in zip(boxes1, confidences1, class_ids1):
                    for box2, confidence2, class_id2 in zip(boxes2, confidences2, class_ids2):
                        x_center1, y_center1 = get_center_coordinates(box1)
                        label1 = result1.names[int(class_id1)]
                        x_center2, y_center2 = get_center_coordinates(box2)
                        label2 = result2.names[int(class_id2)]

                        x_camera1,y_camera1 = pixel_to_camera_coordinates(x_center1, y_center1)
                        x_camera2,y_camera2 = pixel_to_camera_coordinates(x_center2, y_center2)

                        cv2.rectangle(frame, (int(box1[0]), int(box1[1])), (int(box1[2]), int(box1[3])), (0, 255, 0), 2)
                        cv2.circle(frame, (int(x_center1), int(y_center1)), 5, (0, 0, 255), -1)
                        cv2.putText(frame, label1, (int(box1[0]), int(box1[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                        cv2.rectangle(frame, (int(box2[0]), int(box2[1])), (int(box2[2]), int(box2[3])), (255, 0, 0), 2)
                        cv2.circle(frame, (int(x_center2), int(y_center2)), 5, (0, 0, 255), -1)
                        cv2.putText(frame, label2, (int(box2[0]), int(box2[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                        # unique_results[label2] = f"{label2},({int(camera_coordinates2[0])},{int(camera_coordinates2[1])},{50})"
                        # unique_results[label1] = f"{label1},({int(camera_coordinates1[0])},{int(camera_coordinates1[1])},{50})"
                        unique_results[label2] = f"{label2},({int(x_camera2)},{int(y_camera2 )},{50})"
                        unique_results[label1] = f"{label1},({int(x_camera1)},{int(y_camera1)},{50})"
            print(list(unique_results.values()))
            
            cv2.imshow('YOLOv8 Detection', frame)
            cv2.waitKey(20)

            print("可選擇的物件和目標列表:")
            for idx, item in enumerate(unique_results.values()):
                print(f"{idx + 1}: {item}")

            # Ask user to choose which object they want to grab and which destination do they want to place
            object_choice = int(input("請選擇物件 (輸入數字): ")) - 1
            destination_choice = int(input("請選擇目標 (輸入數字): ")) - 1

            # Turns every item in  unique_results dictionary into a list
            unique_results_list = list(unique_results.values())

            if 0 <= object_choice < len(unique_results_list) and 0 <= destination_choice < len(unique_results_list):
                # Reach the object information and destination information by searching with index 
                object_list = unique_results_list[object_choice]
                destination_list = unique_results_list[destination_choice]
                
                # combine object_list with destination_list and turned into a formatted-string 
                data_to_send = f"{object_list};{destination_list}"

                # change the format befor sending messages  to the server(robotARM) 
                formatted_object, formatted_destination = format_message(data_to_send)

                # combine formatted_object with formatted_destination and turned into a formatted-string send to server 
                if formatted_object and formatted_destination:
                    combined_data = f"{formatted_object} {formatted_destination}"
                    send_data_to_server(combined_data)
                
            else:
                print("選擇無效，請重新運行程式並選擇有效的選項。")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
