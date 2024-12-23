# selection_ui.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI import Ui_MainWindow  # 假設 UI.py 中的類名是 Ui_MainWindow

class ObjectSelectionWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, object_list, target_list):
        super().__init__()
        self.setupUi(self)

        # 初始化選擇變數
        self.object_choice = None
        self.destination_choice = None

        # 加載物件和目標到列表
        for obj in object_list:
            self.ObjectListWidget.addItem(obj)
        for tgt in target_list:
            self.TargetListWidget.addItem(tgt)

        # 連接確認按鈕事件
        self.confirmButton.clicked.connect(self.confirm_selection)

    def confirm_selection(self):
        # 獲取選擇的物件和目標
        self.object_choice = self.ObjectListWidget.currentItem().text() if self.ObjectListWidget.currentItem() else None
        self.destination_choice = self.TargetListWidget.currentItem().text() if self.TargetListWidget.currentItem() else None
        
        # 關閉視窗
        self.close()

    def get_choices(self):
        # 返回使用者選擇
        return self.object_choice, self.destination_choice

def run_selection_ui(object_list, target_list):
    app = QApplication(sys.argv)
    window = ObjectSelectionWindow(object_list, target_list)
    window.show()
    app.exec_()
    return window.get_choices()
