"""
@author: Team Mizogg
"""
import os
import sys
import subprocess
import signal
import webbrowser
import platform
import subprocess
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from game import snake_gui, Start_game
from funct import (set_settings, create_setting, range_div_gui, about_gui, ice_gui, bitcrack_gui, keyhunt_gui, Kangaroo_gui, grid_16x16, miz_mnemonic, miz_poetry, conversion_gui, balance_gui, brain_gui, xpub_gui, calculator, vanbit_gui, wallet_gui)
from Mizmusic import MusicPlayer
sys.path.extend(['config', 'funct', 'found', 'input', 'game', 'images'])
from game.speaker import Speaker
from config import *

current_platform = platform.system()
IMAGES_MAIN = "images/main/"
image_folder = "images"
RED_ICON = f"{IMAGES_MAIN}/mizogg-eyes.png"
image_files = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
version = '1.5'

def open_website(self):
    webbrowser.open("https://mizogg.co.uk")

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Team Hunter GUI")
        self.setWindowIcon(QIcon(f"{IMAGES_MAIN}miz.ico"))
        self.move(30, 30)
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.icon_size = QSize(26, 26)
        self.images_main = IMAGES_MAIN
        self.tabmain = QWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tab7 = QWidget()
        self.tab8 = QWidget()
        self.tab9 = QWidget()
        self.tab10 = QWidget()
        self.tab11 = QWidget()
        self.tab12 = QWidget()

        self.tab_widget.addTab(self.tabmain, "Welcome")
        self.tab_widget.addTab(self.tab1, "BitCrack")
        self.tab_widget.addTab(self.tab2, "VanBit")
        self.tab_widget.addTab(self.tab3, "KeyHunt")
        self.tab_widget.addTab(self.tab4, "Kangaroo")
        self.tab_widget.addTab(self.tab5, "Iceland2k14 Secp256k1")
        self.tab_widget.addTab(self.tab6, "Miz Mnemonic")
        self.tab_widget.addTab(self.tab7, "Brain Hunter")
        self.tab_widget.addTab(self.tab8, "Miz Poetry")
        self.tab_widget.addTab(self.tab9, "XPUB")
        self.tab_widget.addTab(self.tab10, "BTC Snake Game")
        self.tab_widget.addTab(self.tab11, "Art Work")
        self.tab_widget.addTab(self.tab12, "CAL")
        
        self.process = None
        self.scanning = False
        self.initUI()

    def initUI(self):
        Speaker.play_death()
        menubar = self.menuBar()
        def add_menu_action(menu, text, function):
            action = QAction(text, self)
            action.triggered.connect(function)
            menu.addAction(action)

        file_menu = menubar.addMenu("File")
        add_menu_action(file_menu, "New Window", self.new_window)
        file_menu.addSeparator()

        file_menu.addSeparator()
        add_menu_action(file_menu, "Quit", self.exit_app)

        help_menu = menubar.addMenu("Help")
        add_menu_action(help_menu, "Help Telegram Group", self.open_telegram)
        add_menu_action(help_menu, "About", self.about)
        self.timer = QTimer(self)

        self.main_layout = QVBoxLayout()

        git_label = QLabel("GitHub Links")

        self.alberto_mode_button = self.create_button("GitHub Alertobsd Keyhunt About", "python-snake-black.png", self.alberto_git)
        self.bitcrack_mode_button = self.create_button("GitHub brichard19 BitCrack About", "python-snake-red.png", self.bitcrack_git)
        self.iceland_mode_button = self.create_button("GitHub Iceland iceland2k14 Python Secp256k1 About", "python-snake-black.png", self.iceland_git)
        self.miz_git_mode_button = self.create_button("GitHub Mizogg About", "python-snake-red.png", self.miz_git)

        dark_label = QLabel("EXTRA TOOLS (16x16 Grid, Tetris, Range Division, Conversion, Balance, Mute/UnMute, Wallet)")

        self.grid_mode_button = self.create_button("Run 16x16 Grid Hunter", "grid.png", self.load_16x16)
        self.tetris_mode_button = self.create_button("Play The GAME Tetris Bitcoin Finder", "Tetris.png", self.tetris_play, hover_sound=Speaker.row_deleted)
        self.div_mode_button = self.create_button("Range Division in HEX", "Range.png", self.range_check)
        self.cov_mode_button = self.create_button("Conversion Tools", "Conversion.png", self.conv_check)
        self.bal_mode_button = self.create_button("Balance Check BTC", "walletpic.png", self.balcheck)
        self.mute_mode_button = self.create_button("Mute sound effects", "mute.png", self.mute_sound, is_checkbox=True)
        self.wallet_mode_button = self.create_button("Wallet Check", "walletpic.png", self.wallet_check)

        dark_mode_layout = QHBoxLayout()
        dark_mode_layout.addWidget(git_label)
        dark_mode_layout.addWidget(self.alberto_mode_button)
        dark_mode_layout.addWidget(self.bitcrack_mode_button)
        dark_mode_layout.addWidget(self.iceland_mode_button)
        dark_mode_layout.addWidget(self.miz_git_mode_button)

        dark_mode_layout.addStretch()
        dark_mode_layout.addWidget(dark_label)
        dark_mode_layout.addWidget(self.grid_mode_button)
        dark_mode_layout.addWidget(self.tetris_mode_button)
        dark_mode_layout.addWidget(self.div_mode_button)
        dark_mode_layout.addWidget(self.cov_mode_button)
        dark_mode_layout.addWidget(self.bal_mode_button)
        dark_mode_layout.addWidget(self.mute_mode_button)
        dark_mode_layout.addWidget(self.wallet_mode_button)

        self.main_layout.addLayout(dark_mode_layout)

        labels_info = [
            {"text": f"Made by Team Mizogg", "object_name": "madeby"},
            {"text": f"Full Version {version} ({current_platform})", "object_name": f"{current_platform}_version"},
            {"text": "© mizogg.com 2018 - 2024", "object_name": "copyright"},
            {
                "text": f"Running Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}",
                "object_name": "versionpy",
            },
        ]

        dot_labels = [QLabel("●", objectName=f"dot{i}") for i in range(1, 4)]
        icon_size = QSize(26, 26)
        iconred = QIcon(QPixmap(RED_ICON))
        def create_miz_git_mode_button():
            button = QPushButton(self)
            button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Help ME. Just by visiting my site https://mizogg.co.uk keep up those clicks. Mizogg Website and Information </span>')
            button.setStyleSheet("font-size: 12pt;")
            button.setIconSize(icon_size)
            button.setIcon(iconred)
            button.clicked.connect(open_website)
            return button

        self.miz_git_mode_button = create_miz_git_mode_button()
        self.miz_git_mode_button1 = create_miz_git_mode_button()

        credit_label = QHBoxLayout()
        credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credit_label.addWidget(self.miz_git_mode_button)
        mizlogo = QPixmap(f"{IMAGES_MAIN}mizogglogo.png")
        miz_label = QLabel(self)
        miz_label.setPixmap(mizlogo)
        miz_label1 = QLabel(self)
        miz_label1.setPixmap(mizlogo)
        credit_label.addWidget(miz_label)
        for info in labels_info:
            label = QLabel(info["text"])
            credit_label.addWidget(label)
            if dot_labels:
                dot_label = dot_labels.pop(0)
                credit_label.addWidget(dot_label)
        credit_label.addWidget(miz_label1)
        credit_label.addWidget(self.miz_git_mode_button1)
        self.main_layout.addWidget(self.tab_widget)
        
        self.tabmain_layout = QVBoxLayout()
        self.tab1_layout = QVBoxLayout()
        self.tab2_layout = QVBoxLayout()
        self.tab3_layout = QVBoxLayout()
        self.tab4_layout = QVBoxLayout()
        self.tab5_layout = QVBoxLayout()
        self.tab6_layout = QVBoxLayout()
        self.tab7_layout = QVBoxLayout()
        self.tab8_layout = QVBoxLayout()
        self.tab9_layout = QVBoxLayout()
        self.tab10_layout = QVBoxLayout()
        self.tab11_layout = QVBoxLayout()
        self.tab12_layout = QVBoxLayout()

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)
        bitcrack_tool = bitcrack_gui.BitcrackFrame()
        keyhunt_tool = keyhunt_gui.KeyHuntFrame()
        kangaroo_tool = Kangaroo_gui.KangarooFrame()
        ice_tool = ice_gui.GUIInstance()
        MIZ_tool = miz_mnemonic.GUIInstance()
        MIZP_tool = miz_poetry.GUIInstance()
        BRAIN_tool = brain_gui.GUIInstance()
        XPUB_tool = xpub_gui.GUIInstance()
        VAN_tool = vanbit_gui.VanbitFrame()
        snake_frame = snake_gui.Window()
        cal_frame = calculator.MyMainWindow()
        
        self.tabmain_layout = self.main_tab()
        self.tab1_layout.addWidget(bitcrack_tool)
        self.tab2_layout.addWidget(VAN_tool)
        self.tab3_layout.addWidget(keyhunt_tool)
        self.tab4_layout.addWidget(kangaroo_tool)
        self.tab5_layout.addWidget(ice_tool)
        self.tab6_layout.addWidget(MIZ_tool)
        self.tab7_layout.addWidget(BRAIN_tool)
        self.tab8_layout.addWidget(MIZP_tool)
        self.tab9_layout.addWidget(XPUB_tool)
        self.tab10_layout.addWidget(snake_frame)
        self.tab11_layout = self.picture_tab()
        self.tab12_layout.addWidget(cal_frame)

        self.tabmain.setLayout(self.tabmain_layout)
        self.tab1.setLayout(self.tab1_layout)
        self.tab2.setLayout(self.tab2_layout)
        self.tab3.setLayout(self.tab3_layout)
        self.tab4.setLayout(self.tab4_layout)
        self.tab5.setLayout(self.tab5_layout)
        self.tab6.setLayout(self.tab6_layout)
        self.tab7.setLayout(self.tab7_layout)
        self.tab8.setLayout(self.tab8_layout)
        self.tab9.setLayout(self.tab9_layout)
        self.tab10.setLayout(self.tab10_layout)
        self.tab11.setLayout(self.tab11_layout)
        self.tab12.setLayout(self.tab12_layout)

        self.layout.addLayout(self.main_layout)
        mizogg_player = MusicPlayer()
        self.main_layout.addWidget(mizogg_player)
        self.layout.addLayout(credit_label)

    def create_button(self, tooltip, icon_name, callback, hover_sound=None, is_checkbox=False):
        button = QPushButton(self)
        button.setToolTip(f'<span style="font-size: 10pt; font-weight: bold; color: black;">{tooltip}</span>')
        button.setStyleSheet("font-size: 12pt;")
        button.setIconSize(self.icon_size)
        icon = QIcon(QPixmap(f"{self.images_main}{icon_name}"))
        button.setIcon(icon)
        button.clicked.connect(callback)
        
        if hover_sound:
            button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(hover_sound))
        else:
            button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        
        return button


    def create_tab_buttons(self):
        buttons_layout = QGridLayout()

        tabs = ["BitCrack", "VanBitCracken", "KeyHunt", "Kangaroo", "Iceland2k14 Secp256k1", "Miz Mnemonic", "Brain Hunter", "Miz Poetry", "XPUB Tool", "BTC Snake Game", "CAL", "16x16 Grid"]
        
        for i, tab_name in enumerate(tabs):
            row = i // 4
            col = i % 4

            button = QPushButton(tab_name)

            if tab_name == "16x16 Grid":
                button.clicked.connect(self.load_16x16)
            else:
                button.clicked.connect(self.switch_to_tab(i + 1))

            button.setStyleSheet(
                "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
            )

            button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
            buttons_layout.addWidget(button, row, col)

        return buttons_layout


    def main_tab(self):
        pixmap = QPixmap(f"{IMAGES_MAIN}title.png")
        title_label = QLabel(self)
        title_label.setPixmap(pixmap)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutmain = QVBoxLayout()
        labels_layout = QHBoxLayout()
        combined_text = """
        <html><center>
        <font size="13" color="#E7481F">❤️ Welcome to TeamHunter ₿itcoin & Crypto Scanner ❤️</font>

        <br><font size="4">
        This Python application, named "Team Hunter GUI," provides a user-friendly interface for various cryptocurrency-related tools and functions.<br>
        Users can access tools for Bitcoin-related operations, including BitCrack, VanBitCraken, KeyHunt, Iceland2k14 Secp256k1....<br>
        It also features a 16x16 grid tool, a range division tool in hexadecimal format, and allows users to open external websites.<br>
        This application is built using PyQt6 and is designed to assist cryptocurrency enthusiasts in their endeavors.</font>
        <br><br><font size="5" color="#E7481F">
        Database Files have to be stored in the Input folder
        <br>
        Found Files will be inside the Found Folder
        </center></font><br></html>
        """

        welcome_label = QLabel(combined_text)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        buttons_layout = self.create_tab_buttons()
        layoutmain.addWidget(title_label)
        layoutmain.addWidget(welcome_label)
        layoutmain.addLayout(buttons_layout)
        return layoutmain
    
    def switch_to_tab(self, tab_index):
        def switch():
            self.tab_widget.setCurrentIndex(tab_index)
        return switch

    def picture_tab(self):
        picture_layout = QHBoxLayout()
        for image_path in image_files:
            pixmap = QPixmap(image_path)
            pic_label = QLabel()
            pic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tab_size = self.tab_widget.widget(0).size()
            scaled_pixmap = pixmap.scaled(tab_size, Qt.AspectRatioMode.KeepAspectRatio)
            pic_label.setPixmap(scaled_pixmap)
            pic_label.setFixedSize(scaled_pixmap.size())
            picture_layout.addWidget(pic_label)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(QWidget())
        scroll_area.widget().setLayout(picture_layout)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        next_button = QPushButton("Next")
        prev_button = QPushButton("Previous")
        current_index = 0

        def next_picture():
            nonlocal current_index
            current_index = (current_index + 1) % len(image_files)
            scroll_area.horizontalScrollBar().setValue(current_index * tab_size.width())

        def prev_picture():
            nonlocal current_index
            current_index = (current_index - 1 + len(image_files)) % len(image_files)
            scroll_area.horizontalScrollBar().setValue(current_index * tab_size.width())

        next_button.clicked.connect(next_picture)
        prev_button.clicked.connect(prev_picture)
        button_layout = QVBoxLayout()
        button_layout.addWidget(prev_button)
        button_layout.addWidget(next_button)
        pic_layout = QVBoxLayout()
        pic_layout.addWidget(scroll_area)
        pic_layout.addLayout(button_layout)
        return pic_layout

    def range_check(self):
        range_dialog = range_div_gui.RangeDialog(self)
        range_dialog.show()

    def wallet_check(self):
        wallet_dialog = wallet_gui.WalletFrame(self)
        wallet_dialog.show()     

    def load_16x16(self):
        self.frame_16x16 = grid_16x16.GridFrame()
        self.frame_16x16.show()


    def exit_app(self):
        QApplication.quit()

    def about(self):
        about_dialog = about_gui.AboutDialog(self)
        about_dialog.show()

    def open_telegram(self):
        webbrowser.open("https://t.me/TeamHunter_GUI")

    def alberto_git(self):
        webbrowser.open("https://github.com/albertobsd/keyhunt")

    def bitcrack_git(self):
        webbrowser.open("https://github.com/brichard19/BitCrack")

    def iceland_git(self):
        webbrowser.open("https://github.com/iceland2k14/secp256k1")

    def miz_git(self):
        webbrowser.open("https://github.com/Mizogg")

    def conv_check(self):
        conv_dialog = conversion_gui.ConversionDialog(self)
        conv_dialog.show()

    def balcheck(self):
        balance_dialog = balance_gui.BalanceDialog(self)
        balance_dialog.show()

    def tetris_play(self):
        self.tetris_dialog = Start_game.LauncherWindow()
        self.tetris_dialog.show()

    def mute_sound(self):
        Speaker.toggle_mute()
        if Speaker.muted:
            self.mute_mode_button.setIcon(QIcon(QPixmap(f"{self.images_main}sound.png")))
        else:
            self.mute_mode_button.setIcon(QIcon(QPixmap(f"{self.images_main}mute.png")))

    @pyqtSlot()
    def new_window(self):
        python_cmd = f'start cmd /c "{sys.executable}" TeamHunter.py'
        subprocess.Popen(python_cmd, shell=True)

if __name__ == "__main__":
    create_setting.create_settings_file_if_not_exists()
    settings = set_settings.get_settings()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())