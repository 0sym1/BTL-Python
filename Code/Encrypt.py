from Cryptodome.Cipher import AES, DES3, Blowfish
from Cryptodome.Random import get_random_bytes
import base64


class Encryptor:
    def __init__(self, algo, key=None):
        self.algo = algo
        self.key = key or self.generate_key()

    def generate_key(self):
        """Tạo khóa ngẫu nhiên theo thuật toán đã chọn"""
        if self.algo == "AES":
            return get_random_bytes(32)
        elif self.algo == "3DES":
            return get_random_bytes(24)
        elif self.algo == "Blowfish":
            return get_random_bytes(16)

    def encrypt_text(self, text):
        """Mã hóa văn bản"""
        if self.algo == "AES":
            cipher = AES.new(self.key, AES.MODE_EAX)
        elif self.algo == "3DES":
            cipher = DES3.new(self.key, DES3.MODE_EAX)
        elif self.algo == "Blowfish":
            cipher = Blowfish.new(self.key, Blowfish.MODE_EAX)

        ciphertext, tag = cipher.encrypt_and_digest(text.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

    def encrypt_file(self, file_path, save_path):
        """Mã hóa file"""
        with open(file_path, "rb") as f:
            plaintext = f.read()

        if self.algo == "AES":
            cipher = AES.new(self.key, AES.MODE_EAX)
        elif self.algo == "3DES":
            cipher = DES3.new(self.key, DES3.MODE_EAX)
        elif self.algo == "Blowfish":
            cipher = Blowfish.new(self.key, Blowfish.MODE_EAX)

        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        with open(save_path, "wb") as f:
            f.write(cipher.nonce + tag + ciphertext)
    
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
