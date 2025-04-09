from Cryptodome.Cipher import AES, DES3, Blowfish
from Cryptodome.Random import get_random_bytes
import base64
import random
import string

class Encryptor:
    def __init__(self, algo, key=None):
        self.algo = algo
        self.key = key if key else self.generate_key()

    def generate_key(self):
        if self.algo == "AES":
            return get_random_bytes(32)
        elif self.algo == "3DES":
            return get_random_bytes(24)
        elif self.algo == "Blowfish":
            return get_random_bytes(16)

    def encrypt_text(self, text):
        try:
            if self.algo == "AES":
                cipher = AES.new(self.key, AES.MODE_EAX)
            elif self.algo == "3DES":
                cipher = DES3.new(self.key, DES3.MODE_EAX)
            elif self.algo == "Blowfish":
                cipher = Blowfish.new(self.key, Blowfish.MODE_EAX)

            ciphertext, tag = cipher.encrypt_and_digest(text.encode())
            tag_length = len(tag).to_bytes(1, byteorder='big')  # Lưu độ dài tag (1 byte)
            encrypted_data = tag_length + cipher.nonce + tag + ciphertext
            print(f"[Encrypt] Tag length: {len(tag)}, Nonce: {len(cipher.nonce)}, Ciphertext: {len(ciphertext)}")
            return base64.b64encode(encrypted_data).decode()
        except Exception as e:
            return f"Lỗi mã hóa: {str(e)}"

    def encrypt_file(self, file_path, save_path):
        try:
            with open(file_path, "rb") as f:
                plaintext = f.read()

            if self.algo == "AES":
                cipher = AES.new(self.key, AES.MODE_EAX)
            elif self.algo == "3DES":
                cipher = DES3.new(self.key, DES3.MODE_EAX)
            elif self.algo == "Blowfish":
                cipher = Blowfish.new(self.key, Blowfish.MODE_EAX)

            ciphertext, tag = cipher.encrypt_and_digest(plaintext)
            tag_length = len(tag).to_bytes(1, byteorder='big')
            encrypted_data = tag_length + cipher.nonce + tag + ciphertext
            print(f"[Encrypt File] Tag length: {len(tag)}, Nonce: {len(cipher.nonce)}, Ciphertext: {len(ciphertext)}")

            with open(save_path, "wb") as f:
                f.write(encrypted_data)
            return f"Mã hóa file thành công: {save_path}"
        except Exception as e:
            return f"Lỗi mã hóa file: {str(e)}"
        
    def adjust_key_length(algo, key):
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