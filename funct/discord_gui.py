"""

@author: Team Mizogg
"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
import json

ICO_ICON = "images/main/miz.ico"
TITLE_ICON = "images/main/title.png"
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