import smtplib
import random
import pyotp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Cấu hình email server (sử dụng Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "kalyxianua123@gmail.com"
EMAIL_PASSWORD = "uxgs xbre sxjy uvwo"  # App Password, không dùng mật khẩu thật

otp = ''

# Tạo mã OTP
def generate_otp():
    return str(random.randint(100000, 999999))  # Mã OTP 6 chữ số

# Gửi mã OTP qua email
def send_otp(email, otp):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = email
    msg["Subject"] = "Mã xác thực OTP của bạn"

    body = f"Mã OTP của bạn là: {otp}. Mã này có hiệu lực trong 5 phút."
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, email, msg.as_string())
        server.quit()
        print("OTP đã được gửi thành công!")
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")

