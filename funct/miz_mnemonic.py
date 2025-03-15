"""

@author: Team Mizogg
"""
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import os
import datetime
import time
import random
import requests
import json
from funct.iceland import secp256k1 as ice
from funct import (win_gui, telegram_gui, discord_gui, load_file, team_word)
from funct.console_gui import ConsoleWindow
from config.config import *
from config.config_manager import config
import locale
from mnemonic import Mnemonic
from game.speaker import Speaker
import itertools
from bloomfilter import BloomFilter

addfind = load_file.load_addresses()
TEL_ICON = "images/Telegram.png"
DIS_ICON = "images/Discord.png"
WINNER_FOUND = "found/found.txt"
CONFIG_FILE = "config/settings.json"
########### Database Load and Files ###########
mylist = []
 
with open('input/mnemonics.txt', newline='', encoding='utf-8') as f:
    for line in f:
        mylist.append(line.strip())
class GUIInstance(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scanning = False
        self.initUI()

    def initUI(self):

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.add_count_label = QLabel(self.count_addresses(), objectName="count_addlabel", alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.add_count_label)
        power_label = QLabel("Amount Of Devrations to Show", self)
        power_label.setStyleSheet("font-size: 10pt; font-weight: bold;")

        ammount_words_label = QLabel('Amount of words:')
        ammount_words_label.setStyleSheet("font-size: 10pt; font-weight: bold;")
        ammount_words_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.ammount_words = QComboBox()
        self.ammount_words.addItems(['random', '12', '15', '18', '21', '24'])
        self.ammount_words.setCurrentIndex(1)
        
        lang_words_label = QLabel('Choose Language:')
        lang_words_label.setStyleSheet("font-size: 10pt; font-weight: bold;")
        lang_words_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lang_words = QComboBox()
        self.lang_words.addItems(['random', 'english', 'french', 'italian', 'spanish', 'chinese_simplified', 'chinese_traditional', 'japanese', 'korean'])
        self.lang_words.setCurrentIndex(1)

        self.format_combo_box_POWER = QLineEdit('1', self)
        self.format_combo_box_POWER.setPlaceholderText('Type here your Mnemonic to Check')
        self.format_combo_box_POWER.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Amount it Address to Check per scan. Ajust for best speed have to stop to change amount </span>')
        
        custom_phrase_layout = QHBoxLayout()
        custom_phrase_label = QLabel('Custom Phrase:')
        custom_phrase_layout.addWidget(custom_phrase_label)
        self.custom_phrase_edit = QLineEdit("abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about")
        self.custom_phrase_edit.setPlaceholderText('Type here your Mnemonic to Check')
        self.custom_phrase_edit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> TYPE a Mnemonic Here to check </span>')
        
        custom_phrase_layout.addWidget(self.custom_phrase_edit)
        enter_button = QPushButton('Enter')
        enter_button.setFixedWidth(300)
        enter_button.clicked.connect(self.enter)
        enter_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back)) if config.get("sound_enabled", True) else None
        custom_phrase_layout.addWidget(enter_button)

        shuffle_button_i = QPushButton('Iterate Over All')
        shuffle_button_i.clicked.connect(self.iterate_over_shuffles)
        shuffle_button_i.setFixedWidth(300)
        shuffle_button_i.clicked.connect(self.enter)
        shuffle_button_i.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back)) if config.get("sound_enabled", True) else None
        custom_phrase_layout.addWidget(shuffle_button_i)

        select_power_layout = QHBoxLayout()
        select_power_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        select_power_layout.addWidget(power_label)
        select_power_layout.addWidget(self.format_combo_box_POWER)
        select_power_layout.addWidget(ammount_words_label)
        select_power_layout.addWidget(self.ammount_words)
        select_power_layout.addWidget(lang_words_label)
        select_power_layout.addWidget(self.lang_words)
        layout.addLayout(custom_phrase_layout)

        start_button = QPushButton("Start", self)
        start_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start scanning </span>')
        start_button.clicked.connect(self.start)
        start_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus)) if config.get("sound_enabled", True) else None
        start_button.setFixedWidth(200)

        start_button_read = QPushButton("Read File of Menmonic Words", self)
        start_button_read.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start scanning </span>')
        start_button_read.clicked.connect(self.read_mnms)
        start_button_read.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus)) if config.get("sound_enabled", True) else None
        start_button_read.setFixedWidth(200)

        stop_button = QPushButton("Stop", self)
        stop_button.setStyleSheet(
            "QPushButton { font-size: 10pt; background-color: #1E1E1E; color: white; }"
            "QPushButton:hover { font-size: 10pt; background-color: #5D6062; color: white; }"
        )
        stop_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Stop scanning </span>')
        stop_button.clicked.connect(self.stop)
        stop_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back)) if config.get("sound_enabled", True) else None
        stop_button.setFixedWidth(200)

        control_layout = QHBoxLayout()
        control_layout.addLayout(select_power_layout)
        control_layout.addStretch(1)

        mnm_label = QLabel(" Mnenonics :")
        self.value_edit_mnm = QLineEdit()
        self.value_edit_mnm.setReadOnly(True)

        current_scan_layout = QHBoxLayout()
        current_scan_layout.addWidget(mnm_label)
        current_scan_layout.addWidget(self.value_edit_mnm)
        checkbox_labels = ["Compressed", "P2SH", "Bech32", "ETH", "Stop if found"]
        checkbox_objects = []
        checkbox_width = 140
        for label in checkbox_labels:
            checkbox = QCheckBox(label)
            checkbox.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Ticks can be removed to search for single type or mutiple types of Bitcoin Address. Removing some will increase speed. Address not selected we not be searched </span>')
            checkbox.setFixedWidth(checkbox_width)
            checkbox_objects.append(checkbox)
        self.compressed_checkbox, self.p2sh_checkbox, self.bech32_checkbox, self.eth_checkbox, self.win_checkbox = checkbox_objects[0:]
        checkboxes_to_check = [self.compressed_checkbox, self.p2sh_checkbox, self.bech32_checkbox]
        for checkbox in checkboxes_to_check:
            checkbox.setChecked(True)
        self.eth_checkbox.setChecked(False)
        self.win_checkbox.setChecked(False)
        divider = QFrame(frameShape=QFrame.Shape.VLine, frameShadow=QFrame.Shadow.Sunken)
        radio_and_checkbox_layout = QHBoxLayout()

        widgets = [
            self.compressed_checkbox,
            self.p2sh_checkbox, self.bech32_checkbox,
            self.eth_checkbox, self.win_checkbox
        ]

        for widget in widgets:
            radio_and_checkbox_layout.addWidget(widget)

        layouts = [
            control_layout, 
            radio_and_checkbox_layout, current_scan_layout
        ]

        for l in layouts:
            layout.addLayout(l)

        def create_line_edit(read_only=True, text="0"):
            line_edit = QLineEdit()
            line_edit.setReadOnly(read_only)
            line_edit.setText(text)
            return line_edit

        self.found_mnms_scanned_edit = create_line_edit()
        self.total_mnms_scanned_edit = create_line_edit()
        self.mnms_per_sec_edit = create_line_edit(False, "")
        labels_and_edits = [
            ("Found", self.found_mnms_scanned_edit),
            ("Total Mnemonic scanned:", self.total_mnms_scanned_edit),
            ("Menmonics per second:", self.mnms_per_sec_edit)
        ]

        mnms_layout = QHBoxLayout()

        for label_text, edit_widget in labels_and_edits:
            label = QLabel(label_text)
            mnms_layout.addWidget(label)
            mnms_layout.addWidget(edit_widget)

        layout.addLayout(mnms_layout)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(start_button)
        buttonLayout.addWidget(stop_button)
        buttonLayout.addWidget(start_button_read)
        layout.addLayout(buttonLayout)
        self.consoleWindow = ConsoleWindow(self)
        layout.addWidget(self.consoleWindow)

        icon_size = QSize(26, 26)
        icontel = QIcon(QPixmap(TEL_ICON))
        icondis = QIcon(QPixmap(DIS_ICON))

        self.telegram_mode_button = QPushButton(self)
        self.telegram_mode_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Enter Custom Telegram Credentials Settings .</span>')
        self.telegram_mode_button.setStyleSheet("font-size: 10pt;")
        self.telegram_mode_button.setIconSize(icon_size)
        self.telegram_mode_button.setIcon(icontel)
        self.telegram_mode_button.clicked.connect(self.open_telegram_settings)
        self.telegram_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back)) if config.get("sound_enabled", True) else None
        self.use_telegram_credentials_checkbox = QCheckBox("Use Custom Telegram Credentials")
        self.use_telegram_credentials_checkbox.setChecked(False)

        self.discord_mode_button = QPushButton(self)
        self.discord_mode_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Enter Custom Discord Credentials Settings .</span>')
        self.discord_mode_button.setStyleSheet("font-size: 10pt;")
        self.discord_mode_button.setIconSize(icon_size)
        self.discord_mode_button.setIcon(icondis)
        self.discord_mode_button.clicked.connect(self.open_discord_settings)
        self.discord_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back)) if config.get("sound_enabled", True) else None
        self.use_discord_credentials_checkbox = QCheckBox("Use Custom Discord Credentials")
        self.use_discord_credentials_checkbox.setChecked(False)


        self.load_mode_button = QPushButton("Load New Database from File",self)
        self.load_mode_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Load New Database from File.</span>')
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

    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def start(self):
        self.scanning = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.generate_mnemonic)
        self.timer.start()
        self.start_time = time.time()
        self.timer.timeout.connect(self.update_mnms_per_sec)

    def stop(self):
        if isinstance(self.timer, QTimer):
            self.timer.stop()
            self.worker_finished("Recovery Finished")

    def worker_finished(self, result):
        if self.scanning:
            QMessageBox.information(self, "Recovery Finished", "Done")
        self.scanning = False
        
    def generate_mnemonic(self):
        if self.timer.isActive():
            if self.lang_words.currentText() == 'random':
                lang = random.choice(['english', 'french', 'italian', 'spanish', 'chinese_simplified', 'chinese_traditional', 'japanese', 'korean'])
            else:
                lang = self.lang_words.currentText()
            
            if self.ammount_words.currentText() == 'random':
                word_length = random.choice([12, 15, 18, 21, 24])
            else:
                word_length = int(self.ammount_words.currentText())
            
            strengths = {
                12: 128,
                15: 160,
                18: 192,
                21: 224,
                24: 256
            }
            strength = strengths[word_length]
            mnemonic = Mnemonic(lang)
            words = mnemonic.generate(strength=strength)
            self.mnemonic_btc(words)

    def enter(self):
        words = self.custom_phrase_edit.text()
        self.mnemonic_btc(words)

    def iterate_over_shuffles(self):
        self.permutation_iterator = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_next_permutation)
        self.timer.start(0)
        self.start_time = time.time()
        self.timer.timeout.connect(self.update_mnms_per_sec)

    def process_next_permutation(self):
        if not self.permutation_iterator:
            original_words = self.custom_phrase_edit.text().split()
            self.permutation_iterator = itertools.permutations(original_words)

        try:
            permuted_words = next(self.permutation_iterator)
            shuffled_text = ' '.join(permuted_words)
            self.mnemonic_btc(shuffled_text)
        except StopIteration:
            self.timer.stop()
            self.permutation_iterator = None

    def read_mnms(self):
        self.word_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_next_mnm)
        self.timer.start(0)
        self.start_time = time.time()
        self.timer.timeout.connect(self.update_mnms_per_sec)

    def process_next_mnm(self):
        if self.word_index < len(mylist):
            words = mylist[self.word_index]
            self.mnemonic_btc(words)
            self.word_index += 1
        else:
            self.timer.stop()

    def mnemonic_btc(self, words):
        found = int(self.found_mnms_scanned_edit.text())
        power_format = int(self.format_combo_box_POWER.text())
        try:
            seed = team_word.mnem_to_seed(words)
            for r in range (0,power_format):
                if self.compressed_checkbox.isChecked():
                    pvk = team_word.bip39seed_to_private_key(seed, r)
                    dec = (int.from_bytes(pvk, "big"))
                    HEX = "%064x" % dec
                    caddr = ice.privatekey_to_address(0, True, (int.from_bytes(pvk, "big")))
                    cpath = f"m/44'/0'/0'/0/{r}"
                    wordvartext = (f'\n Menmonic {words} \n Bitcoin {cpath} :  {caddr} \n Dec : {dec} \n   Hex : {HEX}  ')
                    self.consoleWindow.append_output(wordvartext)
                    if caddr in addfind:
                        found += 1
                        self.found_mnms_scanned_edit.setText(str(found))
                        WINTEXT = f"\n Menmonic {words} \n {caddr} \n Decimal Private Key \n {dec} \n Hexadecimal Private Key \n {HEX}  \n"

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
                    pvk2 = team_word.bip39seed_to_private_key2(seed, r)
                    dec2 = (int.from_bytes(pvk2, "big"))
                    HEX2 = "%064x" % dec2
                    p2sh = ice.privatekey_to_address(1, True, (int.from_bytes(pvk2, "big")))
                    ppath = f"m/49'/0'/0'/0/{r}"
                    wordvartext = (f'\n Menmonic {words} \n Bitcoin {ppath} :  {p2sh}\n Dec : {dec2} \n  Hex : {HEX2}')
                    self.consoleWindow.append_output(wordvartext)
                    if p2sh in addfind:
                        found += 1
                        self.found_mnms_scanned_edit.setText(str(found))
                        WINTEXT = f"\n Menmonic {words} \n {p2sh}\nDecimal Private Key \n {dec2} \n Hexadecimal Private Key \n {HEX2} \n"

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
                    pvk3 = team_word.bip39seed_to_private_key3(seed, r)
                    dec3 = (int.from_bytes(pvk3, "big"))
                    HEX3 = "%064x" % dec3
                    bech32 = ice.privatekey_to_address(2, True, (int.from_bytes(pvk3, "big")))
                    bpath = f"m/84'/0'/0'/0/{r}"
                    wordvartext = (f'\n Menmonic {words} \n Bitcoin {bpath} : {bech32}\n  Dec : {dec3} \n  Hex : {HEX3} ')
                    self.consoleWindow.append_output(wordvartext)
                    if bech32 in addfind:
                        found += 1
                        self.found_mnms_scanned_edit.setText(str(found))
                        WINTEXT = f"\n Menmonic {words} \n {bech32}\n Decimal Private Key \n {dec3} \n Hexadecimal Private Key \n {HEX3} \n"

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
                    pvk4 = team_word.bip39seed_to_private_key4(seed, r)
                    dec4 = (int.from_bytes(pvk4, "big"))
                    HEX4 = "%064x" % dec4
                    ethaddr = ice.privatekey_to_ETH_address(int.from_bytes(pvk4, "big"))
                    epath = f"m/44'/60'/0'/0/{r}"
                    wordvartext = (f'\n Menmonic {words} \n Eth {epath} : {ethaddr}\n  Dec : {dec4} \n  Hex : {HEX4} ')
                    self.consoleWindow.append_output(wordvartext)
                    if ethaddr in addfind or ethaddr[2:] in addfind:
                        found += 1
                        self.found_mnms_scanned_edit.setText(str(found))
                        WINTEXT = f"\n Menmonic {words} \n {ethaddr}\n Decimal Private Key \n {dec4} \n Hexadecimal Private Key \n {HEX4} \n"

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
            self.value_edit_mnm.setText(words)
            self.counter += 1
        except ValueError:
            print("Invalid input. Please enter a valid Menmonics.")

    def update_mnms_per_sec(self):
        elapsed_time = time.time() - self.start_time

        if elapsed_time == 0:
            mnms_per_sec = 0
        else:
            mnms_per_sec = self.counter / elapsed_time

        mnms_per_sec = round(mnms_per_sec, 2)

        total_mnms_scanned_text = self.total_mnms_scanned_edit.text()
        total_mnms_scanned = locale.atoi(total_mnms_scanned_text) + self.counter

        total_mnms_scanned_formatted = locale.format_string("%d", total_mnms_scanned, grouping=True)
        mnms_per_sec_formatted = locale.format_string("%.2f", mnms_per_sec, grouping=True)

        self.total_mnms_scanned_edit.setText(total_mnms_scanned_formatted)
        self.mnms_per_sec_edit.setText(mnms_per_sec_formatted)
        self.start_time = time.time()
        self.counter = 0