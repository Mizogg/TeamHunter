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
from funct import (win_gui, telegram_gui, discord_gui, load_file, team_brain)
from funct.console_gui import ConsoleWindow
from config.config import *
import locale
from game.speaker import Speaker
import itertools
from config import *
import locale

addfind = load_file.load_addresses()
TEL_ICON = "images/main/Telegram.png"
DIS_ICON = "images/main/Discord.png"
WINNER_FOUND = "found/found.txt"
CONFIG_FILE = "config/config.json"
########### Database Load and Files ###########
mylist = []
 
with open('input/words.txt', newline='', encoding='utf-8') as f:
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

        ammount_words_label = QLabel('Amount of words:')
        ammount_words_label.setStyleSheet("font-size: 10pt; font-weight: bold; color: #E7481F;")
        ammount_words_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.ammount_words = QComboBox()
        self.ammount_words.addItems(['random', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'])
        self.ammount_words.setCurrentIndex(2)
    
        custom_phrase_layout = QHBoxLayout()
        custom_phrase_label = QLabel('Custom BrainWallet:')
        custom_phrase_layout.addWidget(custom_phrase_label)
        self.custom_phrase_edit = QLineEdit("bitcoin is awsome")
        self.custom_phrase_edit.setPlaceholderText('Type here your BrainWallet to Check')
        self.custom_phrase_edit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> TYPE a BrainWallet Here to check </span>')
        
        custom_phrase_layout.addWidget(self.custom_phrase_edit)
        enter_button = QPushButton('Enter')
        enter_button.setStyleSheet(
                "QPushButton { font-size: 10pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 10pt; background-color: #A13316; color: white; }"
            )
        enter_button.setFixedWidth(200)
        enter_button.clicked.connect(self.enter)
        enter_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back))
        custom_phrase_layout.addWidget(enter_button)

        shuffle_button_i = QPushButton('Iterate Over All')
        shuffle_button_i.clicked.connect(self.iterate_over_shuffles)
        shuffle_button_i.setStyleSheet(
                "QPushButton { font-size: 10pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 10pt; background-color: #A13316; color: white; }"
            )
        shuffle_button_i.setFixedWidth(200)
        shuffle_button_i.clicked.connect(self.enter)
        shuffle_button_i.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back))
        custom_phrase_layout.addWidget(shuffle_button_i)

        select_power_layout = QHBoxLayout()
        select_power_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        select_power_layout.addWidget(ammount_words_label)
        select_power_layout.addWidget(self.ammount_words)
        layout.addLayout(custom_phrase_layout)

        start_button = QPushButton("Start Random Amount of Words", self)
        start_button.setStyleSheet(
                "QPushButton { font-size: 10pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 10pt; background-color: #A13316; color: white; }"
            )
        start_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start scanning </span>')
        start_button.clicked.connect(self.start)
        start_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        start_button.setFixedWidth(200)

        start_button_read = QPushButton("Read File of BrainWallet Words", self)
        start_button_read.setStyleSheet(
                "QPushButton { font-size: 10pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 10pt; background-color: #A13316; color: white; }"
            )
        start_button_read.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start scanning </span>')
        start_button_read.clicked.connect(self.read_brains)
        start_button_read.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        start_button_read.setFixedWidth(200)

        stop_button = QPushButton("Stop", self)
        stop_button.setStyleSheet(
            "QPushButton { font-size: 10pt; background-color: #1E1E1E; color: white; }"
            "QPushButton:hover { font-size: 10pt; background-color: #5D6062; color: white; }"
        )
        stop_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Stop scanning </span>')
        stop_button.clicked.connect(self.stop)
        stop_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back))
        stop_button.setFixedWidth(200)

        control_layout = QHBoxLayout()
        #control_layout.addStretch(1)

        brain_label = QLabel(" BrainWallet Words :")
        self.value_edit_brain = QLineEdit()
        self.value_edit_brain.setReadOnly(True)

        current_scan_layout = QHBoxLayout()
        current_scan_layout.addWidget(brain_label)
        current_scan_layout.addWidget(self.value_edit_brain)


        layouts = [
            control_layout, 
            current_scan_layout
        ]

        for l in layouts:
            layout.addLayout(l)

        def create_line_edit(read_only=True, text="0"):
            line_edit = QLineEdit()
            line_edit.setReadOnly(read_only)
            line_edit.setText(text)
            return line_edit

        self.found_brains_scanned_edit = create_line_edit()
        self.total_brains_scanned_edit = create_line_edit()
        self.brains_per_sec_edit = create_line_edit(False, "")
        labels_and_edits = [
            ("Found", self.found_brains_scanned_edit),
            ("Total Brains scanned:", self.total_brains_scanned_edit),
            ("Brains per second:", self.brains_per_sec_edit)
        ]

        brains_layout = QHBoxLayout()

        for label_text, edit_widget in labels_and_edits:
            label = QLabel(label_text)
            brains_layout.addWidget(label)
            brains_layout.addWidget(edit_widget)

        layout.addLayout(brains_layout)
        buttonLayout = QHBoxLayout()
        buttonLayout.addLayout(select_power_layout)
        buttonLayout.addWidget(start_button)
        buttonLayout.addWidget(start_button_read)
        buttonLayout.addWidget(stop_button)
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
        self.telegram_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back))
        self.use_telegram_credentials_checkbox = QCheckBox("Use Custom Telegram Credentials")
        self.use_telegram_credentials_checkbox.setChecked(False)

        self.discord_mode_button = QPushButton(self)
        self.discord_mode_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Enter Custom Discord Credentials Settings .</span>')
        self.discord_mode_button.setStyleSheet("font-size: 10pt;")
        self.discord_mode_button.setIconSize(icon_size)
        self.discord_mode_button.setIcon(icondis)
        self.discord_mode_button.clicked.connect(self.open_discord_settings)
        self.discord_mode_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back))
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

    def onOpen(self):
        global addfind, BTC_TXT_FILE
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt)"
        )

        if not filePath:
            return

        try:
            if filePath.endswith(".txt"):
                with open(filePath, "r") as file:
                    addfind = file.read().split()
            else:
                raise ValueError("Unsupported file type")
            
            BTC_TXT_FILE = filePath
            
        except Exception as e:
            error_message = f"Error loading file: {str(e)}"
            QMessageBox.critical(self, "Error", error_message)
            return

        success_message = f"File loaded: {filePath}"
        QMessageBox.information(self, "File Loaded", success_message)

        self.add_count_label.setText(self.count_addresses(BTC_TXT_FILE))

    def exit_app(self):
        QApplication.quit()

    def open_telegram_settings(self):
        settings_dialog = telegram_gui.Settings_telegram_Dialog(self)
        settings_dialog.exec()
    
    def open_discord_settings(self):
        settings_dialog = discord_gui.Settings_discord_Dialog(self)
        settings_dialog.exec()

    def count_addresses(self, btc_txt_file=None):
        if btc_txt_file is None:
            btc_txt_file = BTC_TXT_FILE       
        try:
            last_updated = os.path.getmtime(BTC_TXT_FILE)
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

    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def start(self):
        self.scanning = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.generate_brains)
        self.timer.start()
        self.start_time = time.time()
        self.timer.timeout.connect(self.update_brains_per_sec)

    def stop(self):
        if isinstance(self.timer, QTimer) and self.timer.isActive():
            self.timer.stop()
            self.worker_finished("Recovery Finished")
        else:
            self.worker_finished("User Stopped")

    def worker_finished(self, result):
        if self.scanning:
            QMessageBox.information(self, "Recovery Finished", "Done")
        self.scanning = False

    def generate_brains(self):
        if self.ammount_words.currentText() == 'random':
                word_length = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
        else:
            word_length = int(self.ammount_words.currentText())
        if self.timer.isActive():
            passphrase = ' '.join(random.sample(mylist, word_length))
            self.brains_btc(passphrase)

    def enter(self):
        passphrase = self.custom_phrase_edit.text()
        total_brains_scanned_text = int(self.total_brains_scanned_edit.text())
        self.brains_btc(passphrase)
        total_brains_scanned_text +=1
        self.total_brains_scanned_edit.setText(str(total_brains_scanned_text))

    def iterate_over_shuffles(self):
        self.permutation_iterator = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_next_permutation)
        self.timer.start(0)
        self.start_time = time.time()
        self.timer.timeout.connect(self.update_brains_per_sec)


    def process_next_permutation(self):
        if not self.permutation_iterator:
            original_words = self.custom_phrase_edit.text().split()
            self.permutation_iterator = itertools.permutations(original_words)

        try:
            permuted_words = next(self.permutation_iterator)
            shuffled_text = ' '.join(permuted_words)
            self.brains_btc(shuffled_text)
        except StopIteration:
            self.timer.stop()
            self.permutation_iterator = None


    def read_brains(self):
        self.word_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_next_word)
        self.timer.start(0)
        self.start_time = time.time()
        self.timer.timeout.connect(self.update_brains_per_sec)

    def process_next_word(self):
        if self.word_index < len(mylist):
            passphrase = mylist[self.word_index]
            self.brains_btc(passphrase)
            self.word_index += 1
        else:
            self.timer.stop()

    def brains_btc(self, passphrase):
        found = int(self.found_brains_scanned_edit.text())
        try:
            wallet = team_brain.BrainWallet()
            private_key, uaddr = wallet.generate_address_from_passphrase(passphrase)
            brainvartext = (f'\n BrainWallet: {passphrase} \n Private Key In HEX : {private_key} \n Bitcoin Adress : {uaddr}')
            self.consoleWindow.append_output(brainvartext)
            if uaddr in addfind:
                found += 1
                self.found_brains_scanned_edit.setText(str(found))
                WINTEXT = (f'\n BrainWallet: {passphrase} \n Private Key In HEX : {private_key} \n Bitcoin Adress : {uaddr}')

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

                
            self.value_edit_brain.setText(passphrase)
            self.counter += 1
        except ValueError:
            print("Invalid input. Please enter a valid Menmonics.")

    def update_brains_per_sec(self):
        elapsed_time = time.time() - self.start_time

        if elapsed_time == 0:
            brains_per_sec = 0
        else:
            brains_per_sec = self.counter / elapsed_time

        brains_per_sec = round(brains_per_sec, 2)

        total_brains_scanned_text = self.total_brains_scanned_edit.text()
        total_brains_scanned = locale.atoi(total_brains_scanned_text) + self.counter

        total_brains_scanned_formatted = locale.format_string("%d", total_brains_scanned, grouping=True)
        brains_per_sec_formatted = locale.format_string("%.2f", brains_per_sec, grouping=True)

        self.total_brains_scanned_edit.setText(total_brains_scanned_formatted)
        self.brains_per_sec_edit.setText(brains_per_sec_formatted)
        self.start_time = time.time()
        self.counter = 0