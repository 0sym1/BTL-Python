import hashlib
import os
import shutil
import sys

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QLineEdit, QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout, QGroupBox, QWidget
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QIcon


class MainMenuWidget(QtWidgets.QWidget):
    def __init__(self, stacked_widget, main_screen = None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_screen = main_screen
        self.setupUi()

    def setupUi(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Căn giữa toàn bộ layout

        title = QtWidgets.QLabel("Xóa File An Toàn")
        title.setFont(QtGui.QFont("Arial", 24))  # Tăng kích thước font tiêu đề
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

    # Tạo khoảng cách giữa tiêu đề và các nút
        layout.addSpacing(20)

    # Căn chỉnh các nút với kích thước đồng đều
        button_style = """
            QPushButton {
                    min-width: 200px;
                min-height: 50px;
                font-size: 16px;
                font-weight: bold;
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #4e54c8, stop: 1 #8f94fb);
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #5a60d1, stop: 1 #9ca1fd);
            }
            QPushButton:pressed {
            background-color: #3b3f87;
            }
        """

        self.delete_btn = QtWidgets.QPushButton("Xóa File")
        self.delete_btn.setStyleSheet(button_style)
        self.delete_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(self.delete_btn, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)


        self.check_btn = QtWidgets.QPushButton("Kiểm tra File")
        self.check_btn.setStyleSheet(button_style)
        self.check_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        layout.addWidget(self.check_btn, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.back_btn = QtWidgets.QPushButton("Back")
        self.back_btn.setStyleSheet(button_style)
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    # Thêm khoảng cách cuối cùng để căn giữa
        layout.addStretch()
        self.setLayout(layout)

    def go_back(self):
        if self.main_screen:
            self.main_screen.show()
        self.hide()

class DeleteWidget(QtWidgets.QWidget):
    
    def __init__(self, stacked_widget, passwords):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.passwords = passwords
        self.file_path = None
        self.temp_dir = "temp_deleted_files"
        self.setupUi()

    def setupUi(self):
    # Layout ngoài cùng
        outer_layout = QtWidgets.QVBoxLayout(self)
        outer_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    # Widget trung tâm
        central_widget = QtWidgets.QWidget()
        central_layout = QtWidgets.QVBoxLayout(central_widget)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    # Groupbox xóa file
        self.del_group = QtWidgets.QGroupBox("Xóa file")
        self.del_group.setFont(QtGui.QFont("Arial", 16))  # Tăng font size
        self.del_group.setFixedSize(600, 300)  # Tăng kích thước groupbox
        self.del_group.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    # Layout chứa các thành phần trong groupbox
        group_outer_layout = QtWidgets.QVBoxLayout()
        group_outer_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        inner_widget = QtWidgets.QWidget()
        group_layout = QtWidgets.QVBoxLayout(inner_widget)
        group_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    # Nút chọn file
        self.choose_file = QtWidgets.QPushButton(" Chọn File")
        self.choose_file.setIcon(QtGui.QIcon("icons/folder.png"))
        self.choose_file.setFixedWidth(250)  # Tăng chiều rộng nút
        self.choose_file.setFont(QtGui.QFont("Arial", 14))  # Tăng kích thước font
        self.choose_file.clicked.connect(self.select_file)
        group_layout.addWidget(self.choose_file, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    # Nhãn file
        self.file_label = QtWidgets.QLabel("Hãy chọn file của bạn...")
        self.file_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.file_label.setFont(QtGui.QFont("Arial", 14))  # Tăng kích thước font
        group_layout.addWidget(self.file_label)

    # Radio xóa không khôi phục
        self.delete_perm_radio = QtWidgets.QRadioButton("Xóa không khôi phục")
        self.delete_perm_radio.setFont(QtGui.QFont("Arial", 14))  # Tăng font size
        self.delete_perm_radio.toggled.connect(self.toggle_fields)
        group_layout.addWidget(self.delete_perm_radio, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    # Radio xóa có khôi phục
        # self.delete_rec_radio = QtWidgets.QRadioButton("Xóa có khôi phục")
        # self.delete_rec_radio.setFont(QtGui.QFont("Arial", 14))  # Tăng font size
        # self.delete_rec_radio.toggled.connect(self.toggle_fields)
        # group_layout.addWidget(self.delete_rec_radio, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    # Thuật toán
        self.algorithm_label = QtWidgets.QLabel("Thuật toán:")
        self.algorithm_label.setVisible(False)
        self.algorithm_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.algorithm_label.setFont(QtGui.QFont("Arial", 14))  # Tăng font size
        group_layout.addWidget(self.algorithm_label)

        self.algorithm_combo = QtWidgets.QComboBox()
        self.algorithm_combo.addItems(["Simple", "DoD 5220.22-M", "Gutmann"])
        self.algorithm_combo.setVisible(False)
        self.algorithm_combo.setFont(QtGui.QFont("Arial", 14))  # Tăng font size
        self.algorithm_combo.setFixedWidth(280)  # Tăng chiều rộng combo box
        group_layout.addWidget(self.algorithm_combo, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    # Mật khẩu
        self.password_label = QtWidgets.QLabel("Mật khẩu:")
        self.password_label.setVisible(False)
        self.password_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password_label.setFont(QtGui.QFont("Arial", 14))  # Tăng font size
        group_layout.addWidget(self.password_label)

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_input.setVisible(False)
        self.password_input.setFont(QtGui.QFont("Arial", 14))  # Tăng font size
        self.password_input.setFixedWidth(280)  # Tăng chiều rộng input
        group_layout.addWidget(self.password_input, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    # Nút bấm
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.delete_button = QtWidgets.QPushButton(" Xóa")
        self.delete_button.setIcon(QtGui.QIcon("icons/delete.png"))
        self.delete_button.setFont(QtGui.QFont("Arial", 14))  # Tăng font size
        self.delete_button.setFixedSize(250, 50)  # Tăng kích thước nút
        self.delete_button.clicked.connect(self.delete_file)
        btn_layout.addWidget(self.delete_button)

        self.cancel_button = QtWidgets.QPushButton(" Quay lại")
        self.cancel_button.setIcon(QtGui.QIcon("icons/back.png"))
        self.cancel_button.setFont(QtGui.QFont("Arial", 14))  # Tăng font size
        self.cancel_button.setFixedSize(250, 50)  # Tăng kích thước nút
        self.cancel_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        btn_layout.addWidget(self.cancel_button)

        group_layout.addLayout(btn_layout)

    # Nhãn kết quả
        self.result_label = QtWidgets.QLabel("")
        self.result_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFont(QtGui.QFont("Arial", 14))  # Tăng font size
        group_layout.addWidget(self.result_label)

    # Gắn layout vào groupbox
        group_outer_layout.addStretch()
        group_outer_layout.addWidget(inner_widget)
        group_outer_layout.addStretch()

        self.del_group.setLayout(group_outer_layout)
        central_layout.addWidget(self.del_group)
        outer_layout.addWidget(central_widget)

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

        if not self.delete_perm_radio.isChecked():
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn tùy chọn xóa vĩnh viễn!")
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

            self.file_label.setText("Hãy chọn file của bạn...")
            self.file_path = None
            self.password_input.clear()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể xóa file: {str(e)}")




class CheckWidget(QtWidgets.QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.file_path_2 = None
        self.file_path_3 = None
        self.setupUi()

    def setupUi(self):
        outer_layout = QtWidgets.QVBoxLayout(self)
        outer_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        central_widget = QtWidgets.QWidget()
        central_layout = QtWidgets.QVBoxLayout(central_widget)
        central_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.check_group = QtWidgets.QGroupBox("Kiểm tra file")
        self.check_group.setFont(QtGui.QFont("Arial", 16))  # Font lớn hơn
        self.check_group.setFixedSize(700, 550)  # Tăng kích thước group box
        self.check_group.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    # Layout chính của groupbox
        group_outer_layout = QtWidgets.QVBoxLayout()
        group_outer_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    # Nội dung thực tế bên trong groupbox
        inner_widget = QtWidgets.QWidget()
        group_layout = QtWidgets.QVBoxLayout(inner_widget)
        group_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    # Nút chọn file gốc
        self.choose_file_2 = QtWidgets.QPushButton(" Chọn File Gốc")
        self.choose_file_2.setIcon(QtGui.QIcon("icons/folder.png"))
        self.choose_file_2.setFont(QtGui.QFont("Arial", 14))
        self.choose_file_2.setFixedSize(250, 50)
        self.choose_file_2.clicked.connect(self.select_file_2)
        group_layout.addWidget(self.choose_file_2, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    # Nhãn file gốc
        self.file_label_2 = QtWidgets.QLabel("Hãy chọn file gốc...")
        self.file_label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.file_label_2.setFont(QtGui.QFont("Arial", 14))
        group_layout.addWidget(self.file_label_2)

    # Nút chọn file giải mã
        self.choose_file_3 = QtWidgets.QPushButton(" Chọn File Giải Mã")
        self.choose_file_3.setIcon(QtGui.QIcon("icons/folder.png"))
        self.choose_file_3.setFont(QtGui.QFont("Arial", 14))
        self.choose_file_3.setFixedSize(250, 50)
        self.choose_file_3.clicked.connect(self.select_file_3)
        group_layout.addWidget(self.choose_file_3, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

    # Nhãn file giải mã
        self.file_label_3 = QtWidgets.QLabel("Hãy chọn file giải mã...")
        self.file_label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.file_label_3.setFont(QtGui.QFont("Arial", 14))
        group_layout.addWidget(self.file_label_3)

    # Radio buttons
        self.sha256_radio = QtWidgets.QRadioButton("SHA-256")
        self.md5_radio = QtWidgets.QRadioButton("MD5")
        self.sha256_radio.setFont(QtGui.QFont("Arial", 14))
        self.md5_radio.setFont(QtGui.QFont("Arial", 14))

        hash_radio_layout = QtWidgets.QHBoxLayout()
        hash_radio_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        hash_radio_layout.addWidget(self.sha256_radio)
        hash_radio_layout.addWidget(self.md5_radio)
        group_layout.addLayout(hash_radio_layout)

    # Nút kiểm tra và quay lại
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.check_button = QtWidgets.QPushButton(" Kiểm tra")
        self.check_button.setIcon(QtGui.QIcon("icons/check.png"))
        self.check_button.setFont(QtGui.QFont("Arial", 14))
        self.check_button.setFixedSize(250, 50)
        self.check_button.clicked.connect(self.check_hash)
        btn_layout.addWidget(self.check_button)

        self.back_button = QtWidgets.QPushButton(" Quay lại")
        self.back_button.setIcon(QtGui.QIcon("icons/back.png"))
        self.back_button.setFont(QtGui.QFont("Arial", 14))
        self.back_button.setFixedSize(250, 50)
        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        btn_layout.addWidget(self.back_button)

        group_layout.addLayout(btn_layout)

    # Nhãn kết quả
        self.result_label_2 = QtWidgets.QLabel("")
        self.result_label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.result_label_2.setFont(QtGui.QFont("Arial", 14))
        group_layout.addWidget(self.result_label_2)

        group_outer_layout.addStretch()
        group_outer_layout.addWidget(inner_widget, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        group_outer_layout.addStretch()

        self.check_group.setLayout(group_outer_layout)
        central_layout.addWidget(self.check_group)
        outer_layout.addWidget(central_widget)    

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
    def __init__(self, main_screen=None):
        super().__init__()
        self.setWindowTitle("Xóa File An Toàn")
        self.resize(1600, 800)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.passwords = {}
        self.main_screen = main_screen

        self.main_menu = MainMenuWidget(self.stacked_widget, self.main_screen)
        self.delete_widget = DeleteWidget(self.stacked_widget, self.passwords)

        self.check_widget = CheckWidget(self.stacked_widget)

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.delete_widget)

        self.stacked_widget.addWidget(self.check_widget)

        self.setStyleSheet("""
        QMainWindow {
            background-color: #1e1e2f; /* Màu nền chính */
        }
    
        QLabel {
            color: white; /* Chữ trắng */
            font-size: 16px; /* Kích thước chữ */
            font-weight: bold; /* Chữ đậm */
        }
    
        QPushButton {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5F4FFF, stop:1 #8871FF); /* Màu xanh tím */
            color: white; /* Chữ trắng */
            border-radius: 10px;
            font-size: 14px;
            padding: 8px 16px;
        }
    
        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5F4FFF, stop:1 #8871FF); /* Đổi màu xanh tím nhạt hơn khi hover */
            color: white;
        }
    
        QPushButton:pressed {
            background-color: #39416b; /* Đổi màu xanh tím đậm hơn khi nhấn */
            border: 1px solid #272b40;
        }
    
        QGroupBox {
            border: 2px solid #39416b; /* Đường viền xanh tím đậm */
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
            color: #6272a4; /* Màu xanh tím */
        }
    
        QRadioButton {
            font-size: 14px;
            color: #6272a4; /* Màu xanh tím */
        }
    
        QLineEdit {
            border: 1px solid #39416b; /* Viền xanh tím đậm */
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            color: white; /* Chữ trắng */
            background-color: #2d2f3f; /* Nền xanh tím tối */
        }
    
        QLineEdit:focus {
            border: 2px solid #7080c4; /* Viền xanh tím nhạt khi focus */
        }
    
        QMessageBox QLabel {
            font-size: 14px;
            color: #6272a4; /* Màu xanh tím */
        }
    """)