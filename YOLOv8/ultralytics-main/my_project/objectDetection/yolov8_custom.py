from ultralytics import YOLO
import numpy as np
import cv2

model = YOLO('numberv10.pt')#best.pt

result = model(source=1, show=True, conf=0.3, save=True)  # source=1 means external webcam,source=0 means pc webcam




