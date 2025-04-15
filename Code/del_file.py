import hashlib
import os
import shutil
import sys

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QLineEdit, QStackedWidget


class MainMenuWidget(QtWidgets.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout()

        # layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        title = QtWidgets.QLabel("Xóa File An Toàn")
        title.setFont(QtGui.QFont("Arial", 20))
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.delete_btn = QtWidgets.QPushButton("Xóa File")
        self.delete_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(self.delete_btn)

        self.restore_btn = QtWidgets.QPushButton("Khôi phục File")
        self.restore_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        layout.addWidget(self.restore_btn)

        self.check_btn = QtWidgets.QPushButton("Kiểm tra File")
        self.check_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        layout.addWidget(self.check_btn)

        self.back_btn = QtWidgets.QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn)

        layout.addStretch()
        self.setLayout(layout)
    def go_back(self):
        self.stacked_widget.setCurrentIndex(0)


class DeleteWidget(QtWidgets.QWidget):
    
    def __init__(self, stacked_widget, passwords):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.passwords = passwords
        self.file_path = None
        self.temp_dir = "temp_deleted_files"
        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout()

        self.del_group = QtWidgets.QGroupBox("Xóa file")
        self.del_group.setFont(QtGui.QFont("Arial", 13))
        group_layout = QtWidgets.QVBoxLayout()

        self.choose_file = QtWidgets.QPushButton("🔍 Chọn File")
        self.choose_file.clicked.connect(self.select_file)
        group_layout.addWidget(self.choose_file)

        self.file_label = QtWidgets.QLabel("Hãy chọn file của bạn...")
        group_layout.addWidget(self.file_label)

        self.delete_perm_radio = QtWidgets.QRadioButton("Xóa không khôi phục")
        self.delete_perm_radio.toggled.connect(self.toggle_fields)
        group_layout.addWidget(self.delete_perm_radio)

        self.delete_rec_radio = QtWidgets.QRadioButton("Xóa có khôi phục")
        self.delete_rec_radio.toggled.connect(self.toggle_fields)
        group_layout.addWidget(self.delete_rec_radio)

        self.algorithm_label = QtWidgets.QLabel("Thuật toán:")
        self.algorithm_label.setVisible(False)
        group_layout.addWidget(self.algorithm_label)

        self.algorithm_combo = QtWidgets.QComboBox()
        self.algorithm_combo.addItems(["Simple", "DoD 5220.22-M", "Gutmann"])
        self.algorithm_combo.setVisible(False)
        group_layout.addWidget(self.algorithm_combo)

        self.password_label = QtWidgets.QLabel("Mật khẩu:")
        self.password_label.setVisible(False)
        group_layout.addWidget(self.password_label)

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setVisible(False)
        group_layout.addWidget(self.password_input)

        btn_layout = QtWidgets.QHBoxLayout()
        self.delete_button = QtWidgets.QPushButton("Xóa")
        self.delete_button.clicked.connect(self.delete_file)
        btn_layout.addWidget(self.delete_button)

        self.cancel_button = QtWidgets.QPushButton("Quay lại")
        self.cancel_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        btn_layout.addWidget(self.cancel_button)
        group_layout.addLayout(btn_layout)

        self.result_label = QtWidgets.QLabel("")
        group_layout.addWidget(self.result_label)

        self.del_group.setLayout(group_layout)
        layout.addWidget(self.del_group)
        layout.addStretch()
        self.setLayout(layout)

    def select_file(self):
        file_name, _ = QFileDialog.getOpenFileName()
        if file_name:
            self.file_path = file_name
            self.file_label.setText(file_name)

    def toggle_fields(self):
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
                lambda: b'\x24\x92\x49' * (file_size // 3 + 1),]
            patterns += [lambda: os.urandom(file_size) for _ in range(31 - len(patterns))]
            with open(file_path, "rb+") as f:
                for pattern in patterns[:35]:
                    f.seek(0)
                    data = pattern()[:file_size]
                    f.write(data)

    def delete_file(self):
        if not self.file_path:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn file để xóa!")
            return

        if not (self.delete_perm_radio.isChecked() or self.delete_rec_radio.isChecked()):
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một tùy chọn xóa!")
            return

        try:
            if self.delete_perm_radio.isChecked():
                algorithm = self.algorithm_combo.currentText().lower()
                if algorithm == "dod 5220.22-m":
                    algorithm = "dod"
                self.secure_overwrite(self.file_path, algorithm)
                os.remove(self.file_path)
                QMessageBox.information(self, "Thành công",
                                        f"File đã được xóa vĩnh viễn bằng {self.algorithm_combo.currentText()}!")
            elif self.delete_rec_radio.isChecked():
                password = self.password_input.text()
                if not password:
                    QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mật khẩu để xóa có khôi phục!")
                    return

                if not os.path.exists(self.temp_dir):
                    os.makedirs(self.temp_dir)

                file_name = os.path.basename(self.file_path)
                temp_path = os.path.join(self.temp_dir, file_name)
                # Chuẩn hóa đường dẫn để tránh lỗi do dấu phân cách
                temp_path = os.path.normpath(temp_path)
                shutil.move(self.file_path, temp_path)
                self.passwords[temp_path] = hashlib.sha256(password.encode()).hexdigest()
                # In thông tin debug
                print(f"Added to passwords: {temp_path} -> {self.passwords[temp_path]}")
                print(f"Current passwords dict: {self.passwords}")
                QMessageBox.information(self, "Thành công", "File đã được xóa có khôi phục!\n"
                                                            "Lưu ý: File đang ở thư mục tạm và cần mật khẩu để khôi phục.")

            self.file_label.setText("Hãy chọn file của bạn...")
            self.file_path = None
            self.password_input.clear()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể xóa file: {str(e)}")


class RestoreWidget(QtWidgets.QWidget):
    def __init__(self, stacked_widget, passwords):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.passwords = passwords
        self.restore_file_path = None
        self.temp_dir = "temp_deleted_files"
        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout()

        self.restore_group = QtWidgets.QGroupBox("Khôi phục file")
        self.restore_group.setFont(QtGui.QFont("Arial", 13))
        group_layout = QtWidgets.QVBoxLayout()

        self.choose_restore_file = QtWidgets.QPushButton("Chọn File")
        self.choose_restore_file.clicked.connect(self.select_restore_file)
        group_layout.addWidget(self.choose_restore_file)

        self.restore_file_label = QtWidgets.QLabel("Hãy chọn file để khôi phục...")
        group_layout.addWidget(self.restore_file_label)

        self.restore_password_label = QtWidgets.QLabel("Mật khẩu:")
        group_layout.addWidget(self.restore_password_label)

        self.restore_password_input = QLineEdit()
        self.restore_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        group_layout.addWidget(self.restore_password_input)

        btn_layout = QtWidgets.QHBoxLayout()
        self.restore_button = QtWidgets.QPushButton("Khôi phục")
        self.restore_button.clicked.connect(self.restore_file)
        btn_layout.addWidget(self.restore_button)

        self.back_button = QtWidgets.QPushButton("Quay lại")
        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        btn_layout.addWidget(self.back_button)
        group_layout.addLayout(btn_layout)

        self.restore_result_label = QtWidgets.QLabel("")
        group_layout.addWidget(self.restore_result_label)

        self.restore_group.setLayout(group_layout)
        layout.addWidget(self.restore_group)
        layout.addStretch()
        self.setLayout(layout)

    def select_restore_file(self):
        file_name, _ = QFileDialog.getOpenFileName(directory=self.temp_dir)
        if file_name:
            # Chuẩn hóa đường dẫn
            file_name = os.path.normpath(file_name)
            self.restore_file_path = file_name
            self.restore_file_label.setText(file_name)
            # Kiểm tra ngay khi chọn file
            if not os.path.exists(file_name):
                self.restore_result_label.setText("File không tồn tại trong thư mục tạm!")
            elif file_name not in self.passwords:
                self.restore_result_label.setText("File không có trong danh sách khôi phục!")
                # In thông tin debug
                print(f"Selected file: {file_name}")
                print(f"Current passwords dict: {self.passwords}")
            else:
                self.restore_result_label.setText("")

    def restore_file(self):
        if not self.restore_file_path:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn file để khôi phục!")
            return

        password = self.restore_password_input.text()
        if not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mật khẩu!")
            return

        # Kiểm tra file có tồn tại không
        if not os.path.exists(self.restore_file_path):
            QMessageBox.warning(self, "Lỗi", "File không còn tồn tại trong thư mục tạm!")
            return

        stored_hash = self.passwords.get(self.restore_file_path)
        if not stored_hash:
            QMessageBox.warning(self, "Lỗi", "File không có trong danh sách khôi phục!")
            # In thông tin debug
            print(f"Attempting to restore: {self.restore_file_path}")
            print(f"Current passwords dict: {self.passwords}")
            return

        input_hash = hashlib.sha256(password.encode()).hexdigest()
        if input_hash == stored_hash:
            restore_path, _ = QFileDialog.getSaveFileName(self, "Chọn vị trí khôi phục",
                                                          os.path.basename(self.restore_file_path))
            if restore_path:
                try:
                    shutil.move(self.restore_file_path, restore_path)
                    del self.passwords[self.restore_file_path]
                    self.restore_file_label.setText("Hãy chọn file để khôi phục...")
                    self.restore_password_input.clear()
                    self.restore_file_path = None
                    self.restore_result_label.setText("")
                    QMessageBox.information(self, "Thành công", "File đã được khôi phục thành công!")
                except Exception as e:
                    QMessageBox.warning(self, "Lỗi", f"Không thể khôi phục file: {str(e)}")
            else:
                QMessageBox.warning(self, "Hủy bỏ", "Khôi phục file đã bị hủy.")
        else:
            self.restore_result_label.setText("Mật khẩu không đúng!")


class CheckWidget(QtWidgets.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.file_path_2 = None
        self.file_path_3 = None
        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout()

        self.check_group = QtWidgets.QGroupBox("Kiểm tra file")
        self.check_group.setFont(QtGui.QFont("Arial", 13))
        group_layout = QtWidgets.QVBoxLayout()

        self.choose_file_2 = QtWidgets.QPushButton("Chọn File Gốc")
        self.choose_file_2.clicked.connect(self.select_file_2)
        group_layout.addWidget(self.choose_file_2)

        self.file_label_2 = QtWidgets.QLabel("Hãy chọn file gốc...")
        group_layout.addWidget(self.file_label_2)

        self.choose_file_3 = QtWidgets.QPushButton("Chọn File Giải Mã")
        self.choose_file_3.clicked.connect(self.select_file_3)
        group_layout.addWidget(self.choose_file_3)

        self.file_label_3 = QtWidgets.QLabel("Hãy chọn file giải mã...")
        group_layout.addWidget(self.file_label_3)

        self.sha256_radio = QtWidgets.QRadioButton("SHA-256")
        group_layout.addWidget(self.sha256_radio)

        self.md5_radio = QtWidgets.QRadioButton("MD5")
        group_layout.addWidget(self.md5_radio)

        btn_layout = QtWidgets.QHBoxLayout()
        self.check_button = QtWidgets.QPushButton("Kiểm tra")
        self.check_button.clicked.connect(self.check_hash)
        btn_layout.addWidget(self.check_button)

        self.back_button = QtWidgets.QPushButton("Quay lại")
        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        btn_layout.addWidget(self.back_button)
        group_layout.addLayout(btn_layout)

        self.result_label_2 = QtWidgets.QLabel("")
        group_layout.addWidget(self.result_label_2)

        self.check_group.setLayout(group_layout)
        layout.addWidget(self.check_group)
        layout.addStretch()
        self.setLayout(layout)

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

    def check_hash(self):
        if not self.file_path_2:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn file gốc!")
            return
        if not self.file_path_3:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn file giải mã!")
            return

        if not (self.sha256_radio.isChecked() or self.md5_radio.isChecked()):
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một thuật toán hash!")
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


class MainWindowDelFile(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xóa File An Toàn")
        self.resize(1600, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.passwords = {}

        self.main_menu = MainMenuWidget(self.stacked_widget)
        self.delete_widget = DeleteWidget(self.stacked_widget, self.passwords)
        self.restore_widget = RestoreWidget(self.stacked_widget, self.passwords)
        self.check_widget = CheckWidget(self.stacked_widget)

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.delete_widget)
        self.stacked_widget.addWidget(self.restore_widget)
        self.stacked_widget.addWidget(self.check_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    app.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(240, 240, 240, 255),
                    stop:1 rgba(200, 228, 238, 255)
                );
            }

            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #004d99; /* Màu xanh da trời đậm */
            }

            QPushButton {
                background-color: #66b3ff; /* Màu xanh nhạt */
                color: white;
                border-radius: 10px;
                font-size: 14px;
                padding: 8px 16px;
            }

            QPushButton:hover {
                background-color: #3399ff; /* Đổi màu khi hover */
                color: #ffffff;
            }

            QPushButton:pressed {
                background-color: #004d99; /* Đổi màu khi nhấn */
                border: 1px solid #003366;
            }

            QGroupBox {
                border: 2px solid #00509e;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                color: #00509e;
            }

            QRadioButton {
                font-size: 14px;
                color: #003366;
            }

            QLineEdit {
                border: 1px solid #00509e;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 2px solid #3399ff;
            }

            QMessageBox QLabel {
                font-size: 14px;
                color: #003366;
            }
        """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())