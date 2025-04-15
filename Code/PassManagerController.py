import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import PassManagerScene
from EditAccountsController import EditAccountsController
from ChangePasswordController import ChangePasswordController
from ChangeEmailController import ChangeEmailController
from Decrypt import Decryptor
from Encrypt import Encryptor
import base64
from Style import Style

############################################
ui = ''
app = QApplication(sys.argv)
window = ''
key = ''
list_password = []

############################################


class PassManagerController(PassManagerScene.Ui_MainWindow):
    def __init__(self, scene_main):
        super().__init__()
        self.setupUi(self)

        self.load_data_account()
        PassManagerController.listener(self)
        self.scene_main = scene_main

        self.get_key()
        Style.apply_styles(self)

    def listener(self):
        self.Back_Button.clicked.connect(self.on_back_button_click)
        self.AddAcount_Button.clicked.connect(self.on_edit_accounts_button_click)
        self.ChangePass_Button.clicked.connect(self.on_change_password_button_click)
        self.ChangeMail_Button.clicked.connect(self.on_change_email_button_click)


    def on_back_button_click(self):
        self.scene_main.show()
        self.hide()

    def on_edit_accounts_button_click(self):
        self.window2 = EditAccountsController(self)
        self.window2.show()
        self.hide()

        self.window2.update_data_account.connect(self.load_data_account)

    def on_change_password_button_click(self):
        self.window2 = ChangePasswordController(self)
        self.window2.show()
        self.hide()

        self.window2.update_data_account.connect(self.load_data_account)

    def on_change_email_button_click(self):
        self.window2 = ChangeEmailController(self)
        self.window2.show()
        self.hide()

    # def on_change_email_button_click(self):
    #     self.window2 = ChangeEmailController(self)

    # def load_data_account(self):
    #     count_line = 0

    #     self.tableWidget.setRowCount(len(lines))  # Đặt số hàng theo dữ liệu
    #     self.tableWidget.setColumnCount(3)

    #     with open("Data/data_accounts", "r", encoding="utf-8") as files:
    #         for line in files:
    #             count_line += 1
    #             arr_line = line.strip().split("|")
    #             for i in range(len(arr_line)):
    #                 self.tableWidget.setItem(count_line, i, QTableWidgetItem(arr_line[i].strip()))
    #                 print(arr_line[i], end=" ")
    #             print()
        
    #     files.close()
    #     self.tableWidget.setItem(1, 1, QTableWidgetItem("hello"))
        
    def load_data_account(self):
        with open("Data/data_accounts", "r", encoding="utf-8") as files:
            lines = files.readlines()

            global key
            self.get_key()

            # encrypt = Encryptor("AES", key)

            encrypt_key = Encryptor.adjust_key_length("AES", key)
            key64 = base64.b64encode(encrypt_key).decode()
            decryptor = Decryptor("AES", key64)

            self.tableWidget.setRowCount(len(lines))  # Đặt số hàng theo dữ liệu
            self.tableWidget.setColumnCount(4)  # Giả sử file có 3 cột, chỉnh lại nếu cần

            for row, line in enumerate(lines):
                arr_line = line.strip().split("|")
                if(len(arr_line) <= 1): continue
                print(arr_line)
                arr_line[2] = decryptor.decrypt_text(arr_line[2].strip())
                for col, value in enumerate(arr_line):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(value.strip()))


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
