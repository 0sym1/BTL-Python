import string
import secrets
import random

class GenPass:
    def generate_strong_password(length=None):
        if length is None:
            length = random.randint(12, 24)  # Random độ dài từ 12 đến 24 ký tự 
        
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
