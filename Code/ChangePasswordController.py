import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import ChangePasswordScene
from PyQt6.QtCore import pyqtSignal
from HashData import HashData
from Encrypt import Encryptor
from Decrypt import Decryptor
import base64
from AI.AIPass import AIPass
from Style import Style

############################################
ui = ''
app = QApplication(sys.argv)
window = ''

confirm_pass = 0
key = ''
list_password = []
############################################


class ChangePasswordController(ChangePasswordScene.Ui_MainWindow):
    update_data_account = pyqtSignal()
    def __init__(self, scene_main):
        super().__init__()
        self.setupUi(self)

        ChangePasswordController.listener(self)
        self.scene_main = scene_main

        Style.apply_styles(self)

    def listener(self):
        self.Cancel_button.clicked.connect(self.on_back_button_click)
        self.OK_button.clicked.connect(self.on_OK_button_click)


    def on_OK_button_click(self):
        current_pass = ""
        lines = []
        with open("Data/data_account_manager", "r", encoding="utf-8") as files:
            lines = files.readlines()
            current_pass = lines[0].strip().split(":")[1].strip()

        if(HashData.verify(self.current_pass_line.text(), current_pass) == False):
            self.notice_label.setText("Current password is incorrect")
            return

        if(self.new_pass_line.text() == "" or self.cf_new_pass_line.text() == "" or self.current_pass_line.text() == ""):
            self.notice_label.setText("Please fill in all the fields")
            return
        
        if(self.new_pass_line.text() != self.cf_new_pass_line.text()):
            self.notice_label.setText("New password does not match")
            return
        
        if(HashData.verify(self.new_pass_line.text(), current_pass)):
            self.notice_label.setText("New password must be different from the current password")
            return
        
        AIpass = AIPass()
        classifier = AIpass.classifier_pass(self.new_pass_line.text())
        global confirm_pass
        if(classifier == 0):
            if(confirm_pass == 0):
                self.notice_label.setText("Password is weak, are you confirm?")
                confirm_pass = 1
                return
        
        if(classifier == 1):
            if(confirm_pass == 0):
                self.notice_label.setText("Password is normal, are you confirm?")
                confirm_pass = 1
                return
        
        hash_pass = HashData.hasing(self.new_pass_line.text())
        
        with open("Data/data_account_manager", "w", encoding="utf-8") as files:
            files.write(f"Password: {hash_pass}\n")
            files.write(f"Email: {lines[1].strip().split(':')[1].strip()}\n")
        
        self.load_pass()
        global key
        key = self.new_pass_line.text()

        with open("Data/data_tmp", "w", encoding="utf-8") as files:
            files.write(f"Password_tmp: {self.new_pass_line.text()}\n")
        confirm_pass = 0

        self.encrypt_pass()

        self.notice_label.setText("Change password successfully")
        self.current_pass_line.setText("")
        self.new_pass_line.setText("")
        self.cf_new_pass_line.setText("")
        self.update_data_account.emit()
        

    def on_back_button_click(self):
        self.scene_main.show()
        self.hide()

    def load_pass(self):
        global list_password
        global key
        self.get_key()
        print("key ne ", key)
        with open("Data/data_accounts", "r", encoding="utf-8") as files:
            lines = files.readlines()

            encrypt_key = Encryptor.adjust_key_length("AES", key)
            key64 = base64.b64encode(encrypt_key).decode()
            decryptor = Decryptor("AES", key64)

            for row, line in enumerate(lines):
                arr_line = line.strip().split("|")
                if(len(arr_line) <= 1): continue
                arr_line[2] = decryptor.decrypt_text(arr_line[2].strip())
                list_password.append(arr_line[2])
                print(len(list_password), arr_line[2])

        id = 0

        with open("Data/data_accounts", "w", encoding="utf-8") as files:
            for line in lines:
                arr_line = line.strip().split("|")
                files.write(arr_line[0] + " | " + arr_line[1] + " | " + list_password[id] + " | " + arr_line[3] + "\n")
                id+= 1

    def encrypt_pass(self):
        global key
        print("key ne 2", key)

        with open("Data/data_accounts", "r", encoding="utf-8") as files:
            lines = files.readlines()
        files.close()

        encrypt_key = Encryptor.adjust_key_length("AES", key)
        encryptor = Encryptor("AES", encrypt_key)
        encrypt_pass = encryptor.encrypt_text(encrypt_key)

        with open("Data/data_accounts", "w", encoding="utf-8") as files:
            for line in lines:
                arr_line = line.strip().split("|")
                print(arr_line[2].strip(), "hehehhe")
                encrypt_pass = encryptor.encrypt_text(arr_line[2].strip())
                files.write(arr_line[0] + " | " + arr_line[1] + " | " + encrypt_pass + " | " + arr_line[3] + "\n")

    def get_key(self):
        global key

        with open("Data/data_tmp", "r", encoding="utf-8") as files:
            lines = files.readlines()
            key = lines[0].strip().split(":")[1].strip()



# if __name__ == "__main__":
#     # app = QApplication(sys.argv)
#     window = PassManagerController()
#     window.show()
#     sys.exit(app.exec())
