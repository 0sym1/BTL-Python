import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import pyqtSignal
import CheckPassScene
import TwoFactorAuth
from HashData import HashData
from Encrypt import Encryptor
from Style import Style


############################################
ui = ''
app = QApplication(sys.argv)
window = ''


############################################

password = ''
otp = ''
email = ''

with open("Data/data_account_manager", "r", encoding="utf-8") as files:
    lines = files.readlines()
    print(lines)
    password = lines[0].strip().split(":")[1].strip()
    email = lines[1].strip().split(":")[1].strip()



############################################


class CheckPassController(CheckPassScene.Ui_MainWindow):
    login_successful = pyqtSignal()  # Tạo signal để báo thành công

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.authentication_step = 1

        CheckPassController.listener(self)
        # Style.apply_styles_v2(self)

    def listener(self):
        self.pushButton.clicked.connect(self.on_button_click)

    def on_button_click(self):
        input = self.lineEdit.text()
        if(self.authentication_step == 1):
            self.check_password(input)
        elif(self.authentication_step == 2):
            self.check_otp(input)
        
    def check_password(self, input):
        #save pass to tmp file data
        with open("Data/data_tmp", "w", encoding="utf-8") as files:
            files.write(f"Password_tmp: {input}\n")

        hash_pass = HashData.hasing(input)

        global password
        global email

        #read pass from data
        with open("Data/data_account_manager", "r", encoding="utf-8") as files:
            lines = files.readlines()
            print(lines)
            password = lines[0].strip().split(":")[1].strip()
            email = lines[1].strip().split(":")[1].strip()

        if(HashData.verify(input, password)):
            self.label.setText('OTP has been sent to your email')
            self.lineEdit.setText('')
            self.authentication_step = 2

            global otp
            otp = TwoFactorAuth.generate_otp()
            # TwoFactorAuth.send_otp(email, otp)
            otp = "123"
            

        else:
            self.label.setText('Incorrect Password')

    def check_otp(self, input):
        if(input == otp):
            self.close()
            self.login_successful.emit()
        else:
            self.label.setText('Incorrect OTP')


if __name__ == "__main__":
    # app = QApplication(sys.argv)
    window = CheckPassController()
    window.show()
    sys.exit(app.exec())