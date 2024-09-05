# import cv2

# cap = cv2.VideoCapture(1)
# if not cap.isOpened():
# 	print("Error")
	
	
# ret,frame = cap.read()

# if ret:
# 	cv2.imwrite(frame)
# 	print(frame)
# else:
# 	print("Error")
# cap.release()

import cv2

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Error: Could not open video capture device.")
    exit()

ret, frame = cap.read()
if ret:
    try:
        cv2.imwrite("frame.jpg", frame)  # Specify a filename
        print("Frame saved to frame.jpg")
    except Exception as e:
        print(f"Error saving frame: {e}")
else:
    print("Error: Could not read frame from video capture device.")

cap.release()