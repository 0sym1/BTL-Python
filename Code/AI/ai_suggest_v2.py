# ai_suggest_v2.py
import joblib
import numpy as np
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'crypto_data_1000.csv')
FEEDBACK_FILE = os.path.join(BASE_DIR, 'user_feedback.csv')
MODEL_FILE = os.path.join(BASE_DIR, 'crypto_recommend_updated.pkl')

algo_map = {0: "AES", 1: "Blowfish", 2: "3DES"}
algo_map_reverse = {v: k for k, v in algo_map.items()}

def assign_algorithm_by_score(row):
    size = row['size_mb']
    sensitivity = row['sensitivity']
    speed = row['speed_priority']

    score_aes = 0.5 * size + 1.5 * sensitivity - 1.0 * speed
    score_blowfish = -1.2 * size + 0.5 * sensitivity + 2.0 * speed
    score_3des = 0.3 * size + 0.8 * sensitivity + 0.8 * speed

    scores = [score_aes, score_blowfish, score_3des]
    return np.argmax(scores)

def generate_training_data():
    np.random.seed(42)
    data = {
        'size_mb': np.random.uniform(0.1, 200, 1000),
        'type': np.random.randint(0, 4, 1000),
        'sensitivity': np.random.randint(0, 3, 1000),
        'speed_priority': np.random.randint(0, 2, 1000)
    }
    df = pd.DataFrame(data)
    df['algorithm'] = df.apply(assign_algorithm_by_score, axis=1)
    df.to_csv(DATA_FILE, index=False)
    return df

def retrain_model():
    print("\n🚀 Đang huấn luyện mô hình...")
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = generate_training_data()

    if os.path.exists(FEEDBACK_FILE):
        feedback = pd.read_csv(FEEDBACK_FILE)
        feedback['algorithm'] = feedback['chosen_algorithm'].map(algo_map_reverse)
        feedback = feedback.drop(columns=['chosen_algorithm'])
        df = pd.concat([df, feedback], ignore_index=True)

    X = df[['size_mb', 'type', 'sensitivity', 'speed_priority']]
    y = df['algorithm']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    joblib.dump(model, MODEL_FILE)
    print(f"✅ Mô hình huấn luyện xong. Độ chính xác: {acc * 100:.2f}%\n")
    return model

# Kiểm tra hoặc huấn luyện lại mô hình
if not os.path.exists(MODEL_FILE):
    model = retrain_model()
else:
    model = joblib.load(MODEL_FILE)
    print(f"📦 Đã tải mô hình từ {MODEL_FILE}")

def recommend_algorithm(size_mb, file_type, sensitivity, speed_priority):
    input_data = np.array([[size_mb, file_type, sensitivity, speed_priority]])
    prediction = model.predict(input_data)[0]
    return algo_map[prediction]

def explain_recommendation(pred, size, sens, speed):
    if pred == "AES":
        return "Vì file lớn, dữ liệu nhạy cảm, không yêu cầu tốc độ cao."
    elif pred == "Blowfish":
        return "Vì file nhỏ và bạn ưu tiên tốc độ xử lý."
    else:
        return "Vì đặc điểm dữ liệu trung tính, nên chọn thuật toán cân bằng như 3DES."

