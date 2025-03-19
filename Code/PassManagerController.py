import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import PassManagerScene
from EditAccountsController import EditAccountsController

############################################
ui = ''
app = QApplication(sys.argv)
window = ''


############################################


class PassManagerController(PassManagerScene.Ui_MainWindow):
    def __init__(self, scene_main):
        super().__init__()
        self.setupUi(self)

        self.load_data_account()
        PassManagerController.listener(self)
        self.scene_main = scene_main

    def listener(self):
        self.Back_Button.clicked.connect(self.on_back_button_click)
        self.AddAcount_Button.clicked.connect(self.on_edit_accounts_button_click)


    def on_back_button_click(self):
        self.scene_main.show()
        self.hide()

    def on_edit_accounts_button_click(self):
        self.window2 = EditAccountsController(self)
        self.window2.show()
        self.hide()

        self.window2.update_data_account.connect(self.load_data_account)

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

            self.tableWidget.setRowCount(len(lines))  # Đặt số hàng theo dữ liệu
            self.tableWidget.setColumnCount(4)  # Giả sử file có 3 cột, chỉnh lại nếu cần

            for row, line in enumerate(lines):
                arr_line = line.strip().split("|")
                if(len(arr_line) == 0): continue
                for col, value in enumerate(arr_line):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(value.strip()))


# if __name__ == "__main__":
#     # app = QApplication(sys.argv)
#     window = PassManagerController()
#     window.show()
#     sys.exit(app.exec())
