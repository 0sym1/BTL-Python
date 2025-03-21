import base64
from Cryptodome.Cipher import AES, DES3, Blowfish
from Cryptodome.Random import get_random_bytes
from PyQt6.QtWidgets import QFileDialog


class Encrypt:
    def generate_key(self, algo):
        if algo == "AES":
            return get_random_bytes(32)
        elif algo == "3DES":
            return get_random_bytes(24)
        elif algo == "Blowfish":
            return get_random_bytes(16)

    def encrypt_text(self, text, algo, key):
        if not text:
            return None, "Vui lòng nhập văn bản để mã hóa."

        if not key:
            key = self.generate_key(algo)
            new_key = base64.b64encode(key).decode()
        else:
            try:
                key = base64.b64decode(key)
                new_key = key
            except:
                return None, "Khóa không hợp lệ."

        if algo == "AES":
            cipher = AES.new(key, AES.MODE_EAX)
        elif algo == "3DES":
            cipher = DES3.new(key, DES3.MODE_EAX)
        elif algo == "Blowfish":
            cipher = Blowfish.new(key, Blowfish.MODE_EAX)

        ciphertext, tag = cipher.encrypt_and_digest(text.encode())
        encrypted_data = base64.b64encode(cipher.nonce + tag + ciphertext).decode()

        return encrypted_data, new_key

    def encrypt_file(self, file_path, algo, key):
        if not key:
            key = self.generate_key(algo)
            new_key = base64.b64encode(key).decode()
        else:
            try:
                key = base64.b64decode(key)
                new_key = key
            except:
                return None, "Khóa không hợp lệ."

        with open(file_path, "rb") as f:
            plaintext = f.read()

        if algo == "AES":
            cipher = AES.new(key, AES.MODE_EAX)
        elif algo == "3DES":
            cipher = DES3.new(key, DES3.MODE_EAX)
        elif algo == "Blowfish":
            cipher = Blowfish.new(key, Blowfish.MODE_EAX)

        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        save_path, _ = QFileDialog.getSaveFileName(None, "Lưu file đã mã hóa", file_path + ".enc", "All Files (*)")
        if not save_path:
            return None, "Hủy lưu file."

        with open(save_path, "wb") as f:
            f.write(cipher.nonce + tag + ciphertext)

        return save_path, new_key
