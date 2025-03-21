from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QComboBox, QLineEdit, QTextEdit
from Code.Encrypt import Encrypt
from Code.Decrypt import Decrypt


class EncryptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.encryptor = Encrypt()
        self.decryptor = Decrypt()

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

    def encrypt_text(self):
        algo = self.combo.currentText()
        text = self.text_input.toPlainText()
        key = self.key_input.text().strip()

        encrypted_data, new_key = self.encryptor.encrypt_text(text, algo, key)
        if encrypted_data:
            self.result.setText(f"Mã hóa thành công:\n{encrypted_data}")
            self.key_input.setText(new_key)
        else:
            self.result.setText(new_key)

    def decrypt_text(self):
        algo = self.combo.currentText()
        encrypted_data = self.text_input.toPlainText()
        key = self.key_input.text().strip()

        decrypted_data, error = self.decryptor.decrypt_text(encrypted_data, algo, key)
        self.result.setText(decrypted_data if decrypted_data else error)

    def encrypt_file(self):
        algo = self.combo.currentText()
        key = self.key_input.text().strip()
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file để mã hóa")

        if not file_path:
            return

        result, new_key = self.encryptor.encrypt_file(file_path, algo, key)
        if result:
            self.result.setText(f"Mã hóa file thành công: {result}")
            self.key_input.setText(new_key)
        else:
            self.result.setText(new_key)

    def decrypt_file(self):
        algo = self.combo.currentText()
        key = self.key_input.text().strip()
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file để giải mã")

        if not file_path:
            return

        result, error = self.decryptor.decrypt_file(file_path, algo, key)
        if result:
            self.result.setText(f"Giải mã file thành công: {result}")
        else:
            self.result.setText(error)