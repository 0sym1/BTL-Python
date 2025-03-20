from PyQt6.QtWidgets import (QApplication)

from UI.EncryptionApp import EncryptionApp

if __name__ == "__main__":
    app = QApplication([])
    window = EncryptionApp()
    window.show()
    app.exec()
