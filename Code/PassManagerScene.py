# Form implementation generated from reading ui file 'UI/PassManagerScene.ui'
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
        MainWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ChangePass_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.ChangePass_Button.setGeometry(QtCore.QRect(40, 40, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ChangePass_Button.setFont(font)
        self.ChangePass_Button.setObjectName("ChangePass_Button")
        self.ChangeMail_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.ChangeMail_Button.setGeometry(QtCore.QRect(230, 40, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ChangeMail_Button.setFont(font)
        self.ChangeMail_Button.setObjectName("ChangeMail_Button")
        self.AddAcount_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.AddAcount_Button.setGeometry(QtCore.QRect(430, 40, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.AddAcount_Button.setFont(font)
        self.AddAcount_Button.setObjectName("AddAcount_Button")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 111, 561, 251))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.Back_Button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Back_Button.setGeometry(QtCore.QRect(10, 10, 56, 17))
        self.Back_Button.setObjectName("Back_Button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.EditTrigger.AllEditTriggers)
        self.tableWidget.setColumnWidth(0, 160)  # Cột "Account"
        self.tableWidget.setColumnWidth(1, 150)  # Cột "Username"
        self.tableWidget.setColumnWidth(2, 138)  # Cột "Password"
        self.tableWidget.setColumnWidth(3, 110)  # Cột "Date"

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ChangePass_Button.setText(_translate("MainWindow", "Change password"))
        self.ChangeMail_Button.setText(_translate("MainWindow", "Change email"))
        self.AddAcount_Button.setText(_translate("MainWindow", "Add acocunt"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Account"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Username"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Password"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Date"))
        self.Back_Button.setText(_translate("MainWindow", "Back"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
