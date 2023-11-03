"""

@author: Team Mizogg
"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QGroupBox, QTextBrowser
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

version = '0.6'
ICO_ICON = "webfiles/css/images/main/miz.ico"
TITLE_ICON = "webfiles/css/images/main/title.png"
class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About My QT Hunter")
        self.setWindowIcon(QIcon(ICO_ICON))
        self.setMinimumSize(800, 600)
        self.setStyleSheet("font-size: 14px; font-weight: bold; color: #E7481F;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add a header image
        header_pixmap = QPixmap(TITLE_ICON)
        header_label = QLabel()
        header_label.setPixmap(header_pixmap)
        layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add a vertical spacer for better separation
        layout.addSpacing(20)

        # Create a group box for application information
        info_group = QGroupBox("Application Information")
        info_layout = QVBoxLayout()

        app_name_label = QLabel("Team Hunter")
        app_version_label = QLabel(f"Version {version}")
        app_author_label = QLabel("Made by Team Mizogg")

        info_layout.addWidget(app_name_label)
        info_layout.addWidget(app_version_label)
        info_layout.addWidget(app_author_label)
        info_group.setLayout(info_layout)

        layout.addWidget(info_group)

        # Create a QTextBrowser for the description
        description_textbox = QTextBrowser()
        description_textbox.setPlainText(
            "QT Hunter for Bitcoin is a feature-rich application designed for Bitcoin enthusiasts and researchers. "
            "It provides a comprehensive suite of tools for Bitcoin address generation, key scanning, and analysis. "
            "Whether you're hunting for lost Bitcoin addresses, conducting research, or exploring the blockchain, "
            "QT Hunter empowers you with the tools you need to navigate the Bitcoin ecosystem efficiently."
        )
        layout.addWidget(description_textbox)

        # Create QTextBrowser widgets for configuration details
        configurations = [
            ("Bitcrack Configuration", "Recommended for 16GB of RAM: -b 104 -t 512 -p 2016\nRecommended for 8GB of RAM: -b 104 -t 512 -p 1024\n-b = Blocks\n-t = Threads\n-p = points"),
            ("Vanbitcracken Configuration", 
             '''The Newest Version of VanBitCrackenRandom...VBCr
             This program is really only intended for the BTC Challenge. However, you can use it to generate your own personal BTC address and use it.
             It is a spinoff of JLP's original VanitySearch.
             Program supports a simple -bits flag and Begin and End Range (-begr and -endr) flags. New version also supports full address with newer RTX cards.
             It has been tested on Windows 10 and Windows 11 on RTX 30xx cards, RTX 20xx cards and a GTX 1660 Ti card.
             Only working Display is in CMD work in progress'''),
            ("Key Hunt Configuration", 
             '''Run against puzzle 66 (address mode)
             ./keyhunt -m address -f tests/66.txt -b 66 -l compress -R -q -s 10
             This version is still a beta version, there are a lot of things that can be fail or improve. 
             This version also could have some bugs. please report it.
             Modes
             Keyhunt can work in different ways at different speeds.
             The current available modes are:
             address
             rmd160
             xpoint
             bsgs
             Experimental modes
             minikeys
             pub2rmd
             address mode
             This is the most basic approach to work, in this mode your text file need to have a list of the public address to be search.
             Example of address from solved puzzles, this file is already on the repository tests/1to32.txt
             1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH
             1CUNEBjYrCn2y1SdiUMohaKUi4wpP326Lb
             ...
             To target that file we need to execute keyhunt with this line
             ./keyhunt -m address -f tests/1to32.txt -r 1:FFFFFFFF'''
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

        self.setLayout(layout)