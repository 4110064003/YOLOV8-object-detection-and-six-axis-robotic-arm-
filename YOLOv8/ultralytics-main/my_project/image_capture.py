#相機畫面擷取並儲存
import cv2
import time
import os

def capture_image(image_number, folder_path):
    # 初始化摄像头
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # 讀取一幀畫面
    ret, frame = cap.read()

    if ret:
        # 保存畫面到文件，按編號命名
        filename = f"{image_number}.jpg"
        filepath = os.path.join(folder_path, filename)
        cv2.imwrite(filepath, frame)
        print(f"Image captured and saved as {filepath}")
    else:
        print("Error: Failed to capture image.")

    # 釋放鏡頭
    cap.release()

if __name__ == "__main__":
    folder_path = "captured_images"  # specify the folder path
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    image_number = 1  # 初始圖片標號為1
    while True:
        capture_image(image_number, folder_path)
        image_number += 1  # 更新圖片編號
        # 等待10秒
        time.sleep(5)