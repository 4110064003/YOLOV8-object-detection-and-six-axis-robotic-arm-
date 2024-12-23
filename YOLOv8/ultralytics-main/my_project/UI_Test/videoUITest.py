import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from ultralytics import YOLO
from videoUI import Ui_MainWindow  # 假設 UI.py 中的類名是 Ui_MainWindow

class VideoWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 打開攝像頭
        self.cap = cv2.VideoCapture(0)

        # 設置計時器來定期更新影像
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 每 30 毫秒更新一次

        # 加載 YOLOv8 模型
        self.model = YOLO('yolov8n.pt')  # 替換為你的模型路徑

        self.videoLabel.setScaledContents(True)# 啟用 QLabel 的縮放功能
        self.imageLabel.setScaledContents(True)

        # 儲存當前的影像
        self.current_frame = None

        # 連接按鈕事件
        self.startButton.clicked.connect(self.capture_image)

    def update_frame(self):
        # 讀取攝像頭影像
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame  # 儲存當前影像
            # 將影像從 BGR 轉換為 RGB 格式
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w

            # 將 OpenCV 影像轉換為 Qt 支援的 QImage
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)

            # 將 QPixmap 設置到 QLabel 上
            self.videoLabel.setPixmap(pixmap)

    # def keyPressEvent(self, event):
    #     # 檢查按下的按鍵是否為 's'
    #     if event.key() == ord('S') or event.key() == ord('s'):
    #         self.capture_image()

    # def capture_image(self):
    #     if self.current_frame is not None:
    #         # 儲存當前影像為檔案
    #         cv2.imwrite('captured_image.jpg', self.current_frame)
    #         print("影像已擷取並儲存為 'captured_image.jpg'")
            
    #         # 將影像轉換為 RGB 格式
    #         rgb_image = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
    #         h, w, ch = rgb_image.shape
    #         bytes_per_line = ch * w

    #         # 將 OpenCV 影像轉換為 Qt 支援的 QImage
    #         qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    #         pixmap = QPixmap.fromImage(qt_image)

    #         # 顯示擷取的影像到 UI 的 imageLabel
    #         self.imageLabel.setPixmap(pixmap)
    #         self.imageLabel.setScaledContents(True)  # 確保影像適應 QLabel 大小

    def capture_image(self):
        if self.current_frame is not None:
            # 儲存當前影像為檔案
            cv2.imwrite('captured_image.jpg', self.current_frame)
            # print("影像已擷取並儲存為 'captured_image.jpg'")
            # # 顯示影像到新視窗
            # cv2.imshow("Captured Image", self.current_frame)

            results = self.model(self.current_frame)# 使用 YOLOv8 進行目標辨識
            result_frame = results[0].plot()# 在辨識結果上繪製邊框和標籤

            # 將辨識結果影像轉換為 QImage 格式
            rgb_result_image = cv2.cvtColor(result_frame,cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_result_image.shape
            bytes_per_line = ch * w
            qt_result_image = QImage(rgb_result_image, w, h, bytes_per_line, QImage.Format_RGB888)
            result_pixmap = QPixmap.fromImage(qt_result_image)

            # 將 QPixmap 設置到 QLabel 上
            self.imageLabel.setPixmap(result_pixmap)
            self.imageLabel.setScaledContents(True)# 啟用 QLabel 的縮放功能


    def closeEvent(self, event):
        # 在視窗關閉時釋放攝像頭
        self.cap.release()
        cv2.destroyAllWindows()
        event.accept()

# 主程式
app = QApplication(sys.argv)
window = VideoWindow()
window.show()
sys.exit(app.exec_())
