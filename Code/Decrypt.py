from Cryptodome.Cipher import AES, DES3, Blowfish
import base64

class Decryptor:
    def __init__(self, algo, key):
        self.algo = algo
        self.key = base64.b64decode(key)

    def decrypt_text(self, encrypted_text):
        """Giải mã văn bản"""
        try:
            encrypted_data = base64.b64decode(encrypted_text)
            nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]

            if self.algo == "AES":
                cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
            elif self.algo == "3DES":
                cipher = DES3.new(self.key, DES3.MODE_EAX, nonce=nonce)
            elif self.algo == "Blowfish":
                cipher = Blowfish.new(self.key, Blowfish.MODE_EAX, nonce=nonce)

            return cipher.decrypt_and_verify(ciphertext, tag).decode()
        except Exception as e:
            return f"Lỗi giải mã: {str(e)}"

    def decrypt_file(self, file_path, save_path):
        """Giải mã file"""
        try:
            with open(file_path, "rb") as f:
                encrypted_data = f.read()

            nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]

            if self.algo == "AES":
                cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
            elif self.algo == "3DES":
                cipher = DES3.new(self.key, DES3.MODE_EAX, nonce=nonce)
            elif self.algo == "Blowfish":
                cipher = Blowfish.new(self.key, Blowfish.MODE_EAX, nonce=nonce)

            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

            with open(save_path, "wb") as f:
                f.write(decrypted_data)

            return f"Giải mã file thành công: {save_path}"
        except Exception as e:
            return f"Lỗi giải mã file: {str(e)}"
