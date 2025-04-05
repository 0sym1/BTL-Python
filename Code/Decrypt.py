from Cryptodome.Cipher import AES, DES3, Blowfish
import base64

class Decryptor:
    def __init__(self, algo, key):
        self.algo = algo
        try:
            if isinstance(key, str):
                # Thử giải mã base64 (cho trường hợp tự sinh)
                try:
                    key_bytes = base64.b64decode(key)
                except:
                    # Nếu không phải base64, mã hóa chuỗi thô (cho nhập thủ công)
                    key_bytes = key.encode('utf-8')
            else:
                # Nếu key đã là byte (truyền trực tiếp từ Encryptor)
                key_bytes = key
            self.key = self.adjust_key_length(algo, key_bytes)
        except Exception as e:
            raise ValueError(f"Khóa không hợp lệ: {str(e)}")

    def adjust_key_length(self, algo, key_bytes):
        required_lengths = {"AES": 32, "3DES": 24, "Blowfish": 16}
        required_length = required_lengths[algo]
        if len(key_bytes) < required_length:
            key_bytes = key_bytes + b'\x00' * (required_length - len(key_bytes))
        elif len(key_bytes) > required_length:
            key_bytes = key_bytes[:required_length]
        return key_bytes

    def decrypt_text(self, encrypted_text):
        try:
            encrypted_data = base64.b64decode(encrypted_text)
            if len(encrypted_data) < 17:  # 1 byte tag_length + 16 byte nonce
                return "Lỗi giải mã: Dữ liệu mã hóa không hợp lệ (quá ngắn)"

            tag_length = int.from_bytes(encrypted_data[:1], byteorder='big')
            nonce = encrypted_data[1:17]  # 16 byte nonce
            tag = encrypted_data[17:17 + tag_length]
            ciphertext = encrypted_data[17 + tag_length:]
            print(f"[Decrypt] Tag length: {tag_length}, Nonce: {len(nonce)}, Ciphertext: {len(ciphertext)}")

            if self.algo == "AES":
                cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
            elif self.algo == "3DES":
                cipher = DES3.new(self.key, DES3.MODE_EAX, nonce=nonce)
            elif self.algo == "Blowfish":
                cipher = Blowfish.new(self.key, Blowfish.MODE_EAX, nonce=nonce)

            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext.decode()
        except ValueError as e:
            return f"Lỗi giải mã: Khóa hoặc dữ liệu không hợp lệ ({str(e)})"
        except Exception as e:
            return f"Lỗi giải mã: {str(e)}"

    def decrypt_file(self, file_path, save_path):
        try:
            with open(file_path, "rb") as f:
                encrypted_data = f.read()

            if len(encrypted_data) < 17:
                return "Lỗi giải mã file: Dữ liệu mã hóa không hợp lệ (quá ngắn)"

            tag_length = int.from_bytes(encrypted_data[:1], byteorder='big')
            nonce = encrypted_data[1:17]
            tag = encrypted_data[17:17 + tag_length]
            ciphertext = encrypted_data[17 + tag_length:]
            print(f"[Decrypt File] Tag length: {tag_length}, Nonce: {len(nonce)}, Ciphertext: {len(ciphertext)}")

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
        except ValueError as e:
            return f"Lỗi giải mã file: Khóa hoặc dữ liệu không hợp lệ ({str(e)})"
        except Exception as e:
            return f"Lỗi giải mã file: {str(e)}"
