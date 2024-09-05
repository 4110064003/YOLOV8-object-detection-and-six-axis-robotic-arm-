#open the camera and start detect using yolov8n model
from ultralytics import YOLO
# import cv2

# model = YOLO("yolov8n.pt")
# result = model.predict(source="0", show=True)
model = YOLO("yolov8n.pt")
results = model.train(data="coco8.yaml", epochs=3)