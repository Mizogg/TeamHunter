"""

@author: Team Mizogg
"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

ICO_ICON = "webfiles/css/images/main/miz.ico"
TITLE_ICON = "webfiles/css/images/main/title.png"

class Settings_discord_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Discord Settings")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.setMinimumSize(640, 440)
        pixmap = QPixmap(f"{TITLE_ICON}")
        # Create a QLabel and set the pixmap as its content
        title_label = QLabel()
        title_label.setPixmap(pixmap)
        title_label.setFixedSize(pixmap.size())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.webhook_url_label = QLabel("Discord webhook_url:")
        self.webhook_url_edit = QLineEdit()
        
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(
                "QPushButton { font-size: 16pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 16pt; background-color: #A13316; color: white; }"
            )
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(
            "QPushButton { font-size: 16pt; background-color: #1E1E1E; color: white; }"
            "QPushButton:hover { font-size: 16pt; background-color: #5D6062; color: white; }"
        )
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.webhook_url_label)
        layout.addWidget(self.webhook_url_edit)
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)
        
        self.setLayout(layout)
        
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.reject)
    
    def save_settings(self):
        # Get the entered token and chatid
        webhook_url = self.webhook_url_edit.text()
        if self.parent().dark_mode == True:
            theme = "dark"
        else:
            theme = "light"
        # Write the settings to the settings.txt file
        with open('settings.txt', 'w') as file:
            file.write(
f'''// Choose default theme [light] / [dark]
theme={theme}

// Discord Settings
webhook_url={webhook_url}'''
            )
        self.accept()  # Close the dialog