import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import ChangeEmailScene
from EditAccountsController import EditAccountsController
from Style import Style

############################################
ui = ''
app = QApplication(sys.argv)
window = ''


############################################


class ChangeEmailController(ChangeEmailScene.Ui_MainWindow):
    def __init__(self, scene_main):
        super().__init__()
        self.setupUi(self)

        ChangeEmailController.listener(self)
        self.scene_main = scene_main
        Style.apply_styles(self)

    def listener(self):
        self.cancel_button.clicked.connect(self.on_back_button_click)
        self.OK_button.clicked.connect(self.on_OK_button_click)


    def on_OK_button_click(self):
        current_email = ""
        lines = []
        with open("Data/data_account_manager", "r", encoding="utf-8") as files:
            lines = files.readlines()
            current_email = lines[1].strip().split(":")[1].strip()

        if(self.current_mai_line.text() != current_email and current_email != ""):
            self.notice_label.setText("Current email is incorrect")
            return
        
        if(current_email != ""):
            if(self.new_mail_line.text() == "" or self.cf_new_mail_line.text() == "" or self.current_mai_line.text() == ""):
                self.notice_label.setText("Please fill in all the fields")
                return
        
        if(self.new_mail_line.text() != self.cf_new_mail_line.text()):
            self.notice_label.setText("New email does not match")
            return
        
        if(self.new_mail_line.text() == current_email):
            self.notice_label.setText("New email must be different from the current email")
            return
        
        with open("Data/data_account_manager", "w", encoding="utf-8") as files:
            files.write(f"Password: {lines[0].strip().split(':')[1].strip()}\n")
            files.write(f"Email: {self.new_mail_line.text()}\n")

        self.notice_label.setText("Change email successfully")
        self.current_mai_line.setText("")
        self.new_mail_line.setText("")
        self.cf_new_mail_line.setText("")

    def on_back_button_click(self):
        self.scene_main.show()
        self.hide()


# if __name__ == "__main__":
#     # app = QApplication(sys.argv)
#     window = PassManagerController()
#     window.show()
#     sys.exit(app.exec())
