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
CONFIG_FILE = "config/config.json"
class Settings_discord_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Discord Settings")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.setMinimumSize(640, 440)
        config_data = self.load_config()
        discord_config = config_data.get("Discord", {})
        webhookurl = discord_config.get("webhook_url", "")

        pixmap = QPixmap(f"{TITLE_ICON}")
        # Create a QLabel and set the pixmap as its content
        title_label = QLabel()
        title_label.setPixmap(pixmap)
        title_label.setFixedSize(pixmap.size())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.webhook_url_label = QLabel("Discord webhook_url:")
        self.webhook_url_edit = QLineEdit()
        self.webhook_url_edit.setText(webhookurl)
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
        layout.addWidget(self.webhook_url_label)
        layout.addWidget(self.webhook_url_edit)
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
        webhookurl = self.webhook_url_edit.text()
        config_data = self.load_config()
        config_data["Discord"] = {
            "webhook_url": webhookurl,
        }
        self.save_config(config_data)

        self.accept()

def send_to_discord(self, text):
    settings = Settings_discord_Dialog.load_config(self)  # Load settings from config.json
    webhook_url = settings.get("Discord", {}).get("webhook_url", "").strip()
    headers = {'Content-Type': 'application/json'}

    payload = {
        'content': text
    }

    try:
        response = requests.post(webhook_url, json=payload, headers=headers)

        if response.status_code == 204:
            print('Message sent to Discord successfully!')
        else:
            print(f'Failed to send message to Discord. Status Code: {response.status_code}')
    except Exception as e:
        print(f'Error sending message to Discord: {str(e)}')