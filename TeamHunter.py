"""
@author: Team Mizogg
"""
import os
import subprocess
import webbrowser
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import QWebEngineView
import qdarktheme
from libs import set_settings, create_setting
from game import snake_gui, Start_game
from funct import (range_div_gui, about_gui, ice_gui, bitcrack_gui, keyhunt_gui, vanbit_gui, up_bloom_gui, grid_16x16, mnemonic_gui, miz_mnemonic, conversion_gui, balance_gui, wallet_gui)
import sys
sys.path.extend(['libs', 'config', 'funct', 'found', 'input', 'game'])
from speaker import Speaker
from config import *

ICO_ICON = "webfiles/css/images/main/miz.ico"
TITLE_ICON = "webfiles/css/images/main/titlebig.png"
BC_ICON = "webfiles/css/images/main/logobc.png"
MIZ_ICON = "webfiles/css/images/main/mizogg-eyes.png"
LOYCE_ICON = "webfiles/css/images/main/loyce.png"
BLACK_ICON = "webfiles/css/images/main/python-snake-black.png"
RED_ICON = "webfiles/css/images/main/python-snake-red.png"
BAL_ICON = "webfiles/css/images/main/Balance.png"
COV_ICON = "webfiles/css/images/main/Conversion.png"
RANGE_ICON = "webfiles/css/images/main/Range.png"
ICON_16x16 = "webfiles/css/images/main/grid.png"
SUN_ICON = "webfiles/css/images/main/sun.png"
MOON_ICON = "webfiles/css/images/main/moon.png"
WALLET_ICON = "webfiles/css/images/main/walletpic.png"
TETRIS_ICON = "webfiles/css/images/main/Tetris.png"
image_folder = "webfiles/css/images"
image_files = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

version = '0.7'

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Team Hunter GUI")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.setGeometry(50, 50, 1600, 900)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

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
        self.tab_widget.addTab(self.tab2, "KeyHunt")
        self.tab_widget.addTab(self.tab3, "Vanbitcracken")
        self.tab_widget.addTab(self.tab4, "C-Sharp-Mnemonic")
        self.tab_widget.addTab(self.tab5, "Iceland2k14 Secp256k1")
        self.tab_widget.addTab(self.tab6, "Miz Mnemonic")
        self.tab_widget.addTab(self.tab7, "Conversion Tools / BrainWallet")
        self.tab_widget.addTab(self.tab8, "Mnemonic Tools")
        self.tab_widget.addTab(self.tab9, "Mizogg's Tools")
        self.tab_widget.addTab(self.tab10, "BTC Snake Game")
        self.tab_widget.addTab(self.tab11, "Race Game")
        self.tab_widget.addTab(self.tab12, "Art Work")
        self.process = None
        self.scanning = False
        self.initUI()
        self.theme_preference = self.get_theme_preference()
        self.dark_mode = self.theme_preference == "dark"
        self.toggle_theme()
        icon_size = QSize(32, 32)
        self.dark_mode_button.setIconSize(icon_size)
        if self.theme_preference == "dark":
            iconsun = QIcon(QPixmap(SUN_ICON))
            pixsun = QPixmap(iconsun)
            self.dark_mode_button.setIcon(pixsun)
            self.load_dark_mode()
            self.dark_mode = True
        elif self.theme_preference == "light":
            iconmoon = QIcon(QPixmap(MOON_ICON))
            pixmoon = QPixmap(iconmoon)
            self.dark_mode_button.setIcon(pixmoon)
            self.load_light_mode()
            self.dark_mode = False

    def load_dark_mode(self):
        qdarktheme.setup_theme("dark")

    def load_light_mode(self):
        qdarktheme.setup_theme("light")

    def initUI(self):
        Speaker.play_death()
        self.init_webviews()
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

        icon_size = QSize(32, 32)
        iconbc = QIcon(QPixmap(BC_ICON))
        iconmiz = QIcon(QPixmap(MIZ_ICON))
        iconloyce = QIcon(QPixmap(LOYCE_ICON))
        iconblack = QIcon(QPixmap(BLACK_ICON))
        iconred = QIcon(QPixmap(RED_ICON))
        iconbal = QIcon(QPixmap(BAL_ICON))
        iconrange = QIcon(QPixmap(RANGE_ICON))
        iconcon = QIcon(QPixmap(COV_ICON))
        icon16x16 = QIcon(QPixmap(ICON_16x16))
        iconwallet = QIcon(QPixmap(WALLET_ICON))
        tetrisicon = QIcon(QPixmap(TETRIS_ICON))

        main_layout = QVBoxLayout()
        dark_label = QLabel("EXTRA TOOLS (16x16 Grid, Range Divsion, Conversion, Balance, Dark/Light)")
        self.dark_mode_button = QPushButton(self)
        self.dark_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;">Switch Between Dark and Light Theme</span>')
        self.dark_mode_button.setStyleSheet("font-size: 16px;")
        self.dark_mode_button.clicked.connect(self.toggle_theme)
        self.dark_mode_button.setChecked(True if self.get_theme_preference() == "dark" else False)
        self.dark_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        self.grid_mode_button = QPushButton(self)
        self.grid_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;">Run 16x16 Grid Hunter</span>')
        self.grid_mode_button.setStyleSheet("font-size: 16px;")
        self.grid_mode_button.setIconSize(icon_size)
        self.grid_mode_button.setIcon(icon16x16)
        self.grid_mode_button.clicked.connect(self.load_16x16)
        self.grid_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        self.wallet_mode_button = QPushButton(self)
        self.wallet_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;">Wallet Recovery (Work in Progress)</span>')
        self.wallet_mode_button.setStyleSheet("font-size: 16px;")
        self.wallet_mode_button.setIconSize(icon_size)
        self.wallet_mode_button.setIcon(iconwallet)
        self.wallet_mode_button.clicked.connect(self.wallet_check)
        self.wallet_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        self.tetris_mode_button = QPushButton(self)
        self.tetris_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;">Play The GAME Tetris Bitcoin Finder</span>')
        self.tetris_mode_button.setStyleSheet("font-size: 16px;")
        self.tetris_mode_button.setIconSize(icon_size)
        self.tetris_mode_button.setIcon(tetrisicon)
        self.tetris_mode_button.clicked.connect(self.tetris_play)
        self.tetris_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        self.div_mode_button = QPushButton(self)
        self.div_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;">Range Divsion in HEX </span>')
        self.div_mode_button.setStyleSheet("font-size: 16px;")
        self.div_mode_button.setIconSize(icon_size)
        self.div_mode_button.setIcon(iconrange)
        self.div_mode_button.clicked.connect(self.range_check)
        self.div_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        self.cov_mode_button = QPushButton(self)
        self.cov_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;"> Conversion Tools </span>')
        self.cov_mode_button.setStyleSheet("font-size: 16px;")
        self.cov_mode_button.setIconSize(icon_size)
        self.cov_mode_button.setIcon(iconcon)
        self.cov_mode_button.clicked.connect(self.conv_check)
        self.cov_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        self.bal_mode_button = QPushButton(self)
        self.bal_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;"> Balance Check BTC </span>')
        self.bal_mode_button.setStyleSheet("font-size: 16px;")
        self.bal_mode_button.setIconSize(icon_size)
        self.bal_mode_button.setIcon(iconbal)
        self.bal_mode_button.clicked.connect(self.balcheck)
        self.bal_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        favs_label = QLabel("Miz Favs")
        self.blockchain_mode_button = QPushButton(self)
        self.blockchain_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;">Blockchain.com (Relentlessly building the future of finance since 2011)</span>')
        self.blockchain_mode_button.setStyleSheet("font-size: 16px;")
        self.blockchain_mode_button.setIconSize(icon_size)
        self.blockchain_mode_button.setIcon(iconbc)
        self.blockchain_mode_button.clicked.connect(self.blockchain_check)
        self.blockchain_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        self.mizogg_mode_button = QPushButton(self)
        self.mizogg_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;">Mizogg.co.uk (Come Meet Mizogg Check out my Website and other programs)</span>')
        self.mizogg_mode_button.setStyleSheet("font-size: 16px;")
        self.mizogg_mode_button.setIconSize(icon_size)
        self.mizogg_mode_button.setIcon(iconmiz)
        self.mizogg_mode_button.clicked.connect(self.open_website)
        self.mizogg_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        self.loyce_mode_button = QPushButton(self)
        self.loyce_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;">LOYCE.CLUB (Bitcoin Data)</span>')
        self.loyce_mode_button.setStyleSheet("font-size: 16px;")
        self.loyce_mode_button.setIconSize(icon_size)
        self.loyce_mode_button.setIcon(iconloyce)
        self.loyce_mode_button.clicked.connect(self.loyce_check)
        self.loyce_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        git_label = QLabel("GitHub Links")
        self.alberto_mode_button = QPushButton(self)
        self.alberto_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;">GitHub Alertobsd Keyhunt About</span>')
        self.alberto_mode_button.setStyleSheet("font-size: 16px;")
        self.alberto_mode_button.setIconSize(icon_size)
        self.alberto_mode_button.setIcon(iconblack)
        self.alberto_mode_button.clicked.connect(self.alberto_git)
        self.alberto_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        self.XopMC_mode_button = QPushButton(self)
        self.XopMC_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;">GitHub Михаил Х. XopMC C#-Mnemonic About</span>')
        self.XopMC_mode_button.setStyleSheet("font-size: 16px;")
        self.XopMC_mode_button.setIconSize(icon_size)
        self.XopMC_mode_button.setIcon(iconred)
        self.XopMC_mode_button.clicked.connect(self.XopMC_git)
        self.XopMC_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        self.bitcrack_mode_button = QPushButton(self)
        self.bitcrack_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;">GitHub brichard19 BitCrack About</span>')
        self.bitcrack_mode_button.setStyleSheet("font-size: 16px;")
        self.bitcrack_mode_button.setIconSize(icon_size)
        self.bitcrack_mode_button.setIcon(iconblack)
        self.bitcrack_mode_button.clicked.connect(self.bitcrack_git)
        self.bitcrack_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        self.vanbit_mode_button = QPushButton(self)
        self.vanbit_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;">GitHub WanderingPhilosopher VanBitCracken Random About</span>')
        self.vanbit_mode_button.setStyleSheet("font-size: 16px;")
        self.vanbit_mode_button.setIconSize(icon_size)
        self.vanbit_mode_button.setIcon(iconred)
        self.vanbit_mode_button.clicked.connect(self.vanbit_git)
        self.vanbit_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        self.iceland_mode_button = QPushButton(self)
        self.iceland_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;">GitHub Iceland iceland2k14 Python Secp256k1 About</span>')
        self.iceland_mode_button.setStyleSheet("font-size: 16px;")
        self.iceland_mode_button.setIconSize(icon_size)
        self.iceland_mode_button.setIcon(iconblack)
        self.iceland_mode_button.clicked.connect(self.iceland_git)
        self.iceland_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        self.miz_git_mode_button = QPushButton(self)
        self.miz_git_mode_button.setToolTip('<span style="font-size: 12px; font-weight: bold; color: black;">GitHub Mizogg About</span>')
        self.miz_git_mode_button.setStyleSheet("font-size: 16px;")
        self.miz_git_mode_button.setIconSize(icon_size)
        self.miz_git_mode_button.setIcon(iconred)
        self.miz_git_mode_button.clicked.connect(self.miz_git)
        self.miz_git_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))

        self.dark_mode = self.get_theme_preference() == "dark"
        self.load_dark_mode() if self.dark_mode else self.load_light_mode()
        self.toggle_theme()

        dark_mode_layout = QHBoxLayout()
        dark_mode_layout.addWidget(favs_label)
        dark_mode_layout.addWidget(self.blockchain_mode_button)
        dark_mode_layout.addWidget(self.mizogg_mode_button)
        dark_mode_layout.addWidget(self.loyce_mode_button)
        dark_mode_layout.addStretch()

        dark_mode_layout.addWidget(git_label)
        dark_mode_layout.addWidget(self.alberto_mode_button)
        dark_mode_layout.addWidget(self.XopMC_mode_button)
        dark_mode_layout.addWidget(self.bitcrack_mode_button)
        dark_mode_layout.addWidget(self.vanbit_mode_button)
        dark_mode_layout.addWidget(self.iceland_mode_button)
        dark_mode_layout.addWidget(self.miz_git_mode_button)

        dark_mode_layout.addStretch()
        dark_mode_layout.addWidget(dark_label)
        dark_mode_layout.addWidget(self.grid_mode_button)
        dark_mode_layout.addWidget(self.wallet_mode_button)
        dark_mode_layout.addWidget(self.tetris_mode_button)
        dark_mode_layout.addWidget(self.div_mode_button)
        dark_mode_layout.addWidget(self.cov_mode_button)
        dark_mode_layout.addWidget(self.bal_mode_button)
        dark_mode_layout.addWidget(self.dark_mode_button)

        labels_info = [
            {"text": f"Made by Team Mizogg", "object_name": "madeby"},
            {"text": f"Version {version}", "object_name": "version"},
            {"text": "© mizogg.com 2018 - 2023", "object_name": "copyright"},
            {
                "text": f"Running Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}",
                "object_name": "versionpy",
            },
        ]

        dot_labels = [QLabel("●", objectName=f"dot{i}") for i in range(1, 4)]

        credit_label = QHBoxLayout()
        credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for info in labels_info:
            label = QLabel(info["text"])
            credit_label.addWidget(label)
            if dot_labels:
                dot_label = dot_labels.pop(0)
                credit_label.addWidget(dot_label)

        main_layout.addWidget(self.tab_widget)
        
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
        vanbit_tool = vanbit_gui.VanbitFrame()
        ice_tool = ice_gui.GUIInstance()
        XopMC_tool = mnemonic_gui.MnemonicFrame()
        MIZ_tool = miz_mnemonic.GUIInstance()
        snake_frame = snake_gui.Window()
        
        self.tabmain_layout = self.main_tab()
        self.tab1_layout.addWidget(bitcrack_tool)
        self.tab2_layout.addWidget(keyhunt_tool)
        self.tab3_layout.addWidget(vanbit_tool)
        self.tab4_layout.addWidget(XopMC_tool)
        self.tab5_layout.addWidget(ice_tool)
        self.tab6_layout.addWidget(MIZ_tool)
        self.tab7_layout.addWidget(self.webview_con)
        self.tab8_layout.addWidget(self.webview_bip39)
        self.tab9_layout.addWidget(self.webview_miz)
        self.tab10_layout.addWidget(snake_frame)
        self.tab11_layout.addWidget(self.webview_race)
        self.tab12_layout = self.picture_tab()

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
        self.setCentralWidget(self.centralWidget)

        self.layout.addLayout(main_layout)
        main_layout.addLayout(dark_mode_layout)
        self.layout.addLayout(credit_label)

    def create_tab_buttons(self):
        buttons_layout = QGridLayout()

        tabs = ["BitCrack", "KeyHunt", "Vanbitcracken", "C-Sharp-Mnemonic", "Iceland2k14 Secp256k1", "Miz Mnemonic", "Conversion Tools / BrainWallet",
                "Menmonics Tools", "Mizogg's Tools", "BTC Snake Game", "Race Game", "Art Work"]
        for i, tab_name in enumerate(tabs):
            row = i // 4
            col = i % 4

            button = QPushButton(tab_name)

            button.setStyleSheet(
                "QPushButton { font-size: 16pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 16pt; background-color: #A13316; color: white; }"
            )
            
            button.clicked.connect(self.switch_to_tab(i + 1))
            button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
            buttons_layout.addWidget(button, row, col)

        return buttons_layout

    def main_tab(self):
        pixmap = QPixmap(f"{TITLE_ICON}")
        title_label = QLabel(self)
        title_label.setPixmap(pixmap)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layoutmain = QVBoxLayout()
        labels_layout = QHBoxLayout()
        combined_text = """
        <html><center>
        <font size="16" color="#E7481F">❤️ Welcome to TeamHunter ₿itcoin & Crypto Scanner ❤️</font>
        <br><br><font size="8" color="#E7481F">
        Good Luck and Happy Hunting Mizogg<br>
        ⭐ https://mizogg.co.uk ⭐
        </font><br>
        <br>
        <br><font size="4">
        This Python application, named "Team Hunter GUI," provides a user-friendly interface for various cryptocurrency-related tools and functions.<br>
        Users can access tools for Bitcoin-related operations, including BitCrack, KeyHunt, Vanbitcracken, Iceland2k14 Secp256k1, and conversion tools.<br>
        The application supports both dark and light themes and offers a convenient way to switch between them.<br>
        It also features a 16x16 grid tool, a range division tool in hexadecimal format, and allows users to open external websites.<br>
        This application is built using PyQt6 and is designed to assist cryptocurrency enthusiasts in their endeavors.</font>
        <br><br><font size="4" color="#E7481F">
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

    def init_webviews(self):
        self.webview_con = self.setup_webview("/webfiles/conversion.html")
        self.webview_bip39 = self.setup_webview("/webfiles/bip39.html")
        self.webview_miz = self.setup_webview("http://109.205.181.6/")
        self.webview_race = self.setup_webview("/webfiles/Race/race.html")

    def setup_webview(self, url):
        webview = QWebEngineView(self)
        if url.startswith("http:") or url.startswith("https:"):
            webview.setUrl(QUrl(url))
        else:
            local_url = QUrl.fromLocalFile(url)
            webview.setUrl(QUrl(local_url))
        return webview

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
        
    def get_theme_preference(self):
        return ("theme", "dark")

    def load_16x16(self):
        self.frame_16x16 = grid_16x16.GridFrame()
        self.frame_16x16.show()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.load_dark_mode() if self.dark_mode else self.load_light_mode()
        if self.dark_mode:
            sun_icon = QIcon(QPixmap(SUN_ICON))
            self.dark_mode_button.setIcon(sun_icon)
        else:
            moon_icon = QIcon(QPixmap(MOON_ICON))
            self.dark_mode_button.setIcon(moon_icon)

    def exit_app(self):
        QApplication.quit()

    def about(self):
        about_dialog = about_gui.AboutDialog(self)
        about_dialog.show()

    def open_website(self):
        webbrowser.open("https://mizogg.co.uk")

    def open_telegram(self):
        webbrowser.open("https://t.me/TeamHunter_GUI")

    def privatekeyfinder_check(self):
        webbrowser.open("https://privatekeyfinder.io/")

    def blockchain_check(self):
        webbrowser.open("https://www.blockchain.com/")

    def loyce_check(self):
        webbrowser.open("http://addresses.loyce.club/")

    def alberto_git(self):
        webbrowser.open("https://github.com/albertobsd/keyhunt")

    def XopMC_git(self):
        webbrowser.open("https://github.com/XopMC/C-Sharp-Mnemonic")

    def bitcrack_git(self):
        webbrowser.open("https://github.com/brichard19/BitCrack")

    def vanbit_git(self):
        webbrowser.open("https://github.com/WanderingPhilosopher/VanBitCrackenRandom#vanbitcrackenrandom")

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

    def wallet_check(self):
        self.wallet_dialog = wallet_gui.WalletFrame()
        self.wallet_dialog.show()

    def tetris_play(self):
        self.tetris_dialog = Start_game.LauncherWindow()
        self.tetris_dialog.show()


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