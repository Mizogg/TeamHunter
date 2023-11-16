"""

@author: Team Mizogg
"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
import sys
sys.path.extend(['libs', 'config', 'funct'])

from config import *

ICO_ICON = "images/main/miz.ico"
TITLE_ICON = "images/main/title.png"

class Settings_telegram_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Load and populate the settings if they exist in config.json
        config_data = self.load_config()
        telegram_config = config_data.get("Telegram", {})
        token = telegram_config.get("token", "")
        chat_id = telegram_config.get("chatid", "")
        self.setWindowTitle("Telegram Settings")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.setMinimumSize(640, 440)
        pixmap = QPixmap(f"{TITLE_ICON}")
        title_label = QLabel()
        title_label.setPixmap(pixmap)
        title_label.setFixedSize(pixmap.size())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.token_label = QLabel("Token:")
        self.token_edit = QLineEdit()
        
        self.chatid_label = QLabel("Chat ID:")
        self.chatid_edit = QLineEdit()
        
        self.token_edit.setText(token)
        self.chatid_edit.setText(chat_id)

        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(
                "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
            )
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(
            "QPushButton { font-size: 12pt; background-color: #1E1E1E; color: white; }"
            "QPushButton:hover { font-size: 12pt; background-color: #5D6062; color: white; }"
        )
        
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.token_label)
        layout.addWidget(self.token_edit)
        layout.addWidget(self.chatid_label)
        layout.addWidget(self.chatid_edit)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)
        
        self.setLayout(layout)
        
        self.save_button.clicked.connect(self.update_config_address)
        self.cancel_button.clicked.connect(self.reject)
    
    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_config(self, config_data):
        with open(CONFIG_FILE, "w") as file:
            json.dump(config_data, file, indent=4)

    def update_config_address(self):
        token = self.token_edit.text()
        chat_id = self.chatid_edit.text()
        config_data = self.load_config()
        config_data["Telegram"] = {
            "token": token,
            "chatid": chat_id
        }
        self.save_config(config_data)

        self.accept()