"""
@author: Team Mizogg
"""
import os
import sys
import subprocess
import webbrowser
import platform

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

# Local imports
from game import snake_gui
from game.speaker import Speaker
from Mizmusic import MusicPlayer
from funct import (
    range_div_gui, about_gui, ice_gui, 
    bitcrack_gui, keyhunt_gui, grid_16x16, miz_mnemonic, 
    miz_poetry, conversion_gui, balance_gui, brain_gui, xpub_gui, 
    calculator, vanbit_gui, wallet_gui, settings_dialog
)
# Import create_setting separately to avoid import errors if it's missing
try:
    from funct import create_setting
except ImportError:
    # If create_setting is missing, we'll use the config manager directly
    pass

from config import *
from config.config_manager import config
from config.theme_manager import theme_manager
from config.logger import logger

# Add paths to system path
sys.path.extend(['config', 'funct', 'found', 'input', 'game', 'images'])

# Constants
current_platform = platform.system()
IMAGES_MAIN = "images/"
RED_ICON = f"{IMAGES_MAIN}/mizogg-eyes.png"
version = '1.6'

def open_website(self):
    webbrowser.open("https://mizogg.co.uk")

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Team Hunter GUI")
        self.setWindowIcon(QIcon(f"{IMAGES_MAIN}miz.ico"))
        self.move(30, 30)
        
        # Initialize logger
        logger.info(f"Starting TeamHunter v{version} on {current_platform}")
        
        # Create status bar
        self.statusBar().showMessage(f"TeamHunter v{version} ready", 3000)
        
        # Initialize UI components
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.icon_size = QSize(26, 26)
        self.images_main = IMAGES_MAIN
        
        # Create tabs
        self.tabmain = QWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tab7 = QWidget()
        self.tab8 = QWidget()
        self.tab9 = QWidget()
        self.tab10 = QWidget()
        self.tab12 = QWidget()

        self.tab_widget.addTab(self.tabmain, "Welcome")
        self.tab_widget.addTab(self.tab1, "BitCrack")
        self.tab_widget.addTab(self.tab2, "VanBit")
        self.tab_widget.addTab(self.tab3, "KeyHunt")
        self.tab_widget.addTab(self.tab5, "Iceland2k14 Secp256k1")
        self.tab_widget.addTab(self.tab6, "Miz Mnemonic")
        self.tab_widget.addTab(self.tab7, "Brain Hunter")
        self.tab_widget.addTab(self.tab8, "Miz Poetry")
        self.tab_widget.addTab(self.tab9, "XPUB")
        self.tab_widget.addTab(self.tab10, "CAL")
        self.tab_widget.addTab(self.tab12, "BTC Snake Game")
        
        # Set the current tab based on saved settings
        last_tab = config.get("last_tab", 0)
        self.tab_widget.setCurrentIndex(last_tab)
        
        # Connect tab changed signal
        self.tab_widget.currentChanged.connect(self.tab_changed)
        
        self.process = None
        self.scanning = False
        self.initUI()
        
        # Apply theme
        self.apply_theme()

    def tab_changed(self, index):
        """Handle tab changed event"""
        config.set("last_tab", index)
        logger.debug(f"Switched to tab {index}")

    def apply_theme(self):
        """Apply the current theme to the application"""
        # Get the current theme from settings
        theme_name = config.get("theme", "dark")
        theme_manager.set_theme(theme_name)
        
        # Apply the theme stylesheet
        stylesheet = theme_manager.get_stylesheet()
        self.setStyleSheet(stylesheet)
        
        logger.debug(f"Applied theme: {theme_name}")

    def initUI(self):
        # Play sound if enabled
        if config.get("sound_enabled", True):
            Speaker.play_death()
        
        # Create menu bar
        menubar = self.menuBar()
        
        def add_menu_action(menu, text, function):
            action = QAction(text, self)
            action.triggered.connect(function)
            menu.addAction(action)

        # File menu
        file_menu = menubar.addMenu("File")
        add_menu_action(file_menu, "New Window", self.new_window)
        file_menu.addSeparator()
        add_menu_action(file_menu, "Settings", self.open_settings)
        file_menu.addSeparator()
        add_menu_action(file_menu, "Quit", self.exit_app)

        # Help menu
        help_menu = menubar.addMenu("Help")
        add_menu_action(help_menu, "Help Telegram Group", self.open_telegram)
        add_menu_action(help_menu, "About", self.about)
        
        # Timer
        self.timer = QTimer(self)

        # Main layout
        self.main_layout = QVBoxLayout()

        # GitHub links section
        git_label = QLabel("GitHub Links")

        self.alberto_mode_button = self.create_button("GitHub Alertobsd Keyhunt About", "python-snake-black.png", self.alberto_git)
        self.bitcrack_mode_button = self.create_button("GitHub brichard19 BitCrack About", "python-snake-red.png", self.bitcrack_git)
        self.iceland_mode_button = self.create_button("GitHub Iceland iceland2k14 Python Secp256k1 About", "python-snake-black.png", self.iceland_git)
        self.miz_git_mode_button = self.create_button("GitHub Mizogg About", "python-snake-red.png", self.miz_git)

        # Extra tools section
        dark_label = QLabel("EXTRA TOOLS (16x16 Grid, Range Division, Conversion, Balance, Wallet)")

        self.grid_mode_button = self.create_button("Run 16x16 Grid Hunter", "grid.png", self.load_16x16)
        self.div_mode_button = self.create_button("Range Division in HEX", "Range.png", self.range_check)
        self.cov_mode_button = self.create_button("Conversion Tools", "Conversion.png", self.conv_check)
        self.bal_mode_button = self.create_button("Balance Check BTC", "Balance.png", self.balcheck)
        
        self.wallet_mode_button = self.create_button("Wallet Check", "walletpic.png", self.wallet_check)

        # Layout for buttons
        dark_mode_layout = QHBoxLayout()
        dark_mode_layout.addWidget(git_label)
        dark_mode_layout.addWidget(self.alberto_mode_button)
        dark_mode_layout.addWidget(self.bitcrack_mode_button)
        dark_mode_layout.addWidget(self.iceland_mode_button)
        dark_mode_layout.addWidget(self.miz_git_mode_button)

        dark_mode_layout.addStretch()
        dark_mode_layout.addWidget(dark_label)
        dark_mode_layout.addWidget(self.grid_mode_button)
        dark_mode_layout.addWidget(self.div_mode_button)
        dark_mode_layout.addWidget(self.cov_mode_button)
        dark_mode_layout.addWidget(self.bal_mode_button)
        dark_mode_layout.addWidget(self.wallet_mode_button)

        self.main_layout.addLayout(dark_mode_layout)

        # Footer information
        labels_info = [
            {"text": f"Made by Team Mizogg", "object_name": "madeby"},
            {"text": f"Full Version {version} ({current_platform})", "object_name": f"{current_platform}_version"},
            {"text": "© mizogg.com 2018 - 2025", "object_name": "copyright"},
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
        
        # Initialize tab layouts
        self.tabmain_layout = QVBoxLayout()
        self.tab1_layout = QVBoxLayout()
        self.tab2_layout = QVBoxLayout()
        self.tab3_layout = QVBoxLayout()
        self.tab5_layout = QVBoxLayout()
        self.tab6_layout = QVBoxLayout()
        self.tab7_layout = QVBoxLayout()
        self.tab8_layout = QVBoxLayout()
        self.tab9_layout = QVBoxLayout()
        self.tab10_layout = QVBoxLayout()
        self.tab12_layout = QVBoxLayout()

        # Set up central widget
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)
        
        # Create tool instances
        bitcrack_tool = bitcrack_gui.BitcrackFrame()
        keyhunt_tool = keyhunt_gui.KeyHuntFrame()
        ice_tool = ice_gui.GUIInstance()
        MIZ_tool = miz_mnemonic.GUIInstance()
        MIZP_tool = miz_poetry.GUIInstance()
        BRAIN_tool = brain_gui.GUIInstance()
        XPUB_tool = xpub_gui.GUIInstance()
        VAN_tool = vanbit_gui.VanbitFrame()
        snake_frame = snake_gui.Window()
        cal_frame = calculator.MyMainWindow()
        
        # Initialize tool settings
        self.initialize_tool_settings(bitcrack_tool, keyhunt_tool, VAN_tool, ice_tool)
        
        # Set up tab layouts
        self.tabmain_layout = self.main_tab()
        self.tab1_layout.addWidget(bitcrack_tool)
        self.tab2_layout.addWidget(VAN_tool)
        self.tab3_layout.addWidget(keyhunt_tool)
        self.tab5_layout.addWidget(ice_tool)
        self.tab6_layout.addWidget(MIZ_tool)
        self.tab7_layout.addWidget(BRAIN_tool)
        self.tab8_layout.addWidget(MIZP_tool)
        self.tab9_layout.addWidget(XPUB_tool)
        self.tab10_layout.addWidget(cal_frame)
        self.tab12_layout.addWidget(snake_frame)

        # Apply layouts to tabs
        self.tabmain.setLayout(self.tabmain_layout)
        self.tab1.setLayout(self.tab1_layout)
        self.tab2.setLayout(self.tab2_layout)
        self.tab3.setLayout(self.tab3_layout)
        self.tab5.setLayout(self.tab5_layout)
        self.tab6.setLayout(self.tab6_layout)
        self.tab7.setLayout(self.tab7_layout)
        self.tab8.setLayout(self.tab8_layout)
        self.tab9.setLayout(self.tab9_layout)
        self.tab10.setLayout(self.tab10_layout)
        self.tab12.setLayout(self.tab12_layout)

        # Add layouts to main layout
        self.layout.addLayout(self.main_layout)
        
        # Add music player
        mizogg_player = MusicPlayer()
        
        # Set music player volume from settings
        mizogg_player.set_volume(config.get("music_volume", 50))
        
        # Enable/disable music based on settings
        if not config.get("music_enabled", True):
            mizogg_player.stop_music()
            
        self.main_layout.addWidget(mizogg_player)
        self.layout.addLayout(credit_label)
        
        # Log UI initialization
        logger.info("UI initialized successfully")

    def create_button(self, tooltip, icon_name, callback, hover_sound=None, is_checkbox=False):
        button = QPushButton(self)
        button.setToolTip(f'<span style="font-size: 10pt; font-weight: bold; color: black;">{tooltip}</span>')
        button.setStyleSheet("font-size: 12pt;")
        button.setIconSize(self.icon_size)
        icon = QIcon(QPixmap(f"{self.images_main}{icon_name}"))
        button.setIcon(icon)
        button.clicked.connect(callback)
        
        if hover_sound and config.get("sound_enabled", True):
            button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(hover_sound))
        else:
            button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus)) if config.get("sound_enabled", True) else None
        
        return button

    def open_settings(self):
        """Open the settings dialog"""
        settings = settings_dialog.SettingsDialog(self)
        settings.settings_changed.connect(self.apply_settings_changes)
        settings.exec()
        
        logger.debug("Settings dialog closed")
        
    def apply_settings_changes(self):
        """Apply settings changes to all components"""
        # Apply theme changes
        self.apply_theme()
        
        # Reload tool settings for each tab
        try:
            # BitCrack tab (tab1)
            if hasattr(self, 'tab1') and hasattr(self.tab1, 'layout'):
                for i in range(self.tab1.layout().count()):
                    widget = self.tab1.layout().itemAt(i).widget()
                    if isinstance(widget, bitcrack_gui.BitcrackFrame):
                        # Reload BitCrack settings
                        blocks = config.get("bitcrack_settings.blocks", 32)
                        threads = config.get("bitcrack_settings.threads", 256)
                        points = config.get("bitcrack_settings.points", 256)
                        device = config.get("bitcrack_settings.device", "0")
                        
                        # Update UI elements
                        for i in range(widget.blocksSize_choice.count()):
                            if widget.blocksSize_choice.itemText(i) == str(blocks):
                                widget.blocksSize_choice.setCurrentIndex(i)
                                break
                                
                        for i in range(widget.threadComboBox_n.count()):
                            if widget.threadComboBox_n.itemText(i) == str(threads):
                                widget.threadComboBox_n.setCurrentIndex(i)
                                break
                                
                        for i in range(widget.pointsSize_choice.count()):
                            if widget.pointsSize_choice.itemText(i) == str(points):
                                widget.pointsSize_choice.setCurrentIndex(i)
                                break
                                
                        widget.gpuIdLineEdit.setText(device)
                        
                        # Save the settings to ensure they're persisted
                        widget.save_bitcrack_settings()
            
            # KeyHunt tab (tab3)
            if hasattr(self, 'tab3') and hasattr(self.tab3, 'layout'):
                for i in range(self.tab3.layout().count()):
                    widget = self.tab3.layout().itemAt(i).widget()
                    if isinstance(widget, keyhunt_gui.KeyHuntFrame):
                        # Reload KeyHunt settings
                        threads = config.get("keyhunt_settings.threads", 1)
                        mode = config.get("keyhunt_settings.mode", "address")
                        ram = config.get("keyhunt_settings.ram", 512)
                        
                        # Update UI elements
                        thread_index = min(threads - 1, widget.cpu_count - 1)
                        widget.threadComboBox_key.setCurrentIndex(thread_index)
                        
                        for i in range(widget.modeComboBox.count()):
                            if widget.modeComboBox.itemText(i) == mode:
                                widget.modeComboBox.setCurrentIndex(i)
                                break
                                
                        for i, k_value in enumerate(['1', '4', '8', '16', '24', '32', '64', '128', '256', '512', '756', '1024', '2048']):
                            if int(k_value) == ram:
                                widget.kComboBox.setCurrentIndex(i)
                                break
            
            # VanBit settings
            if hasattr(self, 'tab2') and hasattr(self.tab2, 'layout'):
                for i in range(self.tab2.layout().count()):
                    widget = self.tab2.layout().itemAt(i).widget()
                    if hasattr(widget, 'threadComboBox') and hasattr(widget, 'gridSize_choice'):
                        # Reload VanBit settings
                        threads = config.get("vanbit_settings.threads", 4)
                        grid = config.get("vanbit_settings.grid", 32)
                        
                        # Update UI elements
                        for i in range(widget.threadComboBox.count()):
                            if int(widget.threadComboBox.itemText(i)) == threads:
                                widget.threadComboBox.setCurrentIndex(i)
                                break
                        
                        for i in range(widget.gridSize_choice.count()):
                            if widget.gridSize_choice.itemText(i) == str(grid):
                                widget.gridSize_choice.setCurrentIndex(i)
                                break
            
            # Ice settings
            if hasattr(self, 'tab5') and hasattr(self.tab5, 'layout'):
                for i in range(self.tab5.layout().count()):
                    widget = self.tab5.layout().itemAt(i).widget()
                    if hasattr(widget, 'coresComboBox') and hasattr(widget, 'keyspaceLineEdit'):
                        # Reload Ice settings
                        # No specific settings for ice_tool yet
                        pass
            
        except Exception as e:
            logger.error(f"Error applying settings changes: {e}")
            import traceback
            logger.error(traceback.format_exc())

    def create_tab_buttons(self):
        buttons_layout = QGridLayout()

        tabs = ["BitCrack", "VanBitCracken", "KeyHunt", "Iceland2k14 Secp256k1", "Miz Mnemonic", "Brain Hunter", "Miz Poetry", "XPUB Tool", "CAL", "BTC Snake Game", "16x16 Grid"]
        
        for i, tab_name in enumerate(tabs):
            row = i // 4
            col = i % 4

            button = QPushButton(tab_name)

            if tab_name == "16x16 Grid":
                button.clicked.connect(self.load_16x16)
            else:
                button.clicked.connect(self.switch_to_tab(i + 1))

            button.setStyleSheet(
                "QPushButton { font-size: 12pt; }"
                "QPushButton:hover { font-size: 12pt; }"
            )

            button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus)) if config.get("sound_enabled", True) else None
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
        <font size="13">❤️ Welcome to TeamHunter ₿itcoin & Crypto Scanner ❤️</font>

        <br><font size="4">
        This Python application, named "Team Hunter GUI," provides a user-friendly interface for various cryptocurrency-related tools and functions.<br>
        Users can access tools for Bitcoin-related operations, including BitCrack, VanBitCraken, KeyHunt, Iceland2k14 Secp256k1....<br>
        It also features a 16x16 grid tool, a range division tool in hexadecimal format, and allows users to open external websites.<br>
        This application is built using PyQt6 and is designed to assist cryptocurrency enthusiasts in their endeavors.</font>
        <br><br><font size="5">
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
        logger.info("Started new TeamHunter window")

    def initialize_tool_settings(self, bitcrack_tool, keyhunt_tool, vanbit_tool, ice_tool):
        """Initialize tool settings from config"""
        try:
            # BitCrack settings
            if bitcrack_tool:
                # Get settings from config
                blocks = config.get("bitcrack_settings.blocks", 32)
                threads = config.get("bitcrack_settings.threads", 256)
                points = config.get("bitcrack_settings.points", 256)
                device = config.get("bitcrack_settings.device", "0")
                
                # Update UI elements
                for i in range(bitcrack_tool.blocksSize_choice.count()):
                    if bitcrack_tool.blocksSize_choice.itemText(i) == str(blocks):
                        bitcrack_tool.blocksSize_choice.setCurrentIndex(i)
                        break
                        
                for i in range(bitcrack_tool.threadComboBox_n.count()):
                    if bitcrack_tool.threadComboBox_n.itemText(i) == str(threads):
                        bitcrack_tool.threadComboBox_n.setCurrentIndex(i)
                        break
                        
                for i in range(bitcrack_tool.pointsSize_choice.count()):
                    if bitcrack_tool.pointsSize_choice.itemText(i) == str(points):
                        bitcrack_tool.pointsSize_choice.setCurrentIndex(i)
                        break
                        
                bitcrack_tool.gpuIdLineEdit.setText(device)
            
            # KeyHunt settings
            if keyhunt_tool:
                # Get settings from config
                threads = config.get("keyhunt_settings.threads", 1)
                mode = config.get("keyhunt_settings.mode", "address")
                ram = config.get("keyhunt_settings.ram", 512)
                
                # Update UI elements
                thread_index = min(threads - 1, keyhunt_tool.cpu_count - 1)
                keyhunt_tool.threadComboBox_key.setCurrentIndex(thread_index)
                
                for i in range(keyhunt_tool.modeComboBox.count()):
                    if keyhunt_tool.modeComboBox.itemText(i) == mode:
                        keyhunt_tool.modeComboBox.setCurrentIndex(i)
                        break
                        
                for i, k_value in enumerate(['1', '4', '8', '16', '24', '32', '64', '128', '256', '512', '756', '1024', '2048']):
                    if int(k_value) == ram:
                        keyhunt_tool.kComboBox.setCurrentIndex(i)
                        break
            
            # VanBit settings
            if vanbit_tool:
                # Get settings from config
                threads = config.get("vanbit_settings.threads", 4)
                grid = config.get("vanbit_settings.grid", 32)
                
                # Update UI elements if they exist
                if hasattr(vanbit_tool, 'threadComboBox'):
                    for i in range(vanbit_tool.threadComboBox.count()):
                        if int(vanbit_tool.threadComboBox.itemText(i)) == threads:
                            vanbit_tool.threadComboBox.setCurrentIndex(i)
                            break
                
                if hasattr(vanbit_tool, 'gridSize_choice'):
                    for i in range(vanbit_tool.gridSize_choice.count()):
                        if vanbit_tool.gridSize_choice.itemText(i) == str(grid):
                            vanbit_tool.gridSize_choice.setCurrentIndex(i)
                            break
            
            # Ice settings
            if ice_tool:
                # Get settings from config
                # No specific settings for ice_tool yet
                pass
            
        except Exception as e:
            logger.error(f"Error initializing tool settings: {e}")

if __name__ == "__main__":
    # Initialize configuration
    config.initialize()
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Create application
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    
    # Apply theme from configuration
    theme_name = config.get("theme", "dark")
    theme_manager.set_theme(theme_name)
    stylesheet = theme_manager.get_stylesheet()
    app.setStyleSheet(stylesheet)
    
    # Show window
    window.show()
    
    # Log application start
    logger.info(f"TeamHunter v{version} started successfully")
    
    # Run application
    sys.exit(app.exec())