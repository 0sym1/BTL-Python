import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import ChangePasswordScene
from EditAccountsController import EditAccountsController

############################################
ui = ''
app = QApplication(sys.argv)
window = ''


############################################


class ChangePasswordController(ChangePasswordScene.Ui_MainWindow):
    def __init__(self, scene_main):
        super().__init__()
        self.setupUi(self)

        ChangePasswordController.listener(self)
        self.scene_main = scene_main

    def listener(self):
        self.Cancel_button.clicked.connect(self.on_back_button_click)
        self.OK_button.clicked.connect(self.on_OK_button_click)


    def on_OK_button_click(self):
        current_pass = ""
        lines = []
        with open("Data/data_account_manager", "r", encoding="utf-8") as files:
            lines = files.readlines()
            current_pass = lines[0].strip().split(":")[1].strip()

        if(self.current_pass_line.text() != current_pass):
            self.notice_label.setText("Current password is incorrect")
            return

        if(self.new_pass_line.text() == "" or self.cf_new_pass_line.text() == "" or self.current_pass_line.text() == ""):
            self.notice_label.setText("Please fill in all the fields")
            return
        
        if(self.new_pass_line.text() != self.cf_new_pass_line.text()):
            self.notice_label.setText("New password does not match")
            return
        
        if(self.new_pass_line.text() == current_pass):
            self.notice_label.setText("New password must be different from the current password")
            return
        
        with open("Data/data_account_manager", "w", encoding="utf-8") as files:
            files.write(f"Password: {self.new_pass_line.text()}\n")
            files.write(f"Email: {lines[1].strip().split(':')[1].strip()}\n")

        self.notice_label.setText("Change password successfully")
        self.current_pass_line.setText("")
        self.new_pass_line.setText("")
        self.cf_new_pass_line.setText("")
        

    def on_back_button_click(self):
        self.scene_main.show()
        self.hide()


# if __name__ == "__main__":
#     # app = QApplication(sys.argv)
#     window = PassManagerController()
#     window.show()
#     sys.exit(app.exec())
