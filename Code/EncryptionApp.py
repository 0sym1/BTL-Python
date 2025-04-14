from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
                             QFileDialog, QComboBox, QLineEdit, QTextEdit, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame,
                             QMessageBox, QDialog, QDialogButtonBox)
import base64
import os
import pandas as pd
import logging
from Encrypt import Encryptor
from Decrypt import Decryptor
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from AI.ai_suggest_v2 import recommend_algorithm, explain_recommendation, retrain_model

# Thiết lập logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class EncryptionApp(QWidget):
    def __init__(self, main_screen=None):
        super().__init__()
        self.main_screen = main_screen
        self.selected_file = None
        self.last_suggestion = None
        self.initUI()
        logging.info("EncryptionApp initialized")

    def initUI(self):
        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        self.btn_back = QPushButton("Quay lại")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setIcon(QIcon("icons/back.png"))
        self.btn_back.setStyleSheet("""
            QPushButton {
                padding: 8px; 
                font-size: 14px; 
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #B0BEC5, stop: 1 #555
                );
                color: white; 
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #CFD8DC, stop: 1 #78909C
                );
            }
        """)
        header_layout.addWidget(self.btn_back)

        title_label = QLabel("Ứng dụng Mã hóa và Giải mã")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff; margin: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)

        algo_layout = QHBoxLayout()
        self.label = QLabel("Chọn thuật toán:")
        self.label.setStyleSheet("font-size: 16px; color: #ffffff; font-weight: bold;")
        algo_layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(["AES", "3DES", "Blowfish"])
        self.combo.setStyleSheet("padding: 5px; font-size: 16px; color: #ffffff; background-color: #333; border: 1px solid #555; border-radius: 5px; font-weight: bold;")
        algo_layout.addWidget(self.combo)
        left_layout.addLayout(algo_layout)

        file_layout = QHBoxLayout()
        file_label = QLabel("Chọn file:")
        file_label.setStyleSheet("font-size: 16px; color: #ffffff; font-weight: bold;")
        file_layout.addWidget(file_label)

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Chọn file để gợi ý thuật toán")
        self.file_input.setReadOnly(True)
        self.file_input.setStyleSheet("padding: 5px; font-size: 16px; border: 1px solid #555; border-radius: 5px;")
        file_layout.addWidget(self.file_input)

        self.btn_select_file = QPushButton("Chọn")
        self.btn_select_file.clicked.connect(self.select_file_for_suggestion)
        self.btn_select_file.setStyleSheet("""
            padding: 5px; 
            font-size: 16px; 
            background-color: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #B0BEC5, stop: 1 #555
            );
            color: white; 
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """)
        file_layout.addWidget(self.btn_select_file)
        left_layout.addLayout(file_layout)

        sensitivity_layout = QHBoxLayout()
        sensitivity_label = QLabel("Độ nhạy cảm:")
        sensitivity_label.setStyleSheet("font-size: 16px; color: #ffffff; font-weight: bold;")
        sensitivity_layout.addWidget(sensitivity_label)

        self.sensitivity_combo = QComboBox()
        self.sensitivity_combo.addItems(["Thấp (0)", "Trung bình (1)", "Cao (2)"])
        self.sensitivity_combo.setStyleSheet("padding: 5px; font-size: 16px; color: #ffffff; background-color: #333; border: 1px solid #555; border-radius: 5px; font-weight: bold;")
        sensitivity_layout.addWidget(self.sensitivity_combo)
        left_layout.addLayout(sensitivity_layout)

        speed_layout = QHBoxLayout()
        speed_label = QLabel("Ưu tiên tốc độ:")
        speed_label.setStyleSheet("font-size: 16px; color: #ffffff; font-weight: bold;")
        speed_layout.addWidget(speed_label)

        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["Không (0)", "Có (1)"])
        self.speed_combo.setStyleSheet("padding: 5px; font-size: 16px; color: #ffffff; background-color: #333; border: 1px solid #555; border-radius: 5px; font-weight: bold;")
        speed_layout.addWidget(self.speed_combo)
        left_layout.addLayout(speed_layout)

        self.btn_suggest = QPushButton("Gợi ý thuật toán")
        self.btn_suggest.clicked.connect(self.suggest_algorithm)
        self.btn_suggest.setIcon(QIcon("icons/suggest.png"))
        self.btn_suggest.setStyleSheet("""
            padding: 10px; 
            font-size: 16px; 
            background-color: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #4FC3F7, stop: 1 #0E7D92
            );
            color: white; 
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """)
        left_layout.addWidget(self.btn_suggest)

        self.btn_feedback = QPushButton("Phản hồi gợi ý")
        self.btn_feedback.clicked.connect(self.collect_feedback)
        self.btn_feedback.setIcon(QIcon("icons/feedback.png"))
        self.btn_feedback.setStyleSheet("""
            padding: 10px; 
            font-size: 16px; 
            background-color: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #CE93D8, stop: 1 #9C27B0
            );
            color: white; 
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """)
        left_layout.addWidget(self.btn_feedback)

        key_layout = QHBoxLayout()
        key_label = QLabel("Nhập khóa:")
        key_label.setStyleSheet("font-size: 16px; color: #ffffff; font-weight: bold;")
        key_layout.addWidget(key_label)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Nhập khóa (sẽ tự điều chỉnh nếu quá ngắn/dài)")
        self.key_input.setStyleSheet("padding: 5px; font-size: 16px; border: 1px solid #555; border-radius: 5px;")
        key_layout.addWidget(self.key_input)
        left_layout.addLayout(key_layout)

        text_label = QLabel("Nhập văn bản:")
        text_label.setStyleSheet("font-size: 16px; color: #ffffff; font-weight: bold;")
        left_layout.addWidget(text_label)

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Nhập văn bản để mã hóa/giải mã")
        self.text_input.setStyleSheet("padding: 5px; font-size: 16px; border: 1px solid #555; border-radius: 5px;")
        left_layout.addWidget(self.text_input)

        content_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(20)

        self.btn_encrypt = QPushButton("Mã hóa Văn bản")
        self.btn_encrypt.clicked.connect(self.encrypt_text)
        self.btn_encrypt.setIcon(QIcon("icons/encrypt.png"))
        self.btn_encrypt.setStyleSheet("""
            padding: 20px; 
            font-size: 20px; 
            background-color: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #A5D6A7, stop: 1 #4CAF50
            );
            color: white; 
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """)
        right_layout.addWidget(self.btn_encrypt)

        self.btn_decrypt = QPushButton("Giải mã Văn bản")
        self.btn_decrypt.clicked.connect(self.decrypt_text)
        self.btn_decrypt.setIcon(QIcon("icons/decrypt.png"))
        self.btn_decrypt.setStyleSheet("""
            padding: 20px; 
            font-size: 20px; 
            background-color: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #90CAF9, stop: 1 #2196F3
            );
            color: white; 
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """)
        right_layout.addWidget(self.btn_decrypt)

        self.btn_encrypt_file = QPushButton("Mã hóa File")
        self.btn_encrypt_file.clicked.connect(self.encrypt_file)
        self.btn_encrypt_file.setIcon(QIcon("icons/file_encrypt.png"))
        self.btn_encrypt_file.setStyleSheet("""
            padding: 20px; 
            font-size: 20px; 
            background-color: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #A5D6A7, stop: 1 #4CAF50
            );
            color: white; 
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """)
        right_layout.addWidget(self.btn_encrypt_file)

        self.btn_decrypt_file = QPushButton("Giải mã File")
        self.btn_decrypt_file.clicked.connect(self.decrypt_file)
        self.btn_decrypt_file.setIcon(QIcon("icons/file_decrypt.png"))
        self.btn_decrypt_file.setStyleSheet("""
            padding: 20px; 
            font-size: 20px; 
            background-color: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #90CAF9, stop: 1 #2196F3
            );
            color: white; 
            border: none;
            border-radius: 5px;
            font-weight: bold;
        """)
        right_layout.addWidget(self.btn_decrypt_file)

        content_layout.addLayout(right_layout)

        main_layout.addLayout(content_layout)

        result_label = QLabel("Kết quả:")
        result_label.setStyleSheet("font-size: 16px; color: #ffffff; margin-top: 10px;font-weight: bold;")
        main_layout.addWidget(result_label)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setStyleSheet("padding: 5px; font-size: 16px; border: 1px solid #555; border-radius: 5px; background-color: #333; color: #fff;")
        main_layout.addWidget(self.result)

        self.setLayout(main_layout)
        self.setWindowTitle("Ứng dụng Mã hóa và Giải mã")
        self.resize(1600, 800)
        self.setStyleSheet("background-color: #1e1e2f;")
        logging.info("UI setup completed")

    def go_back(self):
        if self.main_screen:
            self.main_screen.show()
        self.hide()
        logging.info("Back button clicked")

    def adjust_key_length(self, algo, key):
        try:
            key_bytes = key.encode('utf-8')
            required_lengths = {"AES": 32, "3DES": 24, "Blowfish": 16}
            required_length = required_lengths[algo]
            if len(key_bytes) < required_length:
                key_bytes = key_bytes + b'\x00' * (required_length - len(key_bytes))
            elif len(key_bytes) > required_length:
                key_bytes = key_bytes[:required_length]
            return key_bytes
        except Exception as e:
            logging.error(f"Error in adjust_key_length: {str(e)}")
            raise

    def select_file_for_suggestion(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file để gợi ý thuật toán")
            if file_path:
                self.selected_file = file_path
                self.file_input.setText(file_path)
                logging.info(f"File selected for suggestion: {file_path}")
        except Exception as e:
            logging.error(f"Error in select_file_for_suggestion: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể chọn file: {str(e)}")

    def get_file_type(self, file_path):
        try:
            extension = os.path.splitext(file_path)[1].lower()
            if extension in ['.txt', '.doc', '.docx', '.pdf']:
                return 0  # Text
            elif extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                return 1  # Image
            elif extension in ['.mp3', '.wav', '.aac']:
                return 2  # Audio
            elif extension in ['.mp4', '.avi', '.mkv', '.mov']:
                return 3  # Video
            logging.info(f"File type determined: {extension} -> 0 (Text)")
            return 0  # Mặc định là Text
        except Exception as e:
            logging.error(f"Error in get_file_type: {str(e)}")
            return 0

    def suggest_algorithm(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn file trước khi gợi ý thuật toán.")
            logging.warning("Suggest algorithm attempted without file selection")
            return

        try:
            size_bytes = os.path.getsize(self.selected_file)
            size_mb = size_bytes / (1024 * 1024)
            file_type = self.get_file_type(self.selected_file)
            sensitivity = int(self.sensitivity_combo.currentText().split('(')[1][0])
            speed_priority = int(self.speed_combo.currentText().split('(')[1][0])

            suggested_algo = recommend_algorithm(size_mb, file_type, sensitivity, speed_priority)
            explanation = explain_recommendation(suggested_algo, size_mb, sensitivity, speed_priority)

            self.last_suggestion = {
                'size_mb': size_mb,
                'type': file_type,
                'sensitivity': sensitivity,
                'speed_priority': speed_priority,
                'suggested_algo': suggested_algo
            }

            self.combo.setCurrentText(suggested_algo)
            QMessageBox.information(self, "Gợi ý thuật toán",
                                    f"Thuật toán được gợi ý: {suggested_algo}\nLý do: {explanation}")
            logging.info(f"Algorithm suggested: {suggested_algo}, Reason: {explanation}")
        except Exception as e:
            logging.error(f"Error in suggest_algorithm: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể gợi ý thuật toán: {str(e)}")

    def collect_feedback(self):
        logging.info("collect_feedback started")
        if not self.last_suggestion:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng gợi ý thuật toán trước khi phản hồi.")
            logging.warning("Feedback attempted without prior suggestion")
            return

        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("Phản hồi gợi ý thuật toán")
            dialog_layout = QVBoxLayout()

            label = QLabel("Bạn có đồng ý với thuật toán được gợi ý? Nếu không, chọn thuật toán bạn muốn:")
            dialog_layout.addWidget(label)

            feedback_combo = QComboBox()
            feedback_combo.addItems(["AES", "3DES", "Blowfish"])
            feedback_combo.setCurrentText(self.last_suggestion['suggested_algo'])
            dialog_layout.addWidget(feedback_combo)

            buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            dialog_layout.addWidget(buttons)

            dialog.setLayout(dialog_layout)
            logging.info("Feedback dialog created")

            if dialog.exec() == QDialog.DialogCode.Accepted:
                chosen_algo = feedback_combo.currentText()
                feedback_data = {
                    'size_mb': self.last_suggestion['size_mb'],
                    'type': self.last_suggestion['type'],
                    'sensitivity': self.last_suggestion['sensitivity'],
                    'speed_priority': self.last_suggestion['speed_priority'],
                    'chosen_algorithm': chosen_algo
                }
                logging.info(f"Feedback collected: {feedback_data}")

                feedback_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_feedback.csv')
                feedback_df = pd.DataFrame([feedback_data])
                try:
                    if os.path.exists(feedback_file):
                        feedback_df.to_csv(feedback_file, mode='a', header=False, index=False)
                    else:
                        feedback_df.to_csv(feedback_file, index=False)
                    logging.info(f"Feedback saved to {feedback_file}")

                    # Gọi retrain_model để huấn luyện lại mô hình
                    retrain_model()
                    logging.info("Model retrained successfully")

                    QMessageBox.information(self, "Phản hồi", "Phản hồi đã được ghi nhận và mô hình AI đã được huấn luyện lại.")
                except Exception as e:
                    logging.error(f"Error saving feedback to CSV or retraining model: {str(e)}")
                    QMessageBox.critical(self, "Lỗi", f"Không thể lưu phản hồi hoặc huấn luyện lại mô hình: {str(e)}")
            else:
                logging.info("Feedback dialog cancelled")
        except Exception as e:
            logging.error(f"Error in collect_feedback: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể xử lý phản hồi: {str(e)}")

    def encrypt_text(self):
        try:
            text = self.text_input.toPlainText()
            algo = self.combo.currentText()
            key = self.key_input.text().strip()

            if key:
                adjusted_key = self.adjust_key_length(algo, key)
                encryptor = Encryptor(algo, adjusted_key)
            else:
                encryptor = Encryptor(algo)
                self.key_input.setText(base64.b64encode(encryptor.key).decode())

            encrypted_text = encryptor.encrypt_text(text)
            self.result.setText(f"Mã hóa thành công:\n{encrypted_text}")
            logging.info("Text encrypted successfully")
        except Exception as e:
            logging.error(f"Error in encrypt_text: {str(e)}")
            self.result.setText(f"Lỗi: {str(e)}")

    def decrypt_text(self):
        try:
            encrypted_text = self.text_input.toPlainText().strip()
            algo = self.combo.currentText()
            key = self.key_input.text().strip()

            if not key:
                self.result.setText("Vui lòng nhập khóa giải mã.")
                logging.warning("Decrypt text attempted without key")
                return

            decryptor = Decryptor(algo, key)
            decrypted_text = decryptor.decrypt_text(encrypted_text)
            self.result.setText(f"Giải mã thành công:\n{decrypted_text}")
            logging.info("Text decrypted successfully")
        except ValueError as e:
            logging.error(f"ValueError in decrypt_text: {str(e)}")
            self.result.setText(f"Lỗi: {str(e)}")
        except Exception as e:
            logging.error(f"Error in decrypt_text: {str(e)}")
            self.result.setText(f"Lỗi không xác định: {str(e)}")

    def encrypt_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file để mã hóa")
            if not file_path:
                logging.info("File encryption cancelled: No file selected")
                return

            algo = self.combo.currentText()
            key = self.key_input.text().strip()

            if key:
                adjusted_key = self.adjust_key_length(algo, key)
                encryptor = Encryptor(algo, adjusted_key)
            else:
                encryptor = Encryptor(algo)
                self.key_input.setText(base64.b64encode(encryptor.key).decode())

            save_path, _ = QFileDialog.getSaveFileName(self, "Lưu file đã mã hóa", file_path + ".enc", "All Files (*)")
            if not save_path:
                self.result.setText("Hủy lưu file.")
                logging.info("File encryption cancelled: No save path")
                return

            result = encryptor.encrypt_file(file_path, save_path)
            self.result.setText(result)
            logging.info(f"File encrypted: {file_path} -> {save_path}")
        except Exception as e:
            logging.error(f"Error in encrypt_file: {str(e)}")
            self.result.setText(f"Lỗi: {str(e)}")

    def decrypt_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file để giải mã")
            if not file_path:
                logging.info("File decryption cancelled: No file selected")
                return

            if not file_path.endswith(".enc"):
                self.result.setText("File không hợp lệ! Vui lòng chọn file có đuôi .enc.")
                logging.warning("Invalid file selected for decryption")
                return

            algo = self.combo.currentText()
            key = self.key_input.text().strip()

            if not key:
                self.result.setText("Vui lòng nhập khóa giải mã.")
                logging.warning("Decrypt file attempted without key")
                return

            decryptor = Decryptor(algo, key)
            save_path, _ = QFileDialog.getSaveFileName(self, "Lưu file giải mã", file_path[:-4], "All Files (*)")
            if not save_path:
                self.result.setText("Hủy lưu file.")
                logging.info("File decryption cancelled: No save path")
                return

            result = decryptor.decrypt_file(file_path, save_path)
            self.result.setText(result)
            logging.info(f"File decrypted: {file_path} -> {save_path}")
        except ValueError as e:
            logging.error(f"ValueError in decrypt_file: {str(e)}")
            self.result.setText(f"Lỗi: {str(e)}")
        except Exception as e:
            logging.error(f"Error in decrypt_file: {str(e)}")
            self.result.setText(f"Lỗi không xác định: {str(e)}")