import base64
from Cryptodome.Cipher import AES, DES3, Blowfish
from PyQt6.QtWidgets import QFileDialog


class Decrypt:
    def decrypt_text(self, encrypted_data, algo, key):
        if not encrypted_data:
            return None, "Vui lòng nhập văn bản đã mã hóa."

        if not key:
            return None, "Vui lòng nhập khóa giải mã."

        try:
            key = base64.b64decode(key)
        except:
            return None, "Khóa không hợp lệ."

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
            return decrypted_data.decode(), None

        except Exception as e:
            return None, f"Lỗi giải mã: {str(e)}"
