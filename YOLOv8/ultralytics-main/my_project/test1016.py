import cv2
import socket
import numpy as np
from ultralytics import YOLO
import os
import re
from itertools import combinations
import statistics

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# number detect
model1 = YOLO('numberv10.pt')
# cube detect
model2 = YOLO('cubev1.pt')

# Camera intrinsic matrix in pixels (example values, need to be calibrated for your camera)
mtx = np.array([
    [723.67637467, 0.0, 355.05402153],
    [0.0, 725.23755317, 241.22181201],
    [0.0, 0.0, 1.0]
])

dist = np.array([-2.51361765e-01, 5.22063658e-01, -5.27509826e-04, -9.976e-04, -1.36587518e+00])

# Placeholder for object and destination recognition results
recognized_objects = []
recognized_destinations = []

img_nums=4
for i in range(1,img_nums):
    # Load an image for object detection
    image_path = r"D:\ultralytics-main\my_project\num_img\%d.jpg" % i  # Replace with your image path
    image = cv2.imread(image_path)

    # Perform detection on the image
    results1 = model1(image)  # Detect numbers
    results2 = model2(image)  # Detect cubes

    # Placeholder for object and destination recognition results
    recognized_objects = []
    recognized_destinations = []

    # Extract recognized objects and destinations from detection results
    for result in results2:  # Assuming result contains bounding boxes and class names
        for detection in result.boxes:
            class_name = detection.cls
            label2 = result.names[int(class_name)]
            coordinates = detection.xyxy
            recognized_objects.append(f"{label2}")

    for result in results1:  # Assuming result contains bounding boxes and class names
        for detection in result.boxes:
            class_name = detection.cls
            label1 = result.names[int(class_name)]
            coordinates = detection.xyxy
            recognized_destinations.append(f"{label1}")

    # # Example recognized results for demonstration purposes
    # recognized_destinations = ["circle1", "circle2", "triangle3", "triangle4"]

    # Step 1: Extract numerical values from recognized destination classes
    numbers = []
    for dest in recognized_destinations:
        match = re.search(r'\d+', dest)  # Extract digits from the string
        if match:
            numbers.append(int(match.group()))

    # Step 2: Calculate all possible two-number combinations and their sums
    comb_sum_list = []
    comb_combinations = []
    for comb in combinations(numbers, 2):
        comb_sum = sum(comb)
        comb_sum_list.append(f"{comb_sum}({comb[0]}+{comb[1]})")
        comb_combinations.append(comb)

    # Step 3: Create the final list with unique sums
    unique_comb_sum_list = list(set(comb_sum_list))  # To ensure uniqueness
    unique_comb_sum_list.sort()  # Sort for easier readability

    # Display the result
    print("All possible two-number combinations and their sums:")
    print(unique_comb_sum_list)

    # Calculate the median of the sums
    if unique_comb_sum_list:
        median_value = statistics.median(unique_comb_sum_list)
        print(f"Median of all possible two-number combinations and their sums: {median_value}")

    # Display the result
    print("All possible two-number combinations and their sums:")
    print([f"{comb_sum}({comb[0]}+{comb[1]})" for comb, comb_sum in zip(comb_combinations, comb_sum_list)])

# Process the image
process_image(image)

    # The rest of your code involving socket communication or further processing can be added below

    # Example socket communication (for sending data to the robotic arm)
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_socket.bind(('localhost', 12345))
    # server_socket.listen(1)
    # print("Waiting for connection...")
    # conn, addr = server_socket.accept()
    # print(f"Connected by {addr}")

    # Send the unique combination sums to the client
    # conn.sendall(str(unique_comb_sum_list).encode())
    # conn.close()
