from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
                             QFileDialog, QComboBox, QLineEdit, QTextEdit, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame)
import base64
import random
import string
from Encrypt import Encryptor
from Decrypt import Decryptor
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
class EncryptionApp(QWidget):
    def __init__(self, main_screen=None):
        super().__init__()
        self.main_screen = main_screen  # Lưu tham chiếu đến MyApp (màn hình chính)
        self.initUI()

    def initUI(self):
        # Bố cục chính
        main_layout = QVBoxLayout()

        # Tiêu đề và nút Back
        header_layout = QHBoxLayout()
        self.btn_back = QPushButton("Quay lại")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setIcon(QIcon("icons/back.png"))
        self.btn_back.setStyleSheet("""
            QPushButton {
                padding: 8px; 
                font-size: 14px; 
                background-color: #555; 
                color: white; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        header_layout.addWidget(self.btn_back)

        title_label = QLabel("Ứng dụng Mã hóa và Giải mã")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff; margin: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # type: ignore # Căn giữa tiêu đề
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Bố cục chính chia thành 2 phần: Nhập liệu (trái) và Nút chức năng (phải)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Bên trái: Khu vực nhập liệu
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)  # Khoảng cách giữa các thành phần

        # Chọn thuật toán
        algo_layout = QHBoxLayout()
        self.label = QLabel("Chọn thuật toán:")
        self.label.setStyleSheet("font-size: 16px; color: #ffffff; font-weight: bold;")
        algo_layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(["AES", "3DES", "Blowfish"])
        self.combo.setStyleSheet("padding: 5px; font-size: 16px; color: #ffffff; background-color: #333; border: 1px solid #555; border-radius: 5px;fontweight: bold;")
        algo_layout.addWidget(self.combo)
        left_layout.addLayout(algo_layout)

        # Nhập khóa
        key_layout = QHBoxLayout()
        key_label = QLabel("Nhập khóa:")
        key_label.setStyleSheet("font-size: 16px; color: #ffffff; font-weight: bold;")
        key_layout.addWidget(key_label)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Nhập khóa (sẽ tự điều chỉnh nếu quá ngắn/dài)")
        self.key_input.setStyleSheet("padding: 5px; font-size: 16px; border: 1px solid #555; border-radius: 5px;")
        key_layout.addWidget(self.key_input)
        left_layout.addLayout(key_layout)

        # Nhập văn bản
        text_label = QLabel("Nhập văn bản:")
        text_label.setStyleSheet("font-size: 16px; color: #ffffff; font-weight: bold;")
        left_layout.addWidget(text_label)

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Nhập văn bản để mã hóa/giải mã")
        self.text_input.setStyleSheet("padding: 5px; font-size: 16px; border: 1px solid #555; border-radius: 5px;")
        left_layout.addWidget(self.text_input)

        content_layout.addLayout(left_layout)

        # Bên phải: Các nút chức năng
        right_layout = QVBoxLayout()
        right_layout.setSpacing(20)  # Khoảng cách giữa các nút

        self.btn_encrypt = QPushButton("Mã hóa Văn bản")
        self.btn_encrypt.clicked.connect(self.encrypt_text)
        self.btn_encrypt.setIcon(QIcon("icons/encrypt.png"))  # Biểu tượng mã hóa
        self.btn_encrypt.setStyleSheet("padding: 20px; font-size: 20px; background-color: #4CAF50; color: white; border-radius: 5px;")
        right_layout.addWidget(self.btn_encrypt)

        self.btn_decrypt = QPushButton("Giải mã Văn bản")
        self.btn_decrypt.clicked.connect(self.decrypt_text)
        self.btn_decrypt.setIcon(QIcon("icons/decrypt.png"))  # Biểu tượng giải mã
        self.btn_decrypt.setStyleSheet("padding: 20px; font-size: 20px; background-color: #2196F3; color: white; border-radius: 5px;")
        right_layout.addWidget(self.btn_decrypt)

        self.btn_encrypt_file = QPushButton("Mã hóa File")
        self.btn_encrypt_file.clicked.connect(self.encrypt_file)
        self.btn_encrypt_file.setIcon(QIcon("icons/file_encrypt.png"))  # Biểu tượng mã hóa file
        self.btn_encrypt_file.setStyleSheet("padding: 20px; font-size: 20px; background-color: #4CAF50; color: white; border-radius: 5px;")
        right_layout.addWidget(self.btn_encrypt_file)

        self.btn_decrypt_file = QPushButton("Giải mã File")
        self.btn_decrypt_file.clicked.connect(self.decrypt_file)
        self.btn_decrypt_file.setIcon(QIcon("icons/file_decrypt.png"))  # Biểu tượng giải mã file
        self.btn_decrypt_file.setStyleSheet("padding: 20px; font-size: 20px; background-color: #2196F3; color: white; border-radius: 5px;")
        right_layout.addWidget(self.btn_decrypt_file)

        content_layout.addLayout(right_layout)

        main_layout.addLayout(content_layout)

        # Khu vực kết quả
        result_label = QLabel("Kết quả:")
        result_label.setStyleSheet("font-size: 16px; color: #ffffff; margin-top: 10px;font-weight: bold;")
        main_layout.addWidget(result_label)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setStyleSheet("padding: 5px; font-size: 16px; border: 1px solid #555; border-radius: 5px; background-color: #333; color: #fff;")
        main_layout.addWidget(self.result)

        self.setLayout(main_layout)
        self.setWindowTitle("Ứng dụng Mã hóa và Giải mã")
        self.resize(1600, 800)

        # Áp dụng stylesheet cho toàn bộ widget để thay đổi nền
        self.setStyleSheet("background-color: #1E1E1E;")

    def go_back(self):
        if self.main_screen:
            self.main_screen.show()  # Hiển thị lại màn hình chính (MyApp)
        self.hide()  # Ẩn màn hình hiện tại (EncryptionApp)


    def adjust_key_length(self, algo, key):
        key_bytes = key.encode('utf-8')  # Hỗ trợ ký tự tiếng Việt
        required_lengths = {"AES": 32, "3DES": 24, "Blowfish": 16}
        required_length = required_lengths[algo]
        if len(key_bytes) < required_length:
            key_bytes = key_bytes + b'\x00' * (required_length - len(key_bytes))
        elif len(key_bytes) > required_length:
            key_bytes = key_bytes[:required_length]
        return key_bytes

    def encrypt_text(self):
        text = self.text_input.toPlainText()
        algo = self.combo.currentText()
        key = self.key_input.text().strip()

        if key:
            adjusted_key = self.adjust_key_length(algo, key)
            encryptor = Encryptor(algo, adjusted_key)
        else:
            encryptor = Encryptor(algo)
            self.key_input.setText(base64.b64encode(encryptor.key).decode())

        encrypted_text = encryptor.encrypt_text(text)
        self.result.setText(f"Mã hóa thành công:\n{encrypted_text}")

    def decrypt_text(self):
        encrypted_text = self.text_input.toPlainText().strip()
        algo = self.combo.currentText()
        key = self.key_input.text().strip()
        print(f"Key: {key}")

        if not key:
            self.result.setText("Vui lòng nhập khóa giải mã.")
            return

        try:
            decryptor = Decryptor(algo, key)
            decrypted_text = decryptor.decrypt_text(encrypted_text)
            self.result.setText(f"Giải mã thành công:\n{decrypted_text}")
        except ValueError as e:
            self.result.setText(f"Lỗi: {str(e)}")
        except Exception as e:
            self.result.setText(f"Lỗi không xác định: {str(e)}")

    def encrypt_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file để mã hóa")
        if not file_path:
            return

        algo = self.combo.currentText()
        key = self.key_input.text().strip()

        if key:
            adjusted_key = self.adjust_key_length(algo, key)
            encryptor = Encryptor(algo, adjusted_key)
        else:
            encryptor = Encryptor(algo)
            self.key_input.setText(base64.b64encode(encryptor.key).decode())

        save_path, _ = QFileDialog.getSaveFileName(self, "Lưu file đã mã hóa", file_path + ".enc", "All Files (*)")
        if not save_path:
            self.result.setText("Hủy lưu file.")
            return

        result = encryptor.encrypt_file(file_path, save_path)
        self.result.setText(result)

    def decrypt_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file để giải mã")
        if not file_path:
            return

        if not file_path.endswith(".enc"):
            self.result.setText("File không hợp lệ! Vui lòng chọn file có đuôi .enc.")
            return

        algo = self.combo.currentText()
        key = self.key_input.text().strip()

        if not key:
            self.result.setText("Vui lòng nhập khóa giải mã.")
            return

        try:
            decryptor = Decryptor(algo, key)
            save_path, _ = QFileDialog.getSaveFileName(self, "Lưu file giải mã", file_path[:-4], "All Files (*)")
            if not save_path:
                self.result.setText("Hủy lưu file.")
                return

            result = decryptor.decrypt_file(file_path, save_path)
            self.result.setText(result)
        except ValueError as e:
            self.result.setText(f"Lỗi: {str(e)}")
        except Exception as e:
            self.result.setText(f"Lỗi không xác định: {str(e)}")