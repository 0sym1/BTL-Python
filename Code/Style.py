class Style:
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                font-family: 'Segoe UI', sans-serif;
                color: #f0f0f0;
                font-size: 16px;
            }

            QLabel {
                font-size: 28px;
                font-weight: 600;
                color: #f8f8f8;
            }

            QPushButton {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #4e54c8, stop: 1 #8f94fb
                );
                border: none;
                border-radius: 12px;
                padding: 12px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #5a60d1, stop: 1 #9ca1fd
                );
            }

            QPushButton:pressed {
                background-color: #3b3f87;
            }
        """)

    def apply_styles_v2(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                font-family: 'Segoe UI', sans-serif;
                color: #f0f0f0;
                font-size: 8px;
            }

            QLabel {
                font-size: 28px;
                font-weight: 600;
                color: #f8f8f8;
            }

            QPushButton {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #4e54c8, stop: 1 #8f94fb
                );
                border: none;
                border-radius: 12px;
                padding: 12px;
                color: white;
                font-weight: bold;
                font-size: 5px;
            }

            QPushButton:hover {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #5a60d1, stop: 1 #9ca1fd
                );
            }

            QPushButton:pressed {
                background-color: #3b3f87;
            }
        """)