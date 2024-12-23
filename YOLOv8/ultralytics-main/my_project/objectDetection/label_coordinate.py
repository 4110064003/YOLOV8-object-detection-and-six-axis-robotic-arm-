#目標檢測-拍攝照片後框取目標並繪製圖像中心像素座標
from ultralytics import YOLO
import cv2

# Load a pretrained YOLOv8 model
model = YOLO('numberv10.pt')

# Open a video capture object (source=1 indicates the first camera)
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    # Display the frame to provide visual feedback to the user
    cv2.imshow('Press "s" to capture an image (or "q" to quit)', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):  # 's' key is pressed
        # Run inference on the frame
        results = model(frame, show=False)  # Run inference without showing the image

        # Process each result
        for result in results:
            # Each result contains boxes, scores, and class ids
            boxes = result.boxes.xyxy.cpu().numpy()  # Get bounding box coordinates
            confidences = result.boxes.conf.cpu().numpy()  # Get confidence scores
            class_ids = result.boxes.cls.cpu().numpy()  # Get class ids

            # Iterate over each detection
            for box, confidence, class_id in zip(boxes, confidences, class_ids):
                x1, y1, x2, y2 = box
                x_center = (x1 + x2) / 2
                y_center = (y1 + y2) / 2
                label = result.names[int(class_id)]  # Get the label from class id
                print(f"Detected object: Label {label}, Confidence {confidence:.2f}")
                print(f"Center coordinates: ({x_center:.2f}, {y_center:.2f})")

                # Draw the bounding box and center point on the frame
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.circle(frame, (int(x_center), int(y_center)), 5, (0, 0, 255), -1)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)

        # Display the resulting frame with detections
        cv2.imshow('YOLOv8 Detection', frame)

# When everything done, release the capture object and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
