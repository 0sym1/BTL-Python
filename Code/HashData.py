from Cryptodome.Cipher import AES, DES3, Blowfish
from Cryptodome.Random import get_random_bytes
import base64
import bcrypt

class HashData:
    def hasing(text):
        """Băm mật khẩu và trả về dạng string"""
        return bcrypt.hashpw(text.encode(), bcrypt.gensalt()).decode()
    
    def verify(text, hashed_text):
        """Kiểm tra mật khẩu nhập vào có khớp với hash trong DB không"""
        return bcrypt.checkpw(text.encode(), hashed_text.encode())
    