import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
import MainScene, CheckPassScene, PassManagerScene
from CheckPassController import CheckPassController
from PassManagerController import PassManagerController
from EncryptionApp import EncryptionApp
############################################
ui = ''
app = QApplication(sys.argv)
window = ''

############################################


class MyApp(QMainWindow, MainScene.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        MyApp.listener(self)

    def listener(self):
        self.Password_Manager_Button.clicked.connect(self.on_PassManager_button_click)
        self.Encrypt_Button.clicked.connect(self.on_Encrypt_button_click)
        self.Secure_File_Deletion_Button.clicked.connect(self.on_SecureFile_button_click)

    def on_PassManager_button_click(self):
        # ui = CheckPassScene.Ui_MainWindow()
        # ui.setupUi(window)
        # window.show()

        # self.window2 = CheckPassScene.Ui_MainWindow()
        self.window2 = CheckPassController()
        self.window2.login_successful.connect(self.go_to_pass_manager_scene)
        self.window2.show()

    def go_to_pass_manager_scene(self):
        # ui =  PassManagerScene.Ui_MainWindow()
        # ui.setupUi(window)

        # window = PassManagerController(self)
        # window.show()

        self.window2 = PassManagerController(self)
        window.hide()
        self.window2.show()
        


    def on_Encrypt_button_click(self):
        self.window2 = EncryptionApp()
        window.hide()
        self.window2.show()

    def on_SecureFile_button_click(self):
        self.label.setText(self.lineEdit.text())



if __name__ == "__main__":
    # app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())


# self.tableWidget.setColumnWidth(0, 168)  # Cột "Account"
#         self.tableWidget.setColumnWidth(1, 160)  # Cột "Username"
#         self.tableWidget.setColumnWidth(2, 130)  # Cột "Password"
#         self.tableWidget.setColumnWidth(3, 120)  # Cột "Date"
