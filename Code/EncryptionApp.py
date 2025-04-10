from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
                             QFileDialog, QComboBox, QLineEdit, QTextEdit)
import base64
import random
import string
from Encrypt import Encryptor
from Decrypt import Decryptor

class EncryptionApp(QWidget):
    def __init__(self, main_screen=None):
        super().__init__()
        self.main_screen = main_screen  # Lưu tham chiếu đến MyApp (màn hình chính)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Nút Back
        self.btn_back = QPushButton("Quay lại")
        self.btn_back.clicked.connect(self.go_back)
        layout.addWidget(self.btn_back)

        self.label = QLabel("Chọn thuật toán:")
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(["AES", "3DES", "Blowfish"])
        layout.addWidget(self.combo)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Nhập khóa (sẽ tự điều chỉnh nếu quá ngắn/dài)")
        layout.addWidget(self.key_input)

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Nhập văn bản để mã hóa/giải mã")
        layout.addWidget(self.text_input)

        self.btn_encrypt = QPushButton("Mã hóa Văn bản")
        self.btn_encrypt.clicked.connect(self.encrypt_text)
        layout.addWidget(self.btn_encrypt)

        self.btn_decrypt = QPushButton("Giải mã Văn bản")
        self.btn_decrypt.clicked.connect(self.decrypt_text)
        layout.addWidget(self.btn_decrypt)

        self.btn_encrypt_file = QPushButton("Mã hóa File")
        self.btn_encrypt_file.clicked.connect(self.encrypt_file)
        layout.addWidget(self.btn_encrypt_file)

        self.btn_decrypt_file = QPushButton("Giải mã File")
        self.btn_decrypt_file.clicked.connect(self.decrypt_file)
        layout.addWidget(self.btn_decrypt_file)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        layout.addWidget(self.result)

        self.setLayout(layout)
        self.setWindowTitle("Ứng dụng Mã hóa")
        self.resize(800, 600)

    def go_back(self):
        if self.main_screen:
            self.main_screen.show()  # Hiển thị lại màn hình chính (MyApp)
        self.hide()  # Ẩn màn hình hiện tại (EncryptionApp)

    def adjust_key_length(self, algo, key):
        key_bytes = key.encode('utf-8')
        required_lengths = {"AES": 32, "3DES": 24, "Blowfish": 16}
        required_length = required_lengths[algo]

        if len(key_bytes) < required_length:
            missing_length = required_length - len(key_bytes)
            random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=missing_length))
            adjusted_key = key + random_chars
            adjusted_key_bytes = adjusted_key.encode('utf-8')
            self.key_input.setText(adjusted_key)
            return adjusted_key_bytes
        elif len(key_bytes) > required_length:
            adjusted_key_bytes = key_bytes[:required_length]
            adjusted_key = adjusted_key_bytes.decode('utf-8', errors='ignore')
            self.key_input.setText(adjusted_key)
            return adjusted_key_bytes
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