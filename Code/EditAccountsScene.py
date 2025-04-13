# Form implementation generated from reading ui file 'UI/EditAccountsScene.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 800)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.add_account_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.add_account_button.setGeometry(QtCore.QRect(900, 250, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.add_account_button.setFont(font)
        self.add_account_button.setObjectName("add_account_button")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(390, 170, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.account_lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.account_lineEdit.setGeometry(QtCore.QRect(510, 160, 191, 41))
        self.account_lineEdit.setObjectName("account_lineEdit")
        self.username_lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.username_lineEdit.setGeometry(QtCore.QRect(510, 219, 191, 41))
        self.username_lineEdit.setObjectName("username_lineEdit")
        self.password_lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.password_lineEdit.setGeometry(QtCore.QRect(510, 280, 191, 41))
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.rm_account_lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.rm_account_lineEdit.setGeometry(QtCore.QRect(510, 480, 191, 41))
        self.rm_account_lineEdit.setObjectName("rm_account_lineEdit")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(390, 230, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(390, 290, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.edit_account_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.edit_account_button.setGeometry(QtCore.QRect(900, 330, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.edit_account_button.setFont(font)
        self.edit_account_button.setObjectName("edit_account_button")
        self.remove_account_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.remove_account_button.setGeometry(QtCore.QRect(900, 480, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.remove_account_button.setFont(font)
        self.remove_account_button.setObjectName("remove_account_button")
        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(390, 490, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.back_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(30, 20, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.back_button.setFont(font)
        self.back_button.setObjectName("back_button")
        self.line = QtWidgets.QLabel(parent=self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 400, 1601, 20))
        self.line.setObjectName("line")
        self.notice1_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.notice1_label.setGeometry(QtCore.QRect(720, 20, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.notice1_label.setFont(font)
        self.notice1_label.setText("")
        self.notice1_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.notice1_label.setObjectName("notice1_label")
        self.notice2_label = QtWidgets.QLabel(parent=self.centralwidget)
        self.notice2_label.setGeometry(QtCore.QRect(340, 430, 541, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.notice2_label.setFont(font)
        self.notice2_label.setText("")
        self.notice2_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.notice2_label.setObjectName("notice2_label")
        self.gen_pass_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.gen_pass_button.setGeometry(QtCore.QRect(900, 130, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.gen_pass_button.setFont(font)
        self.gen_pass_button.setObjectName("gen_pass_button")
        self.lenght_pass_LineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lenght_pass_LineEdit.setGeometry(QtCore.QRect(1060, 130, 51, 51))
        self.lenght_pass_LineEdit.setObjectName("lenght_pass_LineEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1600, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.add_account_button.setText(_translate("MainWindow", "Add account"))
        self.label.setText(_translate("MainWindow", "Account"))
        self.label_2.setText(_translate("MainWindow", "Username"))
        self.label_3.setText(_translate("MainWindow", "Password"))
        self.edit_account_button.setText(_translate("MainWindow", "Edit account"))
        self.remove_account_button.setText(_translate("MainWindow", "Remove account"))
        self.label_4.setText(_translate("MainWindow", "Account"))
        self.back_button.setText(_translate("MainWindow", "back"))
        self.line.setText(_translate("MainWindow", "____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________"))
        self.gen_pass_button.setText(_translate("MainWindow", "Generate Password"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
