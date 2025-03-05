import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from testui import Ui_MainWindow

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Thêm logic cho UI
        self.pushButton.clicked.connect(self.on_button_click)

    def on_button_click(self):
        self.label.setText(self.lineEdit.text())  # Ví dụ cập nhật label

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())