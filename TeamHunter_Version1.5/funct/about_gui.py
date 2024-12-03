"""

@author: Team Mizogg
"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QGroupBox, QTextBrowser, QPushButton
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from game.speaker import Speaker
import webbrowser
import platform
version = '1.5'

ICO_ICON = "images/main/miz.ico"
TITLE_ICON = "images/main/title.png"
RED_ICON = "images/main/mizogg-eyes.png"

def open_website():
    webbrowser.open("https://mizogg.co.uk")

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About My QT Hunter")
        self.setWindowIcon(QIcon(ICO_ICON))
        self.setMinimumSize(800, 600)
        self.setStyleSheet("font-size: 14px; font-weight: bold; color: #E7481F;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        header_pixmap = QPixmap(TITLE_ICON)
        header_label = QLabel()
        header_label.setPixmap(header_pixmap)
        layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(20)

        info_group = QGroupBox("Application Information")
        info_layout = QVBoxLayout()

        app_name_label = QLabel("TeamHUnter Puzzles GUI")

        # Determine the current platform (Windows or Linux)
        current_platform = platform.system()

        app_version_label = QLabel(f"Version {version} ({current_platform})")
        app_author_label = QLabel("Made by Team Mizogg")

        info_layout.addWidget(app_name_label)
        info_layout.addWidget(app_version_label)
        info_layout.addWidget(app_author_label)
        info_group.setLayout(info_layout)

        layout.addWidget(info_group)

        description_textbox = QTextBrowser()
        description_textbox.setPlainText(
            "QT Hunter for Bitcoin is a feature-rich application designed for Bitcoin enthusiasts and researchers. "
            "It provides a comprehensive suite of tools for Bitcoin address generation, key scanning, and analysis. "
            "Whether you're hunting for lost Bitcoin addresses, conducting research, or exploring the blockchain, "
            "QT Hunter empowers you with the tools you need to navigate the Bitcoin ecosystem efficiently.\n\n"
            "Help ME.\n"
            "Just by visiting my site https://mizogg.co.uk keep up those clicks\n"
            "Donations welcome. BTC: 3JKyVkRtxDrXEMtZY6Fy53VmvMAT6LKBo8"
        )
        layout.addWidget(description_textbox)

        configurations = [
            ("Bitcrack Configuration", "Recommended for 16GB of RAM: -b 104 -t 512 -p 2016\nRecommended for 8GB of RAM: -b 104 -t 512 -p 1024\n-b = Blocks\n-t = Threads\n-p = points"),
            ("KeyHunter Puzzles GUI Configuration", 
             '''
             KVaules For Ram Usage:

             2 GB Ram -k 128 | 4 GB Ram -k 256 | 8 GB Ram -k 512 | 16 GB Ram -k 1024 | 32 GB Ram -k 2048

             This version is still a beta version, there are a lot of things that can be fail or improve. 
             This version also could have some bugs. please report it.
             Modes
             Keyhunt can work in different ways at different speeds.
             The current available modes are:
             - address
             - bsgs

             This is the most basic approach to work, in this mode your text file need to have a list of the public address to be search.
             '''
            ),
        ]

        for config_title, config_text in configurations:
            config_textbox = QTextBrowser()
            config_textbox.setPlainText(config_text)

            config_group = QGroupBox(config_title)
            config_layout = QVBoxLayout()
            config_layout.addWidget(config_textbox)
            config_group.setLayout(config_layout)
            layout.addWidget(config_group)

        icon_size = QSize(26, 26)
        iconred = QIcon(QPixmap(RED_ICON))

        self.miz_git_mode_button = QPushButton(self)
        self.miz_git_mode_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Help ME. Just by visiting my site https://mizogg.co.uk keep up those clicks. Mizogg Website and Information </span>')
        self.miz_git_mode_button.setStyleSheet("font-size: 12pt;")
        self.miz_git_mode_button.setIconSize(icon_size)
        self.miz_git_mode_button.setIcon(iconred)
        self.miz_git_mode_button.clicked.connect(open_website)
        self.miz_git_mode_button.enterEvent = lambda e: Speaker.play_death()
        layout.addWidget(self.miz_git_mode_button)

        self.setLayout(layout)