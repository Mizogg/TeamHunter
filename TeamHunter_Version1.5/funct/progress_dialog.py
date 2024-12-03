"""
@author: Team Mizogg
"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon

ICO_ICON = "images/miz.ico"

class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("File Found")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))

        layout = QVBoxLayout(self)
        message_label = QLabel("Progress file found. Do you want to delete it?", self)
        layout.addWidget(message_label)

        button_widget = QWidget(self)
        button_layout = QHBoxLayout(button_widget)

        self.keep_button = QPushButton("Keep", self)
        self.keep_button.setStyleSheet(
            "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
            "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
        )
        self.keep_button.clicked.connect(self.keep_clicked)
        button_layout.addWidget(self.keep_button)

        self.delete_button = QPushButton("Delete", self)
        self.delete_button.setStyleSheet(
            "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
            "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
        )
        self.delete_button.clicked.connect(self.delete_clicked)
        button_layout.addWidget(self.delete_button)

        layout.addWidget(button_widget)

    def keep_clicked(self):
        self.done(QDialog.DialogCode.Rejected)

    def delete_clicked(self):
        self.done(QDialog.DialogCode.Accepted)
