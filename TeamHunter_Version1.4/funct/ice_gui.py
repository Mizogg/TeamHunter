"""

@author: Team Mizogg
"""
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import os
import random
import datetime
import time
import locale
import requests
import json
from funct.iceland import secp256k1 as ice
from funct import (win_gui, telegram_gui, discord_gui, utils, load_file)
from funct import load_file
from game.speaker import Speaker
from config.config import *
from bloomfilter import BloomFilter

addfind = load_file.load_addresses()
TEL_ICON = "images/main/Telegram.png"
DIS_ICON = "images/main/Discord.png"
WINNER_FOUND = "found/found.txt"
CONFIG_FILE = "config/config.json"

crypto_mapping = {
    "Bitcoin (BTC)": 0,
    "Bitcoin SV (BSV)": 1,
    "Bitcoin Diamond (BTCD)": 2,
    "Argentum (ARG)": 3,
    "Axe (AXE)": 4,
    "BitcoinCore (BC)": 5,
    "Bitcoin Cash (BCH)": 6,
    "BitcoinStash (BSD)": 7,
    "Bitcore (BTDX)": 8,
    "Bitcoin Gold (BTG)": 9,
    "Bitcore (BTX)": 10,
    "Chaucha (CHA)": 11,
    "Dash (DASH)": 12,
    #"Decred (DCR)": 13,
    "Defcoin (DFC)": 14,
    "DigiByte (DGB)": 15,
    "Dogecoin (DOGE)": 16,
    "Faircoin (FAI)": 17,
    "Feathercoin (FTC)": 18,
    "Groestlcoin (GRS)": 19,
    "Jumbucks (JBS)": 20,
    "Litecoin (LTC)": 21,
    "Megacoin (MEC)": 22,
    "Monacoin (MONA)": 23,
    "Mazacoin (MZC)": 24,
    "PIVX (PIVX)": 25,
    "Polis (POLIS)": 26,
    "Riecoin (RIC)": 27,
    "Stratis (STRAT)": 28,
    "SmartCash (SMART)": 29,
    "Viacoin (VIA)": 30,
    "Myriad (XMY)": 31,
    #"Zcash (ZEC)": 32,
    "Zclassic (ZCL)": 33,
    "Zero (ZERO)": 34,
    "Horizen (ZEN)": 35,
    "TENT (TENT)": 36,
    "Zeitcoin (ZEIT)": 37,
    "Vertcoin (VTC)": 38,
    "Unobtanium (UNO)": 39,
    "Skeincoin (SKC)": 40,
    "Ravencoin (RVN)": 41,
    "Peercoin (PPC)": 42,
    "Ormeus Coin (OMC)": 43,
    "OKCash (OK)": 44,
    "Namecoin (NMC)": 45,
    "Gulden (NLG)": 46,
    "LBRY Credits (LBC)": 47,
    "Denarius (DNR)": 48,
    "Bulwark (BWK)": 49,
}


class GUIInstance(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.add_count_label = QLabel(self.count_addresses(), objectName="count_addlabel", alignment=Qt.AlignmentFlag.AlignLeft)

        power_label = QLabel("Amount Of Addresses Per Page to Show", self)
        power_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #E7481F;")

        self.format_combo_box_POWER = QComboBox(self)
        self.format_combo_box_POWER.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Amount it Address to Check per scan. Ajust for best speed have to stop to change amount </span>')
        self.format_combo_box_POWER.addItems(
            ["1", "128", "256", "512", "1024", "2048", "4096", "8192", "16384"]
        )
        self.format_combo_box_POWER.setCurrentIndex(2)
        crypto_label = QLabel("Type of Crypto ", self)
        crypto_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #E7481F;")
        self.crypto_selector = QComboBox()
        self.crypto_selector.addItem("Bitcoin (BTC)")
        self.crypto_selector.addItem("Bitcoin SV (BSV)")
        self.crypto_selector.addItem("Bitcoin Diamond (BTCD)")
        self.crypto_selector.addItem("Argentum (ARG)")
        self.crypto_selector.addItem("Axe (AXE)")
        self.crypto_selector.addItem("BitcoinCore (BC)")
        self.crypto_selector.addItem("Bitcoin Cash (BCH)")
        self.crypto_selector.addItem("BitcoinStash (BSD)")
        self.crypto_selector.addItem("Bitcore (BTDX)")
        self.crypto_selector.addItem("Bitcoin Gold (BTG)")
        self.crypto_selector.addItem("Bitcore (BTX)")
        self.crypto_selector.addItem("Chaucha (CHA)")
        self.crypto_selector.addItem("Dash (DASH)")
        #self.crypto_selector.addItem("Decred (DCR)")
        self.crypto_selector.addItem("Defcoin (DFC)")
        self.crypto_selector.addItem("DigiByte (DGB)")
        self.crypto_selector.addItem("Dogecoin (DOGE)")
        self.crypto_selector.addItem("Faircoin (FAI)")
        self.crypto_selector.addItem("Feathercoin (FTC)")
        self.crypto_selector.addItem("Groestlcoin (GRS)")
        self.crypto_selector.addItem("Jumbucks (JBS)")
        self.crypto_selector.addItem("Litecoin (LTC)")
        self.crypto_selector.addItem("Megacoin (MEC)")
        self.crypto_selector.addItem("Monacoin (MONA)")
        self.crypto_selector.addItem("Mazacoin (MZC)")
        self.crypto_selector.addItem("PIVX (PIVX)")
        self.crypto_selector.addItem("Polis (POLIS)")
        self.crypto_selector.addItem("Riecoin (RIC)")
        self.crypto_selector.addItem("Stratis (STRAT)")
        self.crypto_selector.addItem("SmartCash (SMART)")
        self.crypto_selector.addItem("Viacoin (VIA)")
        self.crypto_selector.addItem("Myriad (XMY)")
        #self.crypto_selector.addItem("Zcash (ZEC)")
        #self.crypto_selector.addItem("Zclassic (ZCL)")
        #self.crypto_selector.addItem("Zero (ZERO)")
        #self.crypto_selector.addItem("Horizen (ZEN)")
        #self.crypto_selector.addItem("TENT (TENT)")
        self.crypto_selector.addItem("Zeitcoin (ZEIT)")
        self.crypto_selector.addItem("Vertcoin (VTC)")
        self.crypto_selector.addItem("Unobtanium (UNO)")
        self.crypto_selector.addItem("Skeincoin (SKC)")
        self.crypto_selector.addItem("Ravencoin (RVN)")
        self.crypto_selector.addItem("Peercoin (PPC)")
        self.crypto_selector.addItem("Ormeus Coin (OMC)")
        self.crypto_selector.addItem("OKCash (OK)")
        self.crypto_selector.addItem("Namecoin (NMC)")
        self.crypto_selector.addItem("Gulden (NLG)")
        self.crypto_selector.addItem("LBRY Credits (LBC)")
        self.crypto_selector.addItem("Denarius (DNR)")
        self.crypto_selector.addItem("Bulwark (BWK)")


        select_power_layout = QHBoxLayout()
        select_power_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        select_power_layout.addWidget(power_label)
        select_power_layout.addWidget(self.format_combo_box_POWER)

        select_power_layout.addWidget(crypto_label)
        select_power_layout.addWidget(self.crypto_selector)
        self.crypto_selector.currentIndexChanged.connect(self.handle_crypto_change)

        start_button = QPushButton("Start", self)
        start_button.setStyleSheet(
                "QPushButton { font-size: 10pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 10pt; background-color: #A13316; color: white; }"
            )
        start_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start scanning (Make sure Range is set) </span>')
        start_button.clicked.connect(self.start)
        start_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        start_button.setFixedWidth(100)

        stop_button = QPushButton("Stop", self)
        stop_button.setStyleSheet(
            "QPushButton { font-size: 10pt; background-color: #1E1E1E; color: white; }"
            "QPushButton:hover { font-size: 10pt; background-color: #5D6062; color: white; }"
        )
        stop_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Stop scanning </span>')
        stop_button.clicked.connect(self.stop)
        stop_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back))
        stop_button.setFixedWidth(100)

        start_stop_layout = QHBoxLayout()
        start_stop_layout.addLayout(select_power_layout)
        start_stop_layout.addStretch(1)
        start_stop_layout.addWidget(start_button)
        start_stop_layout.addWidget(stop_button)
        start_stop_layout.addStretch(1)

        start_stop_layout.addWidget(self.add_count_label)

        options_layout2 = QHBoxLayout()

        self.keyspaceLabel = QLabel("Key Space:", self)
        options_layout2.addWidget(self.keyspaceLabel)

        self.start_edit = QLineEdit("2000000000000000")
        self.start_edit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Type the start range in HEX </span>')

        self.end_edit = QLineEdit("3FFFFFFFFFFFFFFFF")
        self.end_edit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Type the end range in HEX </span>')
        self.keyspace_slider = QSlider(Qt.Orientation.Horizontal)
        self.keyspace_slider.setMinimum(1)
        self.keyspace_slider.setMaximum(256)
        self.keyspace_slider.setValue(66)
        self.keyspace_slider.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.generic_scroll_01), 0.3)
        self.keyspace_slider.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Drag Left to Right to Adjust Range </span>')
        keyspacerange_layout = QVBoxLayout()
        keyspacerange_layout.addWidget(self.start_edit)
        keyspacerange_layout.addWidget(self.end_edit)
        keyspacerange_layout.addWidget(self.keyspace_slider)

        options_layout2.addLayout(keyspacerange_layout)


        self.keyspace_slider.valueChanged.connect(self.update_keyspace_range)
        self.bitsLabel = QLabel("Bits:", self)
        options_layout2.addWidget(self.bitsLabel)

        self.bitsLineEdit = QLineEdit(self)
        self.bitsLineEdit.setText("66")
        self.bitsLineEdit.textChanged.connect(self.updateSliderAndRanges)
        options_layout2.addWidget(self.bitsLineEdit)


        dec_label = QLabel(" Dec value :")
        self.value_edit_dec = QLineEdit()
        self.value_edit_dec.setReadOnly(True)

        hex_label = QLabel(" HEX value :")
        self.value_edit_hex = QLineEdit()
        self.value_edit_hex.setReadOnly(True)

        current_scan_layout = QHBoxLayout()
        current_scan_layout.addWidget(dec_label)
        current_scan_layout.addWidget(self.value_edit_dec)
        current_scan_layout.addWidget(hex_label)
        current_scan_layout.addWidget(self.value_edit_hex)
        button_labels = ["Random", "Sequence", "Reverse"]
        button_objects = []

        for label in button_labels:
            button = QRadioButton(label)
            button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Pick Type of scan Random Sequence/Forward or Reverse/Backwards </span>')
            button_objects.append(button)

        button_objects[0].setChecked(True)
        self.random_button = button_objects[0]
        self.sequence_button = button_objects[1]
        self.reverse_button = button_objects[2]
        checkbox_labels = ["DEC", "HEX", "Compressed", "Uncompressed", "P2SH", "Bech32", "ETH", "Stop if found"]
        checkbox_objects = []
        checkbox_width = 100
        for label in checkbox_labels:
            checkbox = QCheckBox(label)
            checkbox.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Ticks can be removed to sreach for single type or mutiple types of Bitcoin Address. Removing some will increase speed. Address not selected we not be searched </span>')
            checkbox.setFixedWidth(checkbox_width)
            checkbox_objects.append(checkbox)
        self.dec_checkbox, self.hex_checkbox, self.compressed_checkbox, self.uncompressed_checkbox, self.p2sh_checkbox, self.bech32_checkbox, self.eth_checkbox, self.win_checkbox = checkbox_objects[0:]
        checkboxes_to_check = [self.dec_checkbox, self.hex_checkbox, self.compressed_checkbox]
        for checkbox in checkboxes_to_check:
            checkbox.setChecked(True)
        self.uncompressed_checkbox.setChecked(False)
        self.p2sh_checkbox.setChecked(False)
        self.bech32_checkbox.setChecked(False)
        self.eth_checkbox.setChecked(False)
        self.win_checkbox.setChecked(False)

        # Create a vertical line as a divider
        divider = QFrame(frameShape=QFrame.Shape.VLine, frameShadow=QFrame.Shadow.Sunken)

        # Create a layout for the radio buttons and checkboxes on the same line
        radio_and_checkbox_layout = QHBoxLayout()

        widgets = [
            self.random_button, self.sequence_button, self.reverse_button,
            self.dec_checkbox, self.hex_checkbox, self.compressed_checkbox,
            self.uncompressed_checkbox, self.p2sh_checkbox, self.bech32_checkbox,
            self.eth_checkbox, self.win_checkbox
        ]

        for widget in widgets:
            radio_and_checkbox_layout.addWidget(widget)

        # Set up the main layout
        layouts = [
            start_stop_layout, 
            radio_and_checkbox_layout, options_layout2, current_scan_layout
        ]

        for l in layouts:
            layout.addLayout(l)

        def create_line_edit(read_only=True, text="0"):
            line_edit = QLineEdit()
            line_edit.setReadOnly(read_only)
            line_edit.setText(text)
            return line_edit

        self.found_keys_scanned_edit = create_line_edit()
        self.total_keys_scanned_edit = create_line_edit()
        self.keys_per_sec_edit = create_line_edit(False, "")

        labels_and_edits = [
            ("Found", self.found_keys_scanned_edit),
            ("Total keys scanned:", self.total_keys_scanned_edit),
            ("Keys per second:", self.keys_per_sec_edit)
        ]

        keys_layout = QHBoxLayout()

        for label_text, edit_widget in labels_and_edits:
            label = QLabel(label_text)
            keys_layout.addWidget(label)
            keys_layout.addWidget(edit_widget)

        layout.addLayout(keys_layout)

        progress_layout_text = QHBoxLayout()
        progress_layout_text.setObjectName("progressbar")
        progress_label = QLabel("progress %")

        self.progress_bar = utils.CustomProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)

        progress_layout_text.addWidget(progress_label)
        progress_layout_text.addWidget(self.progress_bar)

        layout.addLayout(progress_layout_text)

        self.address_layout_ = QGridLayout()
        self.priv_label = QLabel("DEC Keys: ")
        self.priv_text = QTextEdit(self)
        self.priv_text.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Decimal Key Output</span>')
        self.HEX_label = QLabel("HEX Keys: ")
        self.HEX_text = QTextEdit(self)
        self.HEX_text.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> HEX Key Output</span>')
        self.comp_label = QLabel("Compressed Address: ")
        self.comp_text = QTextEdit(self)
        self.comp_text.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Compressed Address Output</span>')
        self.uncomp_label = QLabel("Uncompressed Address: ")
        self.uncomp_text = QTextEdit(self)
        self.uncomp_text.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Uncompressed Address Output</span>')
        self.p2sh_label = QLabel("p2sh Address: ")
        self.p2sh_text = QTextEdit(self)
        self.p2sh_text.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> P2SH 3 Address Output</span>')
        self.bech32_label = QLabel("bech32 Address: ")
        self.bech32_text = QTextEdit(self)
        self.bech32_text.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> bech32 BC1 Address Output</span>')
        self.eth_label = QLabel("Eth Address: ")
        self.eth_text = QTextEdit(self)
        self.eth_text.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Eth Address Output Address Output</span>')
        self.address_layout_.addWidget(self.priv_label, 1, 0)
        self.address_layout_.addWidget(self.priv_text, 2, 0)
        self.address_layout_.addWidget(self.HEX_label, 1, 1)
        self.address_layout_.addWidget(self.HEX_text, 2, 1)
        self.address_layout_.addWidget(self.comp_label, 1, 2)
        self.address_layout_.addWidget(self.comp_text, 2, 2)
        self.address_layout_.addWidget(self.uncomp_label, 1, 3)
        self.address_layout_.addWidget(self.uncomp_text, 2, 3)
        self.address_layout_.addWidget(self.p2sh_label, 1, 4)
        self.address_layout_.addWidget(self.p2sh_text, 2, 4)
        self.address_layout_.addWidget(self.bech32_label, 1, 5)
        self.address_layout_.addWidget(self.bech32_text, 2, 5)
        self.address_layout_.addWidget(self.eth_label, 1, 6)
        self.address_layout_.addWidget(self.eth_text, 2, 6)

        layout.addLayout(self.address_layout_)

        self.dec_checkbox.stateChanged.connect(
            lambda: self.toggle_visibility(
                self.dec_checkbox, self.priv_label, self.priv_text
            )
        )
        self.hex_checkbox.stateChanged.connect(
            lambda: self.toggle_visibility(
                self.hex_checkbox, self.HEX_label, self.HEX_text
            )
        )
        self.compressed_checkbox.stateChanged.connect(
            lambda: self.toggle_visibility(
                self.compressed_checkbox, self.comp_label, self.comp_text
            )
        )
        self.uncompressed_checkbox.stateChanged.connect(
            lambda: self.toggle_visibility(
                self.uncompressed_checkbox, self.uncomp_label, self.uncomp_text
            )
        )
        self.p2sh_checkbox.stateChanged.connect(
            lambda: self.toggle_visibility(
                self.p2sh_checkbox, self.p2sh_label, self.p2sh_text
            )
        )
        self.bech32_checkbox.stateChanged.connect(
            lambda: self.toggle_visibility(
                self.bech32_checkbox, self.bech32_label, self.bech32_text
            )
        )

        self.eth_checkbox.stateChanged.connect(
            lambda: self.toggle_visibility(
                self.eth_checkbox, self.eth_label, self.eth_text
            )
        )

        self.toggle_visibility(self.dec_checkbox, self.priv_label, self.priv_text)
        self.toggle_visibility(self.hex_checkbox, self.HEX_label, self.HEX_text)
        self.toggle_visibility(
            self.compressed_checkbox, self.comp_label, self.comp_text
        )
        self.toggle_visibility(
            self.uncompressed_checkbox, self.uncomp_label, self.uncomp_text
        )
        self.toggle_visibility(self.p2sh_checkbox, self.p2sh_label, self.p2sh_text)
        self.toggle_visibility(
            self.bech32_checkbox, self.bech32_label, self.bech32_text
        )
        self.toggle_visibility(self.eth_checkbox, self.eth_label, self.eth_text)
        icon_size = QSize(26, 26)
        icontel = QIcon(QPixmap(TEL_ICON))
        icondis = QIcon(QPixmap(DIS_ICON))

        self.telegram_mode_button = QPushButton(self)
        self.telegram_mode_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Enter Custom Telegram Credentials Settings .</span>')
        self.telegram_mode_button.setStyleSheet("font-size: 10px;")
        self.telegram_mode_button.setIconSize(icon_size)
        self.telegram_mode_button.setIcon(icontel)
        self.telegram_mode_button.clicked.connect(self.open_telegram_settings)
        self.use_telegram_credentials_checkbox = QCheckBox("Use Custom Telegram Credentials")
        self.use_telegram_credentials_checkbox.setChecked(False)

        self.discord_mode_button = QPushButton(self)
        self.discord_mode_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Enter Custom Discord Credentials Settings .</span>')
        self.discord_mode_button.setStyleSheet("font-size: 10px;")
        self.discord_mode_button.setIconSize(icon_size)
        self.discord_mode_button.setIcon(icondis)
        self.discord_mode_button.clicked.connect(self.open_discord_settings)
        self.use_discord_credentials_checkbox = QCheckBox("Use Custom Discord Credentials")
        self.use_discord_credentials_checkbox.setChecked(False)


        self.load_mode_button = QPushButton("Load New Database from File",self)
        self.load_mode_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Load New Database from File.</span>')
        self.load_mode_button.setStyleSheet(
                "QPushButton { font-size: 10pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 10pt; background-color: #A13316; color: white; }"
            )
        self.load_mode_button.clicked.connect(self.onOpen)
        
        custom_credentials_layout = QHBoxLayout()
        custom_credentials_layout.addWidget(self.telegram_mode_button)
        custom_credentials_layout.addWidget(self.use_telegram_credentials_checkbox)
        custom_credentials_layout.addWidget(self.discord_mode_button)
        custom_credentials_layout.addWidget(self.use_discord_credentials_checkbox)
        custom_credentials_layout.addWidget(self.load_mode_button)
        layout.addLayout(custom_credentials_layout)
        self.counter = 0
        self.timer = time.time()
        settings = self.load_config()
        save_start = settings.get("Addresses_start", {}).get("START_ADDRESS", "").strip()
        save_end = settings.get("Addresses_stop", {}).get("END_ADDRESS", "").strip()

        if not save_start:
            save_start = '2000000000000000'

        if not save_end:
            save_end = '3FFFFFFFFFFFFFFFF'

        self.start_edit.setText(save_start)
        self.end_edit.setText(save_end)

    def onOpen(self):
        global addfind, BTC_BF_FILE
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "BF Files (*.bf);;Text Files (*.txt)"
        )

        if not filePath:
            return

        try:
            if filePath.endswith(".bf"):
                with open(filePath, "rb") as fp:
                    addfind = BloomFilter.load(fp)
            elif filePath.endswith(".txt"):
                with open(filePath, "r") as file:
                    addfind = file.read().split()
            else:
                raise ValueError("Unsupported file type")
            
            BTC_BF_FILE = filePath
            
        except Exception as e:
            error_message = f"Error loading file: {str(e)}"
            QMessageBox.critical(self, "Error", error_message)
            return

        success_message = f"File loaded: {filePath}"
        QMessageBox.information(self, "File Loaded", success_message)

        self.add_count_label.setText(self.count_addresses(BTC_BF_FILE))

    def count_addresses(self, btc_bf_file=None):
        if btc_bf_file is None:
            btc_bf_file = BTC_BF_FILE       
        try:
            last_updated = os.path.getmtime(BTC_BF_FILE)
            last_updated_datetime = datetime.datetime.fromtimestamp(last_updated)
            now = datetime.datetime.now()
            delta = now - last_updated_datetime

            if delta < datetime.timedelta(days=1):
                hours, remainder = divmod(delta.seconds, 3600)
                minutes = remainder // 60

                time_units = []

                if hours > 0:
                    time_units.append(f"{hours} {'hour' if hours == 1 else 'hours'}")

                if minutes > 0:
                    time_units.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")

                time_str = ', '.join(time_units)

                if time_units:
                    message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses. The database is <b>{time_str}</b> old.'
                else:
                    message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses. The database is <b>less than a minute</b> old.'
            elif delta < datetime.timedelta(days=2):
                hours, remainder = divmod(delta.seconds, 3600)
                minutes = remainder // 60

                time_str = f'1 day'

                if hours > 0:
                    time_str += f', {hours} {"hour" if hours == 1 else "hours"}'

                if minutes > 0:
                    time_str += f', {minutes} {"minute" if minutes == 1 else "minutes"}'

                message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses. The database is <b>{time_str}</b> old.'
            else:
                message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses. The database is <b>{delta.days} days</b> old.'
        except FileNotFoundError:
            message = f'Currently checking <b>{locale.format_string("%d", len(addfind), grouping=True)}</b> addresses.'

        return message

    def exit_app(self):
        QApplication.quit()

    def open_telegram_settings(self):
        settings_dialog = telegram_gui.Settings_telegram_Dialog(self)
        settings_dialog.exec()
    
    def open_discord_settings(self):
        settings_dialog = discord_gui.Settings_discord_Dialog(self)
        settings_dialog.exec()


    def toggle_visibility(self, checkbox, label_widget, text_widget):
        label_widget.setVisible(checkbox.isChecked())
        text_widget.setVisible(checkbox.isChecked())

    def update_keyspace_range(self, value):
        start_range = 2 ** (value - 1)
        end_range = 2 ** value - 1
        self.start_edit.setText(f"{start_range:X}")
        self.end_edit.setText(f"{end_range:X}")
        self.bitsLineEdit.setText(str(value))

    def updateSliderAndRanges(self, text):
        try:
            bits = int(text)
            bits = max(1, min(bits, 256))
            self.keyspace_slider.setValue(bits)

            if bits == 256:
                start_range = "8000000000000000000000000000000000000000000000000000000000000000"
                end_range = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140"
            else:
                start_range = 2 ** (bits - 1)
                end_range = 2 ** bits - 1
                start_range = f"{start_range:X}"
                end_range = f"{end_range:X}"

            self.start_edit.setText(start_range)
            self.end_edit.setText(end_range)
        except ValueError:
            range_message = "Range should be in Bit 1-256 "
            QMessageBox.information(self, "Range Error", range_message)

    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def start(self):
        try:
            start_value = int(self.start_edit.text(), 16)
            end_value = int(self.end_edit.text(), 16)
            self.total_steps = end_value - start_value
            self.scanning = True

            if self.random_button.isChecked():
                self.timer = QTimer(self)
                self.timer.timeout.connect(lambda: self.update_display_random(start_value, end_value))
            elif self.sequence_button.isChecked():
                self.current = start_value
                self.timer = QTimer(self)
                self.timer.timeout.connect(lambda: self.update_display_sequence(start_value, end_value))
            elif self.reverse_button.isChecked():
                self.current = end_value
                self.timer = QTimer(self)
                self.timer.timeout.connect(lambda: self.update_display_reverse(start_value, end_value))

            self.timer.start()
            self.start_time = time.time()
            self.timer.timeout.connect(self.update_keys_per_sec)
        except Exception as e:
            error_message = f"Ranges empty please Type a Start and Stop: {str(e)}"
            QMessageBox.critical(self, "Error", error_message)

    def stop(self):
        if isinstance(self.timer, QTimer):
            self.timer.stop()
            self.worker_finished("Recovery Finished")

    def worker_finished(self, result):
        if self.scanning:
            QMessageBox.information(self, "Recovery Finished", "Done")
        self.scanning = False

    # Method to handle crypto selection
    def handle_crypto_change(self, index):
        selected_crypto = self.crypto_selector.currentText()
        self.update_address_types(selected_crypto)

    def update_address_types(self, selected_crypto):
        self.compressed_checkbox.setChecked(True)
        self.uncompressed_checkbox.setChecked(True)
        self.p2sh_checkbox.setChecked(True)
        self.bech32_checkbox.setChecked(True)
        self.compressed_checkbox.setEnabled(True)
        self.uncompressed_checkbox.setEnabled(True)
        self.p2sh_checkbox.setEnabled(True)
        self.bech32_checkbox.setEnabled(True)

        unsupported_coins = [
            "Argentum (ARG)",
            "Axe (AXE)",
            "Bitcoin Cash (BCH)",
            "Bitcoin Diamond (BTCD)",
            "BitcoinStash (BSD)",
            "Bitcoin Gold (BTG)",
            "BitcoinX (BCX)",
            "Bitcore (BTDX)",
            "Bitcore (BTX)",
            "Chaucha (CHA)",
            "Dash (DASH)",
            "Defcoin (DFC)",
            "Digitalcoin (DGC)",
            "Dogecoin (DOGE)",
            "Faircoin (FAI)",
            "Feathercoin (FTC)",
            "Groestlcoin (GRS)",
            "Litecoin (LTC)",
            "Monacoin (MONA)",
            "Megacoin (MEC)",
            "Polis (POLIS)",
            "PIVX (PIVX)",
            "Riecoin (RIC)",
            "SmartCash (SMART)",
            "Stratis (STRAT)",
            "Syscoin (SYS)",
            "Terracoin (TRC)",
            "Viacoin (VIA)",
            "Myriad (XMY)",
            "Worldcoin (WDC)",
        ]

        unsupported_coins1 = [
            "Bitcoin SV (BSV)",
            "BitcoinCore (BC)",
            "Jumbucks (JBS)",
            "Mazacoin (MZC)",
            "Zeitcoin (ZEIT)",
            "Vertcoin (VTC)",
            "Unobtanium (UNO)",
            "Skeincoin (SKC)",
            "Ravencoin (RVN)",
            "Ormeus Coin (OMC)",
            "OKCash (OK)",
            "Namecoin (NMC)",
            "Gulden (NLG)",
            "LBRY Credits (LBC)",
            "Denarius (DNR)",
            "Bulwark (BWK)",
            "Peercoin (PPC)",

        ]

        if selected_crypto in unsupported_coins:
            self.bech32_checkbox.setChecked(False)
            self.bech32_checkbox.setEnabled(False)

        elif selected_crypto in unsupported_coins1:
            self.p2sh_checkbox.setChecked(False)
            self.bech32_checkbox.setChecked(False)
            self.p2sh_checkbox.setEnabled(False)
            self.bech32_checkbox.setEnabled(False) 

    def generate_crypto(self):
        global addfind
        power_format = self.format_combo_box_POWER.currentText()
        self.power_format = int(power_format)
        selected_crypto = self.crypto_selector.currentText()
        coin_type = crypto_mapping.get(selected_crypto, 0)
        dec_keys, HEX_keys, uncomp_keys, comp_keys, p2sh_keys, bech32_keys, eth_keys = [], [], [], [], [], [], []
        found = int(self.found_keys_scanned_edit.text())
        startPrivKey = self.num

        for i in range(0, self.power_format):
            dec = int(startPrivKey)
            HEX = f"{dec:016x}"
            dec_keys.append(dec)
            HEX_keys.append(HEX)

            if self.compressed_checkbox.isChecked():
                caddr = ice.privatekey_to_coinaddress(coin_type, 0, True, dec)
                comp_keys.append(caddr)

                if caddr in addfind:
                    found += 1
                    self.found_keys_scanned_edit.setText(str(found))
                    WINTEXT = f"\n {caddr} \n Decimal Private Key \n {dec} \n Hexadecimal Private Key \n {HEX}  \n"

                    try:
                        with open(WINNER_FOUND, "a") as f:
                            f.write(WINTEXT)
                    except FileNotFoundError:
                        os.makedirs(os.path.dirname(WINNER_FOUND), exist_ok=True)

                        with open(WINNER_FOUND, "w") as f:
                            f.write(WINTEXT)
                    if self.use_telegram_credentials_checkbox.isChecked():
                        telegram_gui.send_to_telegram(self, WINTEXT)
                    if self.use_discord_credentials_checkbox.isChecked():
                        discord_gui.send_to_discord(self, WINTEXT)
                    if self.win_checkbox.isChecked():
                        winner_dialog = win_gui.WinnerDialog(WINTEXT, self)
                        winner_dialog.exec()

            if self.uncompressed_checkbox.isChecked():
                uaddr = ice.privatekey_to_coinaddress(coin_type, 0, False, dec)
                uncomp_keys.append(uaddr)

                if uaddr in addfind:
                    found += 1
                    self.found_keys_scanned_edit.setText(str(found))
                    WINTEXT = f"\n {uaddr} \n Decimal Private Key \n {dec} \n Hexadecimal Private Key \n {HEX}  \n"

                    try:
                        with open(WINNER_FOUND, "a") as f:
                            f.write(WINTEXT)
                    except FileNotFoundError:
                        os.makedirs(os.path.dirname(WINNER_FOUND), exist_ok=True)

                        with open(WINNER_FOUND, "w") as f:
                            f.write(WINTEXT)

                    if self.use_telegram_credentials_checkbox.isChecked():
                        telegram_gui.send_to_telegram(self, WINTEXT)
                    if self.use_discord_credentials_checkbox.isChecked():
                        discord_gui.send_to_discord(self, WINTEXT)
                    if self.win_checkbox.isChecked():
                        winner_dialog = win_gui.WinnerDialog(WINTEXT, self)
                        winner_dialog.exec()

            if self.p2sh_checkbox.isChecked():
                p2sh = ice.privatekey_to_coinaddress(coin_type, 1, True, dec)
                p2sh_keys.append(p2sh)

                if p2sh in addfind:
                    found += 1
                    self.found_keys_scanned_edit.setText(str(found))
                    WINTEXT = f"\n {p2sh}\nDecimal Private Key \n {dec} \n Hexadecimal Private Key \n {HEX} \n"

                    try:
                        with open(WINNER_FOUND, "a") as f:
                            f.write(WINTEXT)
                    except FileNotFoundError:
                        os.makedirs(os.path.dirname(WINNER_FOUND), exist_ok=True)

                        with open(WINNER_FOUND, "w") as f:
                            f.write(WINTEXT)

                    if self.use_telegram_credentials_checkbox.isChecked():
                        telegram_gui.send_to_telegram(self, WINTEXT)
                    if self.use_discord_credentials_checkbox.isChecked():
                        discord_gui.send_to_discord(self, WINTEXT)
                    if self.win_checkbox.isChecked():
                        winner_dialog = win_gui.WinnerDialog(WINTEXT, self)
                        winner_dialog.exec()

            if self.bech32_checkbox.isChecked():
                bech32 = ice.privatekey_to_coinaddress(coin_type, 2, True, dec)
                bech32_keys.append(bech32)

                if bech32 in addfind:
                    found += 1
                    self.found_keys_scanned_edit.setText(str(found))
                    WINTEXT = f"\n {bech32}\n Decimal Private Key \n {dec} \n Hexadecimal Private Key \n {HEX} \n"

                    try:
                        with open(WINNER_FOUND, "a") as f:
                            f.write(WINTEXT)
                    except FileNotFoundError:
                        os.makedirs(os.path.dirname(WINNER_FOUND), exist_ok=True)

                        with open(WINNER_FOUND, "w") as f:
                            f.write(WINTEXT)

                    if self.use_telegram_credentials_checkbox.isChecked():
                        telegram_gui.send_to_telegram(self, WINTEXT)
                    if self.use_discord_credentials_checkbox.isChecked():
                        discord_gui.send_to_discord(self, WINTEXT)
                    if self.win_checkbox.isChecked():
                        winner_dialog = win_gui.WinnerDialog(WINTEXT, self)
                        winner_dialog.exec()

            if self.eth_checkbox.isChecked():
                ethaddr = ice.privatekey_to_ETH_address(dec)
                eth_keys.append(ethaddr)

                if ethaddr in addfind or ethaddr[2:] in addfind:
                    found += 1
                    self.found_keys_scanned_edit.setText(str(found))
                    WINTEXT = f"\n {ethaddr}\n Decimal Private Key \n {dec} \n Hexadecimal Private Key \n {HEX} \n"

                    try:
                        with open(WINNER_FOUND, "a") as f:
                            f.write(WINTEXT)
                    except FileNotFoundError:
                        os.makedirs(os.path.dirname(WINNER_FOUND), exist_ok=True)

                        with open(WINNER_FOUND, "w") as f:
                            f.write(WINTEXT)

                    if self.use_telegram_credentials_checkbox.isChecked():
                        telegram_gui.send_to_telegram(self, WINTEXT)
                    if self.use_discord_credentials_checkbox.isChecked():
                        discord_gui.send_to_discord(self, WINTEXT)
                    if self.win_checkbox.isChecked():
                        winner_dialog = win_gui.WinnerDialog(WINTEXT, self)
                        winner_dialog.exec()

            startPrivKey += 1


        self.value_edit_dec.setText(str(dec))
        self.value_edit_hex.setText(HEX)
        self.priv_text.setText("\n".join(map(str, dec_keys)))
        self.HEX_text.setText("\n".join(HEX_keys))
        self.uncomp_text.setText("\n".join(uncomp_keys))
        self.comp_text.setText("\n".join(comp_keys))
        self.p2sh_text.setText("\n".join(p2sh_keys))
        self.bech32_text.setText("\n".join(bech32_keys))
        self.eth_text.setText("\n".join(eth_keys))

        def save_config(config_data):
            with open(CONFIG_FILE, "w") as file:
                json.dump(config_data, file, indent=4)

        def update_config_start(start_address):
            config_data = self.load_config()
            config_data["Addresses_start"] = {
                "START_ADDRESS": f'{start_address}'
            }
            save_config(config_data)

        def update_config_stop(end_address):
            config_data = self.load_config()
            config_data["Addresses_stop"] = {
                "END_ADDRESS": f'{end_address}'
            }
            save_config(config_data)

        if self.sequence_button.isChecked():
            update_config_start(HEX)
        elif self.reverse_button.isChecked():
            update_config_stop(HEX)

    def update_display_random(self, start, end):
        utils.update_display_random(self, start, end)

    def update_display_sequence(self, start, end):
        utils.update_display_sequence(self, start, end)

    def update_display_reverse(self, start, end):
        utils.update_display_reverse(self, start, end)

    def update_keys_per_sec(self):
        utils.update_per_sec(self, self.keys_per_sec_edit, self.total_keys_scanned_edit)