"""

@author: Team Mizogg
"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
import json
import requests
from config import *

ICO_ICON = "images/miz.ico"
TITLE_ICON = "images/title.png"
CONFIG_FILE = "config/settings.json"
class Settings_telegram_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.cancel_button = QPushButton("Cancel")
        
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

def send_to_telegram(self, text):
    settings = Settings_telegram_Dialog.load_config(self)
    apiToken = settings.get("Telegram", {}).get("token", "").strip()
    chatID = settings.get("Telegram", {}).get("chatid", "").strip()

    if not apiToken or not chatID:
        token_message = "No token or ChatID found in CONFIG_FILE"
        QMessageBox.information(self, "No token or ChatID", token_message)
        return

    apiURL = f"https://api.telegram.org/bot{apiToken}/sendMessage"

    try:
        response = requests.post(apiURL, json={"chat_id": chatID, "text": text})
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        error_message = f"HTTP Error: {errh}"
        QMessageBox.critical(self, "Error", error_message)
    except Exception as e:
        error_message = f"Telegram error: {str(e)}"
        QMessageBox.critical(self, "Error", error_message)