# Form implementation generated from reading ui file 'UI/MainScene.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Password_Manager_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Password_Manager_Button.setGeometry(QtCore.QRect(210, 70, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Password_Manager_Button.setFont(font)
        self.Password_Manager_Button.setObjectName("Password_Manager_Button")
        self.Encrypt_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Encrypt_Button.setGeometry(QtCore.QRect(210, 150, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Encrypt_Button.setFont(font)
        self.Encrypt_Button.setObjectName("Encrypt_Button")
        self.Secure_File_Deletion_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Secure_File_Deletion_Button.setGeometry(QtCore.QRect(210, 230, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Secure_File_Deletion_Button.setFont(font)
        self.Secure_File_Deletion_Button.setObjectName("Secure_File_Deletion_Button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 18))
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
        self.Password_Manager_Button.setText(_translate("MainWindow", "Password Manager"))
        self.Encrypt_Button.setText(_translate("MainWindow", "Encrypt and Decrypt "))
        self.Secure_File_Deletion_Button.setText(_translate("MainWindow", "Secure File Deletion"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
