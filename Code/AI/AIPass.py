import joblib
import numpy as np
import re

class AIPass:
    # Load model và scaler đã lưu
    scaler = joblib.load('Code/AI/scaler.pkl')
    model = joblib.load('Code/AI/model.pkl')


    # Hàm phân tích mật khẩu
    def extract_features(self, password):
        length = len(password)
        capital = sum(1 for c in password if c.isupper())
        small = sum(1 for c in password if c.islower())
        special = sum(1 for c in password if re.search(r'[!@#$%^&*(),.?":{}|<>]', c))
        numeric = sum(1 for c in password if c.isdigit())
        
        return np.array([[length, capital, small, special, numeric]])
    
    def classifier_pass(self, password):
        # Trích xuất đặc trưng từ mật khẩu
        user_input = self.extract_features(password)

        # Chuẩn hóa dữ liệu đầu vào
        user_input_scaled = self.scaler.transform(user_input)

        # Dự đoán mức độ mạnh yếu của mật khẩu
        prediction = self.model.predict(user_input_scaled)

        # Hiển thị kết quả
        return prediction[0]
        # print("Mức độ mạnh yếu của mật khẩu:", prediction[0])
