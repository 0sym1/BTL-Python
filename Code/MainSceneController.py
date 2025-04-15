import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
import MainScene, CheckPassScene, PassManagerScene
from CheckPassController import CheckPassController
from PassManagerController import PassManagerController
from EncryptionApp import EncryptionApp
from del_file import MainWindowDelFile
from Style import Style

# Biến toàn cục
window = None


class MyApp(QMainWindow, MainScene.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        MyApp.listener(self)

        Style.apply_styles(self)

    def listener(self):
        self.Password_Manager_Button.clicked.connect(self.on_PassManager_button_click)
        self.Encrypt_Button.clicked.connect(self.on_Encrypt_button_click)
        self.Secure_File_Deletion_Button.clicked.connect(self.on_SecureFile_button_click)

    def on_PassManager_button_click(self):
        self.window2 = CheckPassController()
        self.window2.login_successful.connect(self.go_to_pass_manager_scene)
        self.window2.show()

    def on_Encrypt_button_click(self):
        self.window2 = EncryptionApp(main_screen=self)
        self.hide()
        self.window2.show()

    def on_SecureFile_button_click(self):
        self.window2 = MainWindowDelFile()
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
