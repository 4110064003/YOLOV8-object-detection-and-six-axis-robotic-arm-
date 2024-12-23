import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from UI import Ui_MainWindow  # 假設 UI.py 中的類名是 Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 初始化 UI

        # 動態載入物件和目標列表
        object_list = ["物件1", "物件2", "物件3"]
        target_list = ["目標1", "目標2", "目標3"]

        # 添加物件列表
        for obj in object_list:
            self.ObjectListWidget.addItem(obj)

        # 添加目標列表
        for tgt in target_list:
            self.TargetListWidget.addItem(tgt)

        # 連接確認按鈕事件
        self.confirmButton.clicked.connect(self.confirm_selection)
    
    def confirm_selection(self):
        # 獲取選擇的物件和目標
        selected_object = self.ObjectListWidget.currentItem().text() if self.ObjectListWidget.currentItem() else "無選擇"
        selected_target = self.TargetListWidget.currentItem().text() if self.TargetListWidget.currentItem() else "無選擇"
        
        # 顯示選擇結果
        QMessageBox.information(self, "選擇結果", f"您選擇了物件: {selected_object}\n目標: {selected_target}")
        # 將選擇結果打印在終端
        print(f"您選擇了物件: {selected_object}")
        print(f"您選擇了目標: {selected_target}")
        exit()


# 主程式
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
