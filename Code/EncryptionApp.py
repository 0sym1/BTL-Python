from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
                             QFileDialog, QComboBox, QLineEdit, QTextEdit)
import base64
from Encrypt import Encryptor
from Decrypt import Decryptor

class EncryptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Chọn thuật toán:")
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(["AES", "3DES", "Blowfish"])
        layout.addWidget(self.combo)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Nhập khóa (sẽ tự điều chỉnh độ dài)")
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

    def adjust_key_length(self, algo, key):
        """Điều chỉnh độ dài khóa theo thuật toán"""
        key_bytes = key.encode()  # Chuyển chuỗi thành byte
        required_lengths = {"AES": 32, "3DES": 24, "Blowfish": 16}  # Độ dài yêu cầu (byte)
        required_length = required_lengths[algo]

        if len(key_bytes) < required_length:
            # Nếu ngắn hơn, thêm byte 0 vào cuối (padding)
            key_bytes = key_bytes + b'\x00' * (required_length - len(key_bytes))
        elif len(key_bytes) > required_length:
            # Nếu dài hơn, cắt bớt từ đầu
            key_bytes = key_bytes[:required_length]

        return key_bytes

    def encrypt_text(self):
        """Gọi class Encryptor để mã hóa văn bản"""
        text = self.text_input.toPlainText()
        algo = self.combo.currentText()
        key = self.key_input.text().strip()

        if key:
            # Điều chỉnh độ dài khóa nếu người dùng nhập
            adjusted_key = self.adjust_key_length(algo, key)
            encryptor = Encryptor(algo, adjusted_key)
        else:
            # Nếu không nhập khóa, tự sinh và hiển thị
            encryptor = Encryptor(algo)
            self.key_input.setText(base64.b64encode(encryptor.key).decode())

        encrypted_text = encryptor.encrypt_text(text)
        self.result.setText(f"Mã hóa thành công:\n{encrypted_text}")

    def decrypt_text(self):
        """Gọi class Decryptor để giải mã văn bản"""
        encrypted_text = self.text_input.toPlainText().strip()
        algo = self.combo.currentText()
        key = self.key_input.text().strip()

        if not key:
            self.result.setText("Vui lòng nhập khóa giải mã.")
            return

        # Điều chỉnh độ dài khóa
        adjusted_key = self.adjust_key_length(algo, key)
        key_base64 = base64.b64encode(adjusted_key).decode()  # Chuyển thành base64 để tương thích với Decryptor

        decryptor = Decryptor(algo, key_base64)
        decrypted_text = decryptor.decrypt_text(encrypted_text)
        self.result.setText(f"Giải mã thành công:\n{decrypted_text}")

    def encrypt_file(self):
        """Gọi class Encryptor để mã hóa file"""
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

        encryptor.encrypt_file(file_path, save_path)
        self.result.setText(f"Mã hóa file thành công: {save_path}")

    def decrypt_file(self):
        """Gọi class Decryptor để giải mã file"""
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

        adjusted_key = self.adjust_key_length(algo, key)
        key_base64 = base64.b64encode(adjusted_key).decode()

        decryptor = Decryptor(algo, key_base64)
        save_path, _ = QFileDialog.getSaveFileName(self, "Lưu file giải mã", file_path[:-4], "All Files (*)")
        if not save_path:
            self.result.setText("Hủy lưu file.")
            return

        result = decryptor.decrypt_file(file_path, save_path)
        self.result.setText(result)
