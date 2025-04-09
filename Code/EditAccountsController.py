import sys
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6.QtCore import pyqtSignal
import EditAccountsScene
from Encrypt import Encryptor
from AI.AIPass import AIPass

############################################
ui = ''
app = QApplication(sys.argv)
window = ''

key = ''
confirm_pass = 0

############################################


class EditAccountsController(EditAccountsScene.Ui_MainWindow):
    update_data_account = pyqtSignal()

    def __init__(self, scene_main):
        super().__init__()
        self.setupUi(self)

        EditAccountsController.listener(self)
        self.scene_back = scene_main

        self.get_key()

    def listener(self):
        self.back_button.clicked.connect(self.on_back_button_click)
        self.add_account_button.clicked.connect(self.on_add_account_button_click)
        self.edit_account_button.clicked.connect(self.on_edit_account_button_click)
        

    def on_back_button_click(self):
        self.scene_back.show()
        self.hide()

    def on_add_account_button_click(self):
        if(self.check_fill_input() == False):
            self.notice1_label.setText("Please fill all input")
            return
        
        if(self.check_account_exist() == True):
            self.notice1_label.setText("Account already exist")
            return
        
        AIpass = AIPass()
        classifier = AIpass.classifier_pass(self.password_lineEdit.text())
        global confirm_pass
        if(classifier == 0):
            if(confirm_pass == 0):
                self.notice1_label.setText("Password is weak, are you confirm?")
                confirm_pass = 1
                return
        
        if(classifier == 1):
            if(confirm_pass == 0):
                self.notice1_label.setText("Password is normal, are you confirm?")
                confirm_pass = 1
                return
        
        global key
        # ecrypt = Encryptor("AES", key)
        encrypt_key = Encryptor.adjust_key_length("AES", key)
        encryptor = Encryptor("AES", encrypt_key)
        encrypt_pass = encryptor.encrypt_text(self.password_lineEdit.text())
        
        with open("Data/data_accounts", "a", encoding="utf-8") as files:
            files.write(self.account_lineEdit.text() + " | " + self.username_lineEdit.text() + " | " + encrypt_pass + " | " + datetime.today().strftime("%d/%m/%Y") + "\n")
        files.close()
        self.account_lineEdit.setText("")
        self.username_lineEdit.setText("")
        self.password_lineEdit.setText("")

        self.notice1_label.setText("Add account successfully")
        self.update_data_account.emit()
        confirm_pass = 0

    def on_edit_account_button_click(self):
        if(self.check_fill_input() == False):
            self.notice1_label.setText("Please fill all input")
            return
        
        if(self.check_account_exist() == False):
            self.notice1_label.setText("Account does not exist")
            return
        
        AIpass = AIPass()
        classifier = AIpass.classifier_pass(self.password_lineEdit.text())
        global confirm_pass
        if(classifier == 0):
            if(confirm_pass == 0):
                self.notice1_label.setText("Password is weak, are you confirm?")
                confirm_pass = 1
                return
        
        if(classifier == 1):
            if(confirm_pass == 0):
                self.notice1_label.setText("Password is normal, are you confirm?")
                confirm_pass = 1
                return
        
        line = []
        
        with open("Data/data_accounts", "r", encoding="utf-8") as files:
            lines = files.readlines()
        files.close()

        global key
        encrypt_key = Encryptor.adjust_key_length("AES", key)
        encryptor = Encryptor("AES", encrypt_key)
        encrypt_pass = encryptor.encrypt_text(self.password_lineEdit.text())

        with open("Data/data_accounts", "w", encoding="utf-8") as files:
            for line in lines:
                arr_line = line.strip().split("|")
                if(arr_line[0].strip() == self.account_lineEdit.text()):
                    files.write(self.account_lineEdit.text() + " | " + self.username_lineEdit.text() + " | " + encrypt_pass + " | " + datetime.today().strftime("%d/%m/%Y") + "\n")
                else:
                    files.write(line)

        self.account_lineEdit.setText("")
        self.username_lineEdit.setText("")
        self.password_lineEdit.setText("")
        confirm_pass = 0

        self.notice1_label.setText("Edit account successfully")
        self.update_data_account.emit()


        
    def check_fill_input(self):
        if(self.account_lineEdit.text() == '' or self.username_lineEdit.text() == '' or self.password_lineEdit.text() == ''):
            return False
        return True
    
    def check_account_exist(self):
        with open("Data/data_accounts", "r", encoding="utf-8") as files:
            lines = files.readlines()
            for line in lines:
                arr_line = line.strip().split("|")
                if(arr_line[0].strip() == self.account_lineEdit.text()):
                    return True
        return False
    
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
