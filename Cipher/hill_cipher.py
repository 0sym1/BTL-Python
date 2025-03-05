# # s = input()
# # key = input()

# # def encrypt_hill(s, key):

import numpy as np
import math

# # Hàm tính nghịch đảo modulo 26
# def mod_inverse(det, mod=26):
#     det = det % mod
#     for i in range(1, mod):
#         if (det * i) % mod == 1:
#             return i
#     return None  # Không tồn tại nghịch đảo

# # Hàm kiểm tra ma trận khóa có hợp lệ không
# def is_valid_key(matrix):
#     det = int(round(np.linalg.det(matrix)))  # Tính định thức
#     gcd = np.gcd(det, 26)
#     return det != 0 and gcd == 1  # Kiểm tra định thức ≠ 0 và gcd(det, 26) = 1

# # Hàm chuyển đổi văn bản thành vector số
# def text_to_matrix(text, size):
#     text = text.upper().replace(" ", "")  # Chuyển thành chữ hoa, xóa khoảng trắng
#     while len(text) % size != 0:
#         text += "X"  # Padding nếu cần
#     matrix = [ord(char) - ord('A') for char in text]
#     return np.array(matrix).reshape(-1, size)

# # Hàm chuyển đổi vector số thành văn bản
# def matrix_to_text(matrix):
#     text = "".join(chr(int(num) + ord('A')) for num in matrix.flatten())
#     return text

# # Hàm mã hóa Hill Cipher
# def hill_encrypt(plain_text, key_matrix):
#     size = len(key_matrix)
#     plain_matrix = text_to_matrix(plain_text, size)
#     cipher_matrix = (np.dot(plain_matrix, key_matrix) % 26).flatten()
#     return matrix_to_text(cipher_matrix)

# # Hàm giải mã Hill Cipher
# def hill_decrypt(cipher_text, key_matrix):
#     size = len(key_matrix)
#     det = int(round(np.linalg.det(key_matrix)))  # Định thức của ma trận khóa
#     det_inv = mod_inverse(det, 26)  # Nghịch đảo modulo 26

#     if det_inv is None:
#         return "Không thể giải mã: Ma trận khóa không khả nghịch!"

#     # Tính ma trận nghịch đảo modulo 26
#     adj_matrix = np.round(det * np.linalg.inv(key_matrix)).astype(int) % 26
#     inv_key_matrix = (det_inv * adj_matrix) % 26

#     cipher_matrix = text_to_matrix(cipher_text, size)
#     plain_matrix = (np.dot(cipher_matrix, inv_key_matrix) % 26).flatten()
#     return matrix_to_text(plain_matrix)

# # Nhập dữ liệu từ người dùng
# plain_text = input("Nhập bản rõ: ").strip()
# key_input = input("Nhập ma trận khóa (các số cách nhau bởi dấu cách): ").strip()

# # Chuyển ma trận khóa từ chuỗi thành mảng số
# key_numbers = list(map(int, key_input.split()))
# size = int(len(key_numbers) ** 0.5)

# if size * size != len(key_numbers):
#     print("Lỗi: Ma trận khóa phải là ma trận vuông!")
# else:
#     key_matrix = np.array(key_numbers).reshape(size, size)

#     if not is_valid_key(key_matrix):
#         print("Lỗi: Ma trận khóa không hợp lệ (det = 0 hoặc gcd(det, 26) ≠ 1)!")
#     else:
#         cipher_text = hill_encrypt(plain_text, key_matrix)
#         decrypted_text = hill_decrypt(cipher_text, key_matrix)

#         print(f"\n🔐 Mã hóa: {cipher_text}")
#         print(f"🔓 Giải mã: {decrypted_text}")


s = input()
key = list(map(int, input().strip().split()))

def check_matrix(matrix):
    det = int(round(np.linalg.det(matrix)))  # Tính định thức
    gcd = np.gcd(det, 26)
    return det != 0 and gcd == 1  # Kiểm tra định thức ≠ 0 và gcd(det, 26) = 1

def text_to_matrix(text, size):
    text = text.upper().replace(" ", "")  # Chuyển thành chữ hoa, xóa khoảng trắng

    # Tính số cột cần có

    cols = math.ceil(len(text) / size)
    print(cols)
    # Thêm padding nếu cần
    while len(text) % size != 0:
        text += "X"  # Padding bằng 'X' (23)

    # Khởi tạo ma trận NumPy với số nguyên
    matrix = np.zeros((size, cols), dtype=int)

    # Điền giá trị vào ma trận theo hàng
    for i in range(size):
        for j in range(cols):
            matrix[i][j] = ord(text[i * cols + j]) - ord('A')

    return matrix

def matrix_to_text(matrix):
    text = ""
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            text += chr(int(matrix[i][j]) + ord('A'))
    return text

def hill_encrypt(plain_text, key_matrix):
    size = len(key_matrix)
    plain_matrix = text_to_matrix(plain_text, size)
    cipher_matrix = np.dot(key_matrix, plain_matrix) % 26

    print(plain_matrix)
    print(key_matrix)
    print(cipher_matrix)
    return matrix_to_text(cipher_matrix)

size = int(len(key) ** 0.5)
if(size * size != len(key)):
    print("Lỗi: Ma trận khóa phải là ma trận vuông!")

else:
    key_matrix = np.array(key).reshape(size, size)

    if not check_matrix(key_matrix):
        print("Lỗi: Ma trận khóa không hợp lệ (det = 0 hoặc gcd(det, 26) ≠ 1)!")
    else:
        cipher_text = hill_encrypt(s, key_matrix)
        print(cipher_text)

