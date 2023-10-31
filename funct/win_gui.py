"""

@author: Team Mizogg
"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPlainTextEdit, QPushButton
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

ICO_ICON = "webfiles/css/images/main/miz.ico"
TITLE_ICON = "webfiles/css/images/main/title.png"
# WinnerDialog: Custom QDialog for displaying winner information.
class WinnerDialog(QDialog):
    def __init__(self, WINTEXT, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QTMizICE_Display.py  WINNER")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.setMinimumSize(640, 440)
        pixmap = QPixmap(f"{TITLE_ICON}")
        # Create a QLabel and set the pixmap as its content
        title_label = QLabel()
        title_label.setPixmap(pixmap)
        title_label.setFixedSize(pixmap.size())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(title_label)

        title_label = QLabel("!!!! 🎉 🥳CONGRATULATIONS🥳 🎉 !!!!")
        layout.addWidget(title_label)
        informative_label = QLabel("© MIZOGG 2018 - 2023")
        layout.addWidget(informative_label)
        detail_label = QPlainTextEdit(WINTEXT)
        layout.addWidget(detail_label)
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet(
                "QPushButton { font-size: 16pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 16pt; background-color: #A13316; color: white; }"
            )
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)