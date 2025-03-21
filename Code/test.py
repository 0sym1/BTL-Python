from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
                             QFileDialog, QComboBox, QLineEdit, QTextEdit)
from Cryptodome.Cipher import AES, DES3, Blowfish
from Cryptodome.Random import get_random_bytes
import base64

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
        self.key_input.setPlaceholderText("Nhập khóa (để trống để tự sinh khóa)")
        layout.addWidget(self.key_input)

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Nhập văn bản để mã hóa/giải mã")
        layout.addWidget(self.text_input)

        self.btn_encrypt = QPushButton("Mã hóa")
        self.btn_encrypt.clicked.connect(self.encrypt_text)
        layout.addWidget(self.btn_encrypt)

        self.btn_decrypt = QPushButton("Giải mã")
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

    def generate_key(self, algo):
        if algo == "AES":
            return get_random_bytes(32)
        elif algo == "3DES":
            return get_random_bytes(24)
        elif algo == "Blowfish":
            return get_random_bytes(16)

    def encrypt_text(self):
        """Mã hóa văn bản"""
        text = self.text_input.toPlainText()
        if not text:
            self.result.setText("Vui lòng nhập văn bản để mã hóa.")
            return

        algo = self.combo.currentText()
        key = self.key_input.text().strip()

        if not key:
            key = self.generate_key(algo)
            self.key_input.setText(base64.b64encode(key).decode())
        else:
            try:
                key = base64.b64decode(key)
            except:
                self.result.setText("Khóa không hợp lệ.")
                return

        if algo == "AES":
            cipher = AES.new(key, AES.MODE_EAX)
        elif algo == "3DES":
            cipher = DES3.new(key, DES3.MODE_EAX)
        elif algo == "Blowfish":
            cipher = Blowfish.new(key, Blowfish.MODE_EAX)

        ciphertext, tag = cipher.encrypt_and_digest(text.encode())
        encrypted_data = base64.b64encode(cipher.nonce + tag + ciphertext).decode()

        self.result.setText(f"Mã hóa thành công:\n{encrypted_data}")

    def decrypt_text(self):
        """Giải mã văn bản"""
        encrypted_data = self.text_input.toPlainText().strip()
        if not encrypted_data:
            self.result.setText("Vui lòng nhập văn bản đã mã hóa.")
            return

        algo = self.combo.currentText()
        key = self.key_input.text().strip()

        if not key:
            self.result.setText("Vui lòng nhập khóa giải mã.")
            return

        try:
            key = base64.b64decode(key)
        except:
            self.result.setText("Khóa không hợp lệ.")
            return

        try:
            encrypted_data = base64.b64decode(encrypted_data)
            nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]

            if algo == "AES":
                cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            elif algo == "3DES":
                cipher = DES3.new(key, DES3.MODE_EAX, nonce=nonce)
            elif algo == "Blowfish":
                cipher = Blowfish.new(key, Blowfish.MODE_EAX, nonce=nonce)

            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
            self.result.setText(f"Giải mã thành công:\n{decrypted_data.decode()}")

        except Exception as e:
            self.result.setText(f"Lỗi giải mã: {str(e)}")

    def encrypt_file(self):
        """Mã hóa file và cho phép chọn nơi lưu"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file để mã hóa")
        if not file_path:
            return

        algo = self.combo.currentText()
        key = self.key_input.text().strip()

        if not key:
            key = self.generate_key(algo)
            self.key_input.setText(base64.b64encode(key).decode())
        else:
            try:
                key = base64.b64decode(key)
            except:
                self.result.setText("Khóa không hợp lệ.")
                return

        with open(file_path, "rb") as f:
            plaintext = f.read()

        if algo == "AES":
            cipher = AES.new(key, AES.MODE_EAX)
        elif algo == "3DES":
            cipher = DES3.new(key, DES3.MODE_EAX)
        elif algo == "Blowfish":
            cipher = Blowfish.new(key, Blowfish.MODE_EAX)

        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        # Chọn nơi lưu file đã mã hóa
        save_path, _ = QFileDialog.getSaveFileName(self, "Lưu file đã mã hóa", file_path + ".enc", "All Files (*)")
        if not save_path:  # Nếu người dùng bấm Hủy
            self.result.setText("Hủy lưu file.")
            return

        with open(save_path, "wb") as f:
            f.write(cipher.nonce + tag + ciphertext)

        self.result.setText(f"Mã hóa file thành công: {save_path}")

    def decrypt_file(self):
        """Giải mã file và cho phép chọn nơi lưu"""
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
            key = base64.b64decode(key)
        except:
            self.result.setText("Khóa không hợp lệ.")
            return

        try:
            with open(file_path, "rb") as f:
                encrypted_data = f.read()

            nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]

            if algo == "AES":
                cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            elif algo == "3DES":
                cipher = DES3.new(key, DES3.MODE_EAX, nonce=nonce)
            elif algo == "Blowfish":
                cipher = Blowfish.new(key, Blowfish.MODE_EAX, nonce=nonce)

            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

            # Chọn nơi lưu file sau khi giải mã
            save_path, _ = QFileDialog.getSaveFileName(self, "Lưu file giải mã", file_path[:-4], "All Files (*)")
            if not save_path:  # Nếu người dùng bấm Hủy
                self.result.setText("Hủy lưu file.")
                return

            with open(save_path, "wb") as f:
                f.write(decrypted_data)

            self.result.setText(f"Giải mã file thành công: {save_path}")

        except Exception as e:
            self.result.setText(f"Lỗi giải mã file: {str(e)}")



if __name__ == "__main__":
    app = QApplication([])
    window = EncryptionApp()
    window.show()
    app.exec()
