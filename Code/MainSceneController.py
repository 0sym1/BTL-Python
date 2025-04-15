import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
import MainScene, CheckPassScene, PassManagerScene
from CheckPassController import CheckPassController
from PassManagerController import PassManagerController
from EncryptionApp import EncryptionApp
from del_file import MainWindowDelFile

# Biến toàn cục
window = None


class MyApp(QMainWindow, MainScene.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.apply_styles()
        MyApp.listener(self)

    def listener(self):
        self.Password_Manager_Button.clicked.connect(self.on_PassManager_button_click)
        self.Encrypt_Button.clicked.connect(self.on_Encrypt_button_click)
        self.Secure_File_Deletion_Button.clicked.connect(self.on_SecureFile_button_click)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                font-family: 'Segoe UI', sans-serif;
                color: #f0f0f0;
                font-size: 16px;
            }

            QLabel {
                font-size: 28px;
                font-weight: 600;
                color: #f8f8f8;
            }

            QPushButton {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #4e54c8, stop: 1 #8f94fb
                );
                border: none;
                border-radius: 12px;
                padding: 12px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #5a60d1, stop: 1 #9ca1fd
                );
            }

            QPushButton:pressed {
                background-color: #3b3f87;
            }
        """)

    def on_PassManager_button_click(self):
        self.window2 = CheckPassController()
        self.window2.login_successful.connect(self.go_to_pass_manager_scene)
        self.window2.show()

    def on_Encrypt_button_click(self):
        self.window2 = EncryptionApp(main_screen=self)
        self.hide()
        self.window2.show()

    def on_SecureFile_button_click(self):
        self.window2 = MainWindowDelFile(main_screen=self)
        self.hide()
        self.window2.show()

    def go_to_pass_manager_scene(self):
        self.window2 = PassManagerController(self)
        self.hide()
        self.window2.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
