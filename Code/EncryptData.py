# from Cryptodome.Cipher import AES, DES3, Blowfish
# from Cryptodome.Random import get_random_bytes
# import base64

# class EncyptData:
#     def generate_key(self, algo):
#         if algo == "AES":
#             return get_random_bytes(32)
#         elif algo == "3DES":
#             return get_random_bytes(24)
#         elif algo == "Blowfish":
#             return get_random_bytes(16)
        
#     def encrypt_file(self, plain_text):
#         algo = "AES"
#         key = self.generate_key(algo)

#         # with open(file_path, "rb") as f:
#         #     plaintext = f.read()

#         cipher = AES.new(key, AES.MODE_EAX)

#         ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode())

#         # with open(save_path, "wb") as f:
#         #     f.write(cipher.nonce + tag + ciphertext)

#         return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

#     def decrypt_file(self):
#         algo = "AES"
#         key = self.key_input.text().strip()

#         if not key:
#             self.result.setText("Vui lòng nhập khóa giải mã.")
#             return

#         try:
#             key = base64.b64decode(key)
#         except:
#             self.result.setText("Khóa không hợp lệ.")
#             return

#         try:
#             with open(file_path, "rb") as f:
#                 encrypted_data = f.read()

#             nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]

#             if algo == "AES":
#                 cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
#             elif algo == "3DES":
#                 cipher = DES3.new(key, DES3.MODE_EAX, nonce=nonce)
#             elif algo == "Blowfish":
#                 cipher = Blowfish.new(key, Blowfish.MODE_EAX, nonce=nonce)

#             decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

#             # Chọn nơi lưu file sau khi giải mã
#             save_path, _ = QFileDialog.getSaveFileName(self, "Lưu file giải mã", file_path[:-4], "All Files (*)")
#             if not save_path:  # Nếu người dùng bấm Hủy
#                 self.result.setText("Hủy lưu file.")
#                 return

#             with open(save_path, "wb") as f:
#                 f.write(decrypted_data)

#             self.result.setText(f"Giải mã file thành công: {save_path}")

#         except Exception as e:
#             self.result.setText(f"Lỗi giải mã file: {str(e)}")
