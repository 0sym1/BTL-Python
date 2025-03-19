import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import pyqtSignal
import CheckPassScene
############################################
ui = ''
app = QApplication(sys.argv)
window = ''

password = '123'
otp = '123'

############################################


class CheckPassController(CheckPassScene.Ui_MainWindow):
    login_successful = pyqtSignal()  # Tạo signal để báo thành công

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.authentication_step = 1

        CheckPassController.listener(self)

    def listener(self):
        self.pushButton.clicked.connect(self.on_button_click)

    def on_button_click(self):
        input = self.lineEdit.text()
        if(self.authentication_step == 1):
            self.check_password(input)
        elif(self.authentication_step == 2):
            self.check_otp(input)
        
    def check_password(self, input):
        if(input == password):
            self.label.setText('OTP has been sent to your email')
            self.lineEdit.setText('')
            self.authentication_step = 2
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