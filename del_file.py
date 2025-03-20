import sys
import hashlib
import os
import shutil
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QLineEdit, QComboBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Tiêu đề chính
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 30, 250, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # Group XÓA FILE
        self.del_group = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.del_group.setGeometry(QtCore.QRect(170, 100, 451, 300))  # Tăng chiều cao để thêm QComboBox
        font.setPointSize(13)
        self.del_group.setFont(font)
        self.del_group.setObjectName("del_group")

        self.choose_file = QtWidgets.QPushButton(parent=self.del_group)
        self.choose_file.setGeometry(QtCore.QRect(20, 30, 100, 30))
        self.choose_file.setObjectName("choose_file")
        self.choose_file.clicked.connect(self.select_file)

        self.file_label = QtWidgets.QLabel(parent=self.del_group)
        self.file_label.setGeometry(QtCore.QRect(130, 30, 280, 30))
        self.file_label.setObjectName("file_label")

        # Radio buttons cho tùy chọn xóa
        self.delete_perm_radio = QtWidgets.QRadioButton(parent=self.del_group)
        self.delete_perm_radio.setGeometry(QtCore.QRect(130, 70, 150, 20))
        self.delete_perm_radio.setText("Xóa không khôi phục")
        self.delete_perm_radio.setChecked(False)
        self.delete_perm_radio.toggled.connect(self.toggle_fields)

        self.delete_rec_radio = QtWidgets.QRadioButton(parent=self.del_group)
        self.delete_rec_radio.setGeometry(QtCore.QRect(300, 70, 150, 20))
        self.delete_rec_radio.setText("Xóa có khôi phục")
        self.delete_rec_radio.setChecked(False)
        self.delete_rec_radio.toggled.connect(self.toggle_fields)

        # QComboBox cho thuật toán xóa (ẩn mặc định)
        self.algorithm_label = QtWidgets.QLabel(parent=self.del_group)
        self.algorithm_label.setGeometry(QtCore.QRect(130, 110, 100, 20))
        self.algorithm_label.setText("Thuật toán:")
        self.algorithm_label.setVisible(False)

        self.algorithm_combo = QComboBox(parent=self.del_group)
        self.algorithm_combo.setGeometry(QtCore.QRect(230, 110, 200, 30))
        self.algorithm_combo.addItems(["Simple", "DoD 5220.22-M", "Gutmann"])
        self.algorithm_combo.setVisible(False)

        # Trường nhập mật khẩu (ẩn mặc định)
        self.password_label = QtWidgets.QLabel(parent=self.del_group)
        self.password_label.setGeometry(QtCore.QRect(130, 150, 100, 20))
        self.password_label.setText("Mật khẩu:")
        self.password_label.setVisible(False)

        self.password_input = QLineEdit(parent=self.del_group)
        self.password_input.setGeometry(QtCore.QRect(230, 150, 200, 30))
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setVisible(False)

        self.delete_button = QtWidgets.QPushButton(parent=self.del_group)
        self.delete_button.setGeometry(QtCore.QRect(150, 240, 80, 30))
        self.delete_button.setObjectName("delete_button")
        self.delete_button.clicked.connect(self.delete_file)

        self.cancel_button = QtWidgets.QPushButton(parent=self.del_group)
        self.cancel_button.setGeometry(QtCore.QRect(250, 240, 80, 30))
        self.cancel_button.setObjectName("cancel_button")
        self.cancel_button.clicked.connect(self.cancel_delete)

        self.result_label = QtWidgets.QLabel(parent=self.del_group)
        self.result_label.setGeometry(QtCore.QRect(130, 280, 300, 20))
        self.result_label.setObjectName("result_label")

        # Group KIỂM TRA FILE
        self.check_group = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.check_group.setGeometry(QtCore.QRect(170, 410, 451, 220))
        font.setPointSize(13)
        self.check_group.setFont(font)
        self.check_group.setObjectName("check_group")

        self.choose_file_2 = QtWidgets.QPushButton(parent=self.check_group)
        self.choose_file_2.setGeometry(QtCore.QRect(20, 30, 100, 30))
        self.choose_file_2.setObjectName("choose_file_2")
        self.choose_file_2.clicked.connect(self.select_file_2)

        self.file_label_2 = QtWidgets.QLabel(parent=self.check_group)
        self.file_label_2.setGeometry(QtCore.QRect(130, 30, 280, 30))
        self.file_label_2.setObjectName("file_label_2")

        self.choose_file_3 = QtWidgets.QPushButton(parent=self.check_group)
        self.choose_file_3.setGeometry(QtCore.QRect(20, 70, 100, 30))
        self.choose_file_3.setObjectName("choose_file_3")
        self.choose_file_3.clicked.connect(self.select_file_3)

        self.file_label_3 = QtWidgets.QLabel(parent=self.check_group)
        self.file_label_3.setGeometry(QtCore.QRect(130, 70, 280, 30))
        self.file_label_3.setObjectName("file_label_3")

        self.sha256_radio = QtWidgets.QRadioButton(parent=self.check_group)
        self.sha256_radio.setGeometry(QtCore.QRect(130, 110, 100, 20))
        self.sha256_radio.setText("SHA-256")
        self.sha256_radio.setChecked(False)

        self.md5_radio = QtWidgets.QRadioButton(parent=self.check_group)
        self.md5_radio.setGeometry(QtCore.QRect(240, 110, 100, 20))
        self.md5_radio.setText("MD5")
        self.md5_radio.setChecked(False)

        self.check_button = QtWidgets.QPushButton(parent=self.check_group)
        self.check_button.setGeometry(QtCore.QRect(150, 160, 100, 30))
        self.check_button.setObjectName("check_button")
        self.check_button.clicked.connect(self.check_hash)

        self.result_label_2 = QtWidgets.QLabel(parent=self.check_group)
        self.result_label_2.setGeometry(QtCore.QRect(20, 200, 400, 20))
        self.result_label_2.setObjectName("result_label_2")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.file_path = None
        self.file_path_2 = None  # File gốc
        self.file_path_3 = None  # File giải mã
        self.temp_dir = "temp_deleted_files"  # Thư mục tạm để lưu file có thể khôi phục
        self.passwords = {}  # Lưu trữ mật khẩu cho từng file

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Xóa File An Toàn"))
        self.label.setText(_translate("MainWindow", "Xóa file an toàn"))
        self.del_group.setTitle(_translate("MainWindow", "Xóa file"))
        self.choose_file.setText(_translate("MainWindow", "Chọn File"))
        self.file_label.setText(_translate("MainWindow", "Hãy chọn file của bạn..."))
        self.delete_button.setText(_translate("MainWindow", "Xóa"))
        self.cancel_button.setText(_translate("MainWindow", "Hủy"))
        self.check_group.setTitle(_translate("MainWindow", "Kiểm tra file"))
        self.choose_file_2.setText(_translate("MainWindow", "Chọn File Gốc"))
        self.file_label_2.setText(_translate("MainWindow", "Hãy chọn file gốc..."))
        self.choose_file_3.setText(_translate("MainWindow", "Chọn File Giải Mã"))
        self.file_label_3.setText(_translate("MainWindow", "Hãy chọn file giải mã..."))
        self.check_button.setText(_translate("MainWindow", "Kiểm tra"))

    def toggle_fields(self):
        # Hiển thị hoặc ẩn các trường dựa trên tùy chọn xóa
        if self.delete_perm_radio.isChecked():
            self.algorithm_label.setVisible(True)
            self.algorithm_combo.setVisible(True)
            self.password_label.setVisible(False)
            self.password_input.setVisible(False)
        elif self.delete_rec_radio.isChecked():
            self.algorithm_label.setVisible(False)
            self.algorithm_combo.setVisible(False)
            self.password_label.setVisible(True)
            self.password_input.setVisible(True)
        else:
            self.algorithm_label.setVisible(False)
            self.algorithm_combo.setVisible(False)
            self.password_label.setVisible(False)
            self.password_input.setVisible(False)

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName()
        if file_name:
            self.file_path = file_name
            self.file_label.setText(file_name)

    def select_file_2(self):
        file_name, _ = QFileDialog.getOpenFileName()
        if file_name:
            self.file_path_2 = file_name
            self.file_label_2.setText(file_name)

    def select_file_3(self):
        file_name, _ = QFileDialog.getOpenFileName()
        if file_name:
            self.file_path_3 = file_name
            self.file_label_3.setText(file_name)

    def secure_overwrite(self, file_path, method="simple"):
        file_size = os.path.getsize(file_path)

        if method == "simple":
            with open(file_path, "rb+") as f:
                f.write(b'\x00' * file_size)

        elif method == "dod":
            with open(file_path, "rb+") as f:
                f.write(b'\x00' * file_size)
                f.seek(0)
                f.write(b'\xFF' * file_size)
                f.seek(0)
                f.write(os.urandom(file_size))

        elif method == "gutmann":
            patterns = [
                           lambda: os.urandom(file_size),
                           lambda: os.urandom(file_size),
                           lambda: os.urandom(file_size),
                           lambda: os.urandom(file_size),
                           lambda: b'\x55' * file_size,
                           lambda: b'\xAA' * file_size,
                           lambda: b'\x92\x49\x24' * (file_size // 3 + 1),
                           lambda: b'\x49\x24\x92' * (file_size // 3 + 1),
                           lambda: b'\x24\x92\x49' * (file_size // 3 + 1),
                       ] + [lambda: os.urandom(file_size) for _ in range(31 - len(patterns))]

            with open(file_path, "rb+") as f:
                for pattern in patterns[:35]:
                    f.seek(0)
                    data = pattern()[:file_size]
                    f.write(data)

    def delete_file(self):
        if not self.file_path:
            QMessageBox.warning(None, "Lỗi", "Vui lòng chọn file để xóa!")
            return

        if not (self.delete_perm_radio.isChecked() or self.delete_rec_radio.isChecked()):
            QMessageBox.warning(None, "Lỗi", "Vui lòng chọn một tùy chọn xóa!")
            return

        try:
            if self.delete_perm_radio.isChecked():
                # Xóa không khôi phục với thuật toán được chọn
                algorithm = self.algorithm_combo.currentText().lower()
                if algorithm == "dod 5220.22-m":
                    algorithm = "dod"
                self.secure_overwrite(self.file_path, algorithm)
                os.remove(self.file_path)
                QMessageBox.information(None, "Thành công",
                                        f"File đã được xóa vĩnh viễn bằng {self.algorithm_combo.currentText()}!")
            elif self.delete_rec_radio.isChecked():
                # Xóa có khôi phục
                password = self.password_input.text()
                if not password:
                    QMessageBox.warning(None, "Lỗi", "Vui lòng nhập mật khẩu để xóa có khôi phục!")
                    return

                if not os.path.exists(self.temp_dir):
                    os.makedirs(self.temp_dir)

                file_name = os.path.basename(self.file_path)
                temp_path = os.path.join(self.temp_dir, file_name)
                shutil.move(self.file_path, temp_path)
                self.passwords[temp_path] = hashlib.sha256(password.encode()).hexdigest()
                QMessageBox.information(None, "Thành công", "File đã được xóa có khôi phục!\n"
                                                            "Lưu ý: File đang ở thư mục tạm và cần mật khẩu để khôi phục.")

            self.file_label.setText("Hãy chọn file của bạn...")
            self.file_path = None
            self.password_input.clear()
        except Exception as e:
            QMessageBox.warning(None, "Lỗi", f"Không thể xóa file: {str(e)}")

    def cancel_delete(self):
        QMessageBox.information(None, "Hủy bỏ", "Xóa file đã được hủy.")
        self.file_label.setText("Hãy chọn file của bạn...")
        self.file_path = None
        self.password_input.clear()

    def check_hash(self):
        if not self.file_path_2:
            QMessageBox.warning(None, "Lỗi", "Vui lòng chọn file gốc!")
            return
        if not self.file_path_3:
            QMessageBox.warning(None, "Lỗi", "Vui lòng chọn file giải mã!")
            return

        if not (self.sha256_radio.isChecked() or self.md5_radio.isChecked()):
            QMessageBox.warning(None, "Lỗi", "Vui lòng chọn một thuật toán hash!")
            return

        algorithm = "sha256" if self.sha256_radio.isChecked() else "md5"
        original_hash = self.hash_file(self.file_path_2, algorithm)
        decoded_hash = self.hash_file(self.file_path_3, algorithm)

        if original_hash == decoded_hash:
            self.result_label_2.setText(f"{algorithm.upper()} khớp: File gốc và file giải mã giống nhau!")
        else:
            self.result_label_2.setText(f"{algorithm.upper()} không khớp: File gốc và file giải mã khác nhau!\n"
                                        f"Original: {original_hash}\nDecoded: {decoded_hash}")

    def hash_file(self, file_path, algorithm="sha256"):
        if algorithm == "sha256":
            hash_func = hashlib.sha256()
        elif algorithm == "md5":
            hash_func = hashlib.md5()
        else:
            raise ValueError("Thuật toán không được hỗ trợ!")

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())