"""
@author: Team Mizogg
"""
import os
import subprocess
import webbrowser
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import qdarktheme
from libs import set_settings, create_setting
from game import snake_gui, Start_game
from funct import (range_div_gui, about_gui, ice_gui, bitcrack_gui, keyhunt_gui, vanbit_gui, up_bloom_gui, grid_16x16, mnemonic_gui, miz_mnemonic, conversion_gui, balance_gui)
import sys
from Mizmusic import MusicPlayer
sys.path.extend(['libs', 'config', 'funct', 'found', 'input', 'game', 'images'])
from speaker import Speaker
from config import *
import platform
import subprocess

IMAGES_MAIN = "images/main/"
image_folder = "images"
image_files = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

version = '0.8'

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dark_mode_button = None
        self.setWindowTitle("Team Hunter GUI")
        self.setWindowIcon(QIcon(f"{IMAGES_MAIN}miz.ico"))
        self.setGeometry(50, 50, 1200, 800)
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

        self.tab_widget.addTab(self.tabmain, "Welcome")
        self.tab_widget.addTab(self.tab1, "BitCrack")
        self.tab_widget.addTab(self.tab2, "KeyHunt")
        self.tab_widget.addTab(self.tab3, "Vanbitcracken")
        self.tab_widget.addTab(self.tab4, "C-Sharp-Mnemonic")
        self.tab_widget.addTab(self.tab5, "Iceland2k14 Secp256k1")
        self.tab_widget.addTab(self.tab6, "Miz Mnemonic")
        self.tab_widget.addTab(self.tab7, "BTC Snake Game")
        self.tab_widget.addTab(self.tab8, "Art Work")
        self.process = None
        self.scanning = False
        self.initUI()
        self.theme_preference = self.get_theme_preference()
        self.dark_mode = self.theme_preference == "dark"
        self.load_dark_mode() if self.dark_mode else self.load_light_mode()
        self.toggle_theme()

    def load_dark_mode(self):
        qdarktheme.setup_theme("dark")

    def load_light_mode(self):
        qdarktheme.setup_theme("light")

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
        self.XopMC_mode_button = self.create_button("GitHub Михаил Х. XopMC C#-Mnemonic About", "python-snake-red.png", self.XopMC_git)
        self.bitcrack_mode_button = self.create_button("GitHub brichard19 BitCrack About", "python-snake-black.png", self.bitcrack_git)
        self.vanbit_mode_button = self.create_button("GitHub WanderingPhilosopher VanBitCracken Random About", "python-snake-red.png", self.vanbit_git)
        self.iceland_mode_button = self.create_button("GitHub Iceland iceland2k14 Python Secp256k1 About", "python-snake-black.png", self.iceland_git)
        self.miz_git_mode_button = self.create_button("GitHub Mizogg About", "python-snake-red.png", self.miz_git)

        dark_label = QLabel("EXTRA TOOLS (16x16 Grid, Tetris, Range Division, Conversion, Balance, Dark/Light, Mute/UnMute)")

        self.grid_mode_button = self.create_button("Run 16x16 Grid Hunter", "grid.png", self.load_16x16)
        self.tetris_mode_button = self.create_button("Play The GAME Tetris Bitcoin Finder", "Tetris.png", self.tetris_play, hover_sound=Speaker.row_deleted)
        self.div_mode_button = self.create_button("Range Division in HEX", "Range.png", self.range_check)
        self.cov_mode_button = self.create_button("Conversion Tools", "Conversion.png", self.conv_check)
        self.bal_mode_button = self.create_button("Balance Check BTC", "walletpic.png", self.balcheck)
        self.dark_mode_button = self.create_button("Switch Between Dark and Light Theme", "sun.png", self.toggle_theme, is_checkbox=True)
        self.mute_mode_button = self.create_button("Mute sound effects", "mute.png", self.mute_sound, is_checkbox=True)


        dark_mode_layout = QHBoxLayout()
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
        dark_mode_layout.addWidget(self.tetris_mode_button)
        dark_mode_layout.addWidget(self.div_mode_button)
        dark_mode_layout.addWidget(self.cov_mode_button)
        dark_mode_layout.addWidget(self.bal_mode_button)
        dark_mode_layout.addWidget(self.dark_mode_button)
        dark_mode_layout.addWidget(self.mute_mode_button)

        self.main_layout.addLayout(dark_mode_layout)

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
        self.tab7_layout.addWidget(snake_frame)
        self.tab8_layout = self.picture_tab()

        self.tabmain.setLayout(self.tabmain_layout)
        self.tab1.setLayout(self.tab1_layout)
        self.tab2.setLayout(self.tab2_layout)
        self.tab3.setLayout(self.tab3_layout)
        self.tab4.setLayout(self.tab4_layout)
        self.tab5.setLayout(self.tab5_layout)
        self.tab6.setLayout(self.tab6_layout)
        self.tab7.setLayout(self.tab7_layout)
        self.tab8.setLayout(self.tab8_layout)

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
        
        if is_checkbox:
            button.setChecked(True if self.get_theme_preference() == "dark" else False)
        
        return button


    def create_tab_buttons(self):
        buttons_layout = QGridLayout()

        tabs = ["BitCrack", "KeyHunt", "Vanbitcracken", "C-Sharp-Mnemonic", "Iceland2k14 Secp256k1", "Miz Mnemonic", "BTC Snake Game", "Art Work"]
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
        pixmap = QPixmap(f"{IMAGES_MAIN}titlebig.png")
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
        Users can access tools for Bitcoin-related operations, including BitCrack, KeyHunt, Vanbitcracken, Iceland2k14 Secp256k1....<br>
        The application supports both dark and light themes and offers a convenient way to switch between them.<br>
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
        
    def get_theme_preference(self):
        return ("theme", "dark")

    def load_16x16(self):
        self.frame_16x16 = grid_16x16.GridFrame()
        self.frame_16x16.show()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.load_dark_mode() if self.dark_mode else self.load_light_mode()

        try:
            if self.dark_mode:
                sun_icon = QIcon(QPixmap(f"{IMAGES_MAIN}sun.png"))
                self.dark_mode_button.setIcon(sun_icon)
            else:
                moon_icon = QIcon(QPixmap(f"{IMAGES_MAIN}moon.png"))
                self.dark_mode_button.setIcon(moon_icon)
        except Exception as e:
            print(f"Error loading theme icon: {e}")


    def exit_app(self):
        QApplication.quit()

    def about(self):
        about_dialog = about_gui.AboutDialog(self)
        about_dialog.show()

    def open_telegram(self):
        webbrowser.open("https://t.me/TeamHunter_GUI")

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

    def tetris_play(self):
        self.tetris_dialog = Start_game.LauncherWindow()
        self.tetris_dialog.show()

    def mute_sound(self):
        Speaker.toggle_mute()
        if Speaker.muted:
            self.mute_mode_button.setIcon(QIcon(QPixmap(f"{self.images_main}sound.png")))
        else:
            self.mute_mode_button.setIcon(QIcon(QPixmap(f"{self.images_main}mute.png")))

    def closeEvent(self, event):
        if self.process and hasattr(self.process, 'pid') and self.process.pid:
            if platform.system() == "Windows":
                subprocess.Popen(["taskkill", "/F", "/T", "/PID", str(self.process.pid)])
            else:
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
        event.accept()

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