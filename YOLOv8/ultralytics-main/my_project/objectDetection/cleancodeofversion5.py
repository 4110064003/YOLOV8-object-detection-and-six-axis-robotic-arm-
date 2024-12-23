import cv2
import socket
import numpy as np
from ultralytics import YOLO
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

#number detect
model1 = YOLO('numberv10.pt')
#cube detect
model2 = YOLO('cubev1.pt')

# Camera intrinsic matrix in pixels (example values, need to be calibrated for your camera)
mtx = np.array([
    [723.67637467, 0.0, 355.05402153],
    [0.0, 725.23755317, 241.22181201],
    [0.0, 0.0, 1.0]
]) 

dist = np.array([-2.51361765e-01, 5.22063658e-01, -5.27509826e-04,  -9.97607324e-06, -1.52992367e+00])  # Distortion coefficients

# Define a default depth value in meters (we don't have depth information)
default_depth = 1.0

# Function that calculate dictected object's center coordinate in pixel
def get_center_coordinates(box):
    # the coordinates of the bounding box
    # x1,y1 are the top-left corner of the bounding box
    # x2,y2 are the bottom-right corner of the bounding box
    x1, y1, x2, y2 = box
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2
    return x_center, y_center

# Function that turns the dectected object's center point coordinates from pixel to camera
def pixel_to_camera_coordinates(x_center, y_center, mtx, dist, default_depth,scale_factor=1.0):

    # Convert pixel coordinates to normalized camera coordinates
    uv_point = np.array([[x_center, y_center]], dtype=np.float32).reshape(-1, 1, 2)
    uv_point = cv2.undistortPoints(uv_point, mtx, dist, P=mtx)

    # Homogeneous coordinates
    uv_point = np.append(uv_point[0][0], [1.0])  

    # Assume the depth value (z) is set to a default value
    z = default_depth

    # Convert to camera coordinates
    camera_coordinates = np.dot(np.linalg.inv(mtx), uv_point * z)

    return (camera_coordinates * scale_factor).flatten()

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

# Function that check the duplications in unique_results 
def add_object_to_results(label, x_corrected, y_corrected, z=50, threshold=10):
    # There might have two kinds of situation that we want to avoid 
    # First : one object was recognized into two kinds of different classes , ex : "blue , (15,42,50)" "circle1 ,(15,42,50)" 
    # Second : one object was recognized into one class but with different coordinates , ex : "blue , (15,42,50)" "blue , (5,10,50)"
    # We can solve this kid of problem either rebuilt the YOLO model to better performance or just built a filter avoied duplications.
    
    # Unique_results is a dictionary , we can seprerate the key and value of every items in it
    for key, value in unique_results.items():
        _, coords = value.split(',')
        # coords.strip('()').split(',') for example changes "(10, 20, 30)" into a list ["10","20","30"]
        #map(int , ...) changes ["10","20","30"] into [10 ,20 ,30] and unpacked into three variables
        x_existing, y_existing, z_existing = map(int, coords.strip('()').split(','))

        # Calculte the distance between new iteams and the original items in the dictionary
        distance = math.sqrt((x_corrected - x_existing) ** 2 + (y_corrected - y_existing) ** 2)

        # If the distance is too close , we will keep the origin items
        if distance < threshold:
            print(f"Found similar object: {label} at ({x_corrected}, {y_corrected}) is close to {key} at ({x_existing}, {y_existing})")
            return
    
    # If don't ,we keep and add new items into unique_results
    unique_results[label] = f"{label},({int(x_corrected)},{int(y_corrected)},{z})"  

def enhance_image(frame):
    # 調整對比度和亮度 (alpha: 對比度, beta: 亮度)
    enhanced_frame = cv2.convertScaleAbs(frame, alpha=1, beta=10)
    return enhanced_frame        
# declared a dictionary named unique_results{"key" : "value"}
# for example :
# # unique_results = {
#     "red": "red,(15,42,50)",
#     "circle1": "circle1,(10,20,50)"
# }

unique_results = {}
def main():
    # Open a video capture object (source=1 indicates the first camera)
    cap = cv2.VideoCapture(1)

    # Check whether video capture object open successfully
    if not cap.isOpened():
        print("Error: Could not open video source.")
        exit()# Exit the loop if the frame capture fails

    continue_detection = True
    # Check whether 
    while  continue_detection:
        # ret is a boolen value indication whether the frame was successfully read 
        # frame contains the image data for the current frame.this can be prossed ,displayed or saved
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break
        
        # This part is only resizing the display window on our computer ,not neccessary 
        # screen_width = 1500
        # screen_height = 800
        # window_width = screen_width // 2
        # window_height = screen_height // 2
        # cv2.namedWindow('Press "s" to capture an image (or "q" to quit)',cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Press "s" to capture an image (or "q" to quit)',window_width,window_height)
        
        # Display the frame that the camera captured real time 
        cv2.imshow('Press "s" to capture an image (or "q" to quit)', frame)
        

        key = cv2.waitKey(1) & 0xFF
        # Exit on pressing 'q'
        if key == ord('q'):
            break

        # capture the image on pressing 's'
        elif key == ord('s'):

            enhanced_frame = enhance_image(frame)
            correction_factor = 1.02
            results1 = model1(enhanced_frame, show=False, conf=0.8)
            for result1 in results1:
                boxes1 = result1.boxes.xyxy.cpu().numpy()
                confidences1 = result1.boxes.conf.cpu().numpy()
                class_ids1 = result1.boxes.cls.cpu().numpy()

                for box1, confidence1, class_id1 in zip(boxes1, confidences1, class_ids1):
                    x_center1, y_center1 = get_center_coordinates(box1)
                    label1 = result1.names[int(class_id1)]

                    camera_coordinates1 = pixel_to_camera_coordinates(x_center1, y_center1, mtx, dist, default_depth, scale_factor=100)

                    # 校正
                    x_corrected1 = (camera_coordinates1[0] - (0.03 * 100) * correction_factor) if camera_coordinates1[0] >= 0 else (camera_coordinates1[0] + (0.03 * 100) * correction_factor)
                    y_corrected1 = (camera_coordinates1[1] - (0.03 * 100) * correction_factor) if camera_coordinates1[1] >= 0 else (camera_coordinates1[1] + (0.03 * 100) * correction_factor)

                    # 顯示結果
                    cv2.rectangle(enhanced_frame, (int(box1[0]), int(box1[1])), (int(box1[2]), int(box1[3])), (0, 255, 0), 2)
                    cv2.circle(enhanced_frame, (int(x_center1), int(y_center1)), 5, (0, 0, 255), -1)
                    cv2.putText(enhanced_frame, label1, (int(box1[0]), int(box1[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    unique_results[label1] = f"{label1},({int(x_corrected1)},{int(y_corrected1)},{50})"

            # 運行第二個模型並處理偵測結果
            results2 = model2(enhanced_frame, show=False, conf=0.7)
            for result2 in results2:
                boxes2 = result2.boxes.xyxy.cpu().numpy()
                confidences2 = result2.boxes.conf.cpu().numpy()
                class_ids2 = result2.boxes.cls.cpu().numpy()

                for box2, confidence2, class_id2 in zip(boxes2, confidences2, class_ids2):
                    x_center2, y_center2 = get_center_coordinates(box2)
                    label2 = result2.names[int(class_id2)]

                    camera_coordinates2 = pixel_to_camera_coordinates(x_center2, y_center2, mtx, dist, default_depth, scale_factor=100)

                    # 校正
                    x_corrected2 = (camera_coordinates2[0] - (0.03 * 100) * correction_factor) if camera_coordinates2[0] >= 0 else (camera_coordinates2[0] + (0.03 * 100) * correction_factor)
                    y_corrected2 = (camera_coordinates2[1] - (0.03 * 100) * correction_factor) if camera_coordinates2[1] >= 0 else (camera_coordinates2[1] + (0.03 * 100) * correction_factor)

                    # 顯示結果
                    cv2.rectangle(enhanced_frame, (int(box2[0]), int(box2[1])), (int(box2[2]), int(box2[3])), (255, 0, 0), 2)
                    cv2.circle(enhanced_frame, (int(x_center2), int(y_center2)), 5, (0, 0, 255), -1)
                    cv2.putText(enhanced_frame, label2, (int(box2[0]), int(box2[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    unique_results[label2] = f"{label2},({int(x_corrected2)},{int(y_corrected2)},{50})"

            #unique_results.values() will return like dict_values(['red,(15,42,50)', 'circle1,(10,20,50)'])
            #list(unique_results.values()) will be like ['red,(15,42,50)', 'circle1,(10,20,50)']
            print(list(unique_results.values()))

            # # This part is only resizing the display window on our computer ,not neccessary 
            # screen_width = 1500
            # screen_height = 800
            # window_width = screen_width // 2
            # window_height = screen_height // 2
            # cv2.namedWindow('YOLOv8 Detection',cv2.WINDOW_NORMAL)
            # cv2.resizeWindow('YOLOv8 Detection',window_width,window_height)

            # Display the frame that the camera captured with detected information  
            cv2.imshow('YOLOv8 Detection', enhanced_frame)
            cv2.waitKey(50)
            
            # Print out every single item the camera captured && model detected
            # Putting an index before every item so user can easily choose the matching ones  
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
