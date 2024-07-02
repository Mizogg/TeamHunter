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
from funct import (win_gui, telegram_gui, discord_gui, load_file, team_poetry)
from config.config import *
import locale
from game.speaker import Speaker
import itertools

addfind = load_file.load_addresses()
TEL_ICON = "images/main/Telegram.png"
DIS_ICON = "images/main/Discord.png"
WINNER_FOUND = "found/found.txt"
CONFIG_FILE = "config/config.json"
########### Database Load and Files ###########
mylist = []
 
with open('input/pharse66.txt', newline='', encoding='utf-8') as f:
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
        self.ammount_words.addItems(['random', '3', '6', '9', '12', '15', '18', '21', '24'])
        self.ammount_words.setCurrentIndex(3)

        custom_phrase_layout = QHBoxLayout()
        custom_phrase_label = QLabel('Custom Phrase:')
        custom_phrase_layout.addWidget(custom_phrase_label)
        self.custom_phrase_edit = QLineEdit("north pride grab bird toss shoe")
        self.custom_phrase_edit.setPlaceholderText('Type here your Poetry to Check')
        self.custom_phrase_edit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> TYPE a Poetry Here to check </span>')
        
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

        power_label = QLabel("Amount Of Addresses Per Page to Show", self)
        power_label.setStyleSheet("font-size: 10pt; font-weight: bold; color: #E7481F;")

        self.format_combo_box_POWER = QComboBox(self)
        self.format_combo_box_POWER.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Amount it Address to Check per scan. Ajust for best speed have to stop to change amount </span>')
        self.format_combo_box_POWER.addItems(
            ["1024", "2048", "4096", "8192", "16384"]
        )
        self.format_combo_box_POWER.setCurrentIndex(2)
        select_power_layout.addWidget(power_label)
        select_power_layout.addWidget(self.format_combo_box_POWER)
        layout.addLayout(custom_phrase_layout)

        start_button = QPushButton("Start Random Poetry", self)
        start_button.setStyleSheet(
                "QPushButton { font-size: 10pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 10pt; background-color: #A13316; color: white; }"
            )
        start_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start scanning Random Poetry (Change amount of words in drop down)</span>')
        start_button.clicked.connect(self.start)
        start_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        start_button.setFixedWidth(200)

        start_button_ice = QPushButton("Start Poetry In Range", self)
        start_button_ice.setStyleSheet(
                "QPushButton { font-size: 10pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 10pt; background-color: #A13316; color: white; }"
            )
        start_button_ice.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start scanning Range Poetry (use the slider or edit keyspace range)</span>')
        start_button_ice.clicked.connect(self.start_range)
        start_button_ice.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        start_button_ice.setFixedWidth(200)

        start_button_read = QPushButton("Read File of Poetry Words", self)
        start_button_read.setStyleSheet(
                "QPushButton { font-size: 10pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 10pt; background-color: #A13316; color: white; }"
            )
        start_button_read.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start scanning from you Text file of saved Poetry words (Make sure to save in the Input folder)</span>')
        start_button_read.clicked.connect(self.read_poem)
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


        options_layout2 = QHBoxLayout()

        self.keyspaceLabel = QLabel("Key Space:", self)
        options_layout2.addWidget(self.keyspaceLabel)

        self.start_edit = QLineEdit("2305843009213693952")
        self.start_edit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Type in Starting Decimal or Use Slider to update</span>')

        self.end_edit = QLineEdit("73786976294838206463")
        self.end_edit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Type in Ending Decimal or Use Slider to update</span>')

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

        control_layout = QHBoxLayout()
        control_layout.addLayout(select_power_layout)
        control_layout.addStretch(1)

        checkbox_labels = ["DEC", "HEX", "Compressed", "UnCompressed", "Stop if found"]
        checkbox_objects = []
        checkbox_width = 140
        for label in checkbox_labels:
            checkbox = QCheckBox(label)
            checkbox.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Ticks can be removed to search for single type or mutiple types of Bitcoin Address. Removing some will increase speed. Address not selected we not be searched </span>')
            checkbox.setFixedWidth(checkbox_width)
            checkbox_objects.append(checkbox)
        self.dec_checkbox, self.hex_checkbox, self.compressed_checkbox, self.uncompressed_checkbox, self.win_checkbox = checkbox_objects[0:]
        checkboxes_to_check = [self.compressed_checkbox, self.uncompressed_checkbox]
        for checkbox in checkboxes_to_check:
            checkbox.setChecked(True)
        self.win_checkbox.setChecked(False)
        divider = QFrame(frameShape=QFrame.Shape.VLine, frameShadow=QFrame.Shadow.Sunken)
        radio_and_checkbox_layout = QHBoxLayout()

        widgets = [
            self.random_button, self.sequence_button, self.reverse_button, divider,
            self.dec_checkbox, self.hex_checkbox, self.compressed_checkbox,
            self.uncompressed_checkbox, self.win_checkbox
        ]

        for widget in widgets:
            radio_and_checkbox_layout.addWidget(widget)

        layouts = [
            control_layout, options_layout2, 
            radio_and_checkbox_layout
        ]

        for l in layouts:
            layout.addLayout(l)

        def create_line_edit(read_only=True, text="0"):
            line_edit = QLineEdit()
            line_edit.setReadOnly(read_only)
            line_edit.setText(text)
            return line_edit

        self.found_poem_scanned_edit = create_line_edit()
        self.total_poem_scanned_edit = create_line_edit()
        self.poem_per_sec_edit = create_line_edit(False, "")
        labels_and_edits = [
            ("Found", self.found_poem_scanned_edit),
            ("Total Poems scanned:", self.total_poem_scanned_edit),
            ("Poems per second:", self.poem_per_sec_edit)
        ]

        poem_layout = QHBoxLayout()

        for label_text, edit_widget in labels_and_edits:
            label = QLabel(label_text)
            poem_layout.addWidget(label)
            poem_layout.addWidget(edit_widget)

        layout.addLayout(poem_layout)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(start_button)
        buttonLayout.addWidget(start_button_ice)
        buttonLayout.addWidget(start_button_read)
        buttonLayout.addWidget(stop_button)
        layout.addLayout(buttonLayout)

        self.address_layout_ = QGridLayout()
        self.poem_label = QLabel("Poetry Keys: ")
        self.poem_text = QTextEdit(self)
        self.poem_text.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Poetry Key Output</span>')
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
        self.address_layout_.addWidget(self.poem_label, 1, 0)
        self.address_layout_.addWidget(self.poem_text, 2, 0)
        self.address_layout_.addWidget(self.priv_label, 1, 1)
        self.address_layout_.addWidget(self.priv_text, 2, 1)
        self.address_layout_.addWidget(self.HEX_label, 1, 2)
        self.address_layout_.addWidget(self.HEX_text, 2, 2)
        self.address_layout_.addWidget(self.comp_label, 1, 3)
        self.address_layout_.addWidget(self.comp_text, 2, 3)
        self.address_layout_.addWidget(self.uncomp_label, 1, 4)
        self.address_layout_.addWidget(self.uncomp_text, 2, 4)

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
        self.toggle_visibility(self.dec_checkbox, self.priv_label, self.priv_text)
        self.toggle_visibility(self.hex_checkbox, self.HEX_label, self.HEX_text)
        self.toggle_visibility(
            self.compressed_checkbox, self.comp_label, self.comp_text
        )
        self.toggle_visibility(
            self.uncompressed_checkbox, self.uncomp_label, self.uncomp_text
        )
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

    def toggle_visibility(self, checkbox, label_widget, text_widget):
        label_widget.setVisible(checkbox.isChecked())
        text_widget.setVisible(checkbox.isChecked())

    def update_keyspace_range(self, value):
        start_range = hex(2 ** (value - 1))
        end_range = hex(2 ** value - 1)
        self.start_edit.setText(start_range)
        self.end_edit.setText(end_range)
        self.bitsLineEdit.setText(str(value))


    def updateSliderAndRanges(self, text):
        try:
            bits = int(text)
            bits = max(0, min(bits, 256))
            start_range = str(2 ** (bits - 1))
            end_range = str(2 ** bits - 1)
            self.keyspace_slider.setValue(bits)
            self.start_edit.setText(start_range)
            self.end_edit.setText(end_range)

        except ValueError:
            range_message = "Range should be in Bit 1-256 "
            QMessageBox.information(self, "Range Error", range_message)

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
        self.timer.timeout.connect(self.generate_poetry)
        self.timer.start()
        self.start_time = time.time()
        self.timer.timeout.connect(self.update_poem_per_sec)

    def stop(self):
        if isinstance(self.timer, QTimer):
            self.timer.stop()
            self.worker_finished("Recovery Finished")

    def worker_finished(self, result):
        if self.scanning:
            QMessageBox.information(self, "Recovery Finished", "Done")
        self.scanning = False
        
    def generate_poetry(self):
        if self.ammount_words.currentText() == 'random':
                word_length = random.choice([3, 6, 9, 12, 15, 18, 21, 24])
        else:
            word_length = int(self.ammount_words.currentText())
        if self.timer.isActive():
            passphrase = ' '.join(random.sample(team_poetry.mn_words, word_length))
            self.poetry_btc(passphrase)

    def enter(self):
        words = self.custom_phrase_edit.text()
        self.poetry_btc(words)

    def iterate_over_shuffles(self):
        self.permutation_iterator = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_next_permutation)
        self.timer.start(0)
        self.start_time = time.time()
        self.timer.timeout.connect(self.update_poem_per_sec)

    def process_next_permutation(self):
        if not self.permutation_iterator:
            original_words = self.custom_phrase_edit.text().split()
            self.permutation_iterator = itertools.permutations(original_words)

        try:
            permuted_words = next(self.permutation_iterator)
            shuffled_text = ' '.join(permuted_words)
            self.poetry_btc(shuffled_text)
        except StopIteration:
            self.timer.stop()
            self.permutation_iterator = None

    def read_poem(self):
        self.word_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_next_mnm)
        self.timer.start(0)
        self.start_time = time.time()
        self.timer.timeout.connect(self.update_poem_per_sec)

    def process_next_mnm(self):
        if self.word_index < len(mylist):
            words = mylist[self.word_index]
            words_lower = words.lower()
            self.poetry_btc(words_lower)
            self.word_index += 1
        else:
            self.timer.stop()

    def poetry_btc(self, words):
        found = int(self.found_poem_scanned_edit.text())
        try:
            HEX = team_poetry.mn_decode(words)
            dec = int(HEX, 16)
            if self.compressed_checkbox.isChecked():
                caddr = ice.privatekey_to_address(0, True, dec)
                self.comp_text.setText(caddr)
                if caddr in addfind:
                    found += 1
                    self.found_poem_scanned_edit.setText(str(found))
                    WINTEXT = f"\n {words} \n {caddr} \n Decimal Private Key \n {dec} \n Hexadecimal Private Key \n {HEX}  \n"

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
                uaddr = ice.privatekey_to_address(0, False, dec)
                self.uncomp_text.setText(uaddr)
                if uaddr in addfind:
                    found += 1
                    self.found_poem_scanned_edit.setText(str(found))
                    WINTEXT = f"n {words} \n {uaddr} \n Decimal Private Key \n {dec} \n Hexadecimal Private Key \n {HEX}  \n"

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
                    
            self.poem_text.setText(words)
            self.priv_text.setText(str(int(dec)))
            self.HEX_text.setText(HEX)

            self.counter += 1
        except ValueError as ve:
            print(f"Invalid input. Please enter a valid Poetry Words. Error: {ve}")

    def start_range(self):
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
            self.timer.timeout.connect(self.update_poem_per_sec)
        except Exception as e:
            error_message = f"Ranges empty please Type a Start and Stop: {str(e)}"
            QMessageBox.critical(self, "Error", error_message)

    def generate_crypto(self):
        power_format = self.format_combo_box_POWER.currentText()
        self.power_format = int(power_format)
        dec_keys, HEX_keys, uncomp_keys, comp_keys, poem_keys = [], [], [], [], []
        found = int(self.found_poem_scanned_edit.text())
        startPrivKey = self.num

        for i in range(0, self.power_format):
            dec = int(startPrivKey)
            HEX = hex(dec)
            poetry = team_poetry.hex_to_poetry(HEX[2:])
            dec_keys.append(dec)
            HEX_keys.append(HEX)
            poem_keys.append(poetry)

            if self.compressed_checkbox.isChecked():
                caddr = ice.privatekey_to_address(0, True, dec)
                comp_keys.append(caddr)

                if caddr in addfind:
                    found += 1
                    self.found_poem_scanned_edit.setText(str(found))
                    WINTEXT = f"\n {poetry} \n {caddr} \n Decimal Private Key \n {dec} \n Hexadecimal Private Key \n {HEX}  \n"

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
                uaddr = ice.privatekey_to_address(0, False, dec)
                uncomp_keys.append(uaddr)

                if uaddr in addfind:
                    found += 1
                    self.found_poem_scanned_edit.setText(str(found))
                    WINTEXT = f"n {poetry} \n {uaddr} \n Decimal Private Key \n {dec} \n Hexadecimal Private Key \n {HEX}  \n"

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

        self.poem_text.setText("\n".join(poem_keys))
        self.priv_text.setText("\n".join(map(str, dec_keys)))
        self.HEX_text.setText("\n".join(HEX_keys))
        self.uncomp_text.setText("\n".join(uncomp_keys))
        self.comp_text.setText("\n".join(comp_keys))

    def update_display_random(self, start, end):
        if not self.scanning:
            self.timer.stop()
            return
        rng = random.SystemRandom()
        self.num = rng.randint(start, end)
        self.generate_crypto()
        self.counter += self.power_format

    def update_display_sequence(self, start, end):
        self.num = self.current
        if self.current > int(self.end_edit.text(), 16):
            self.timer.stop()
            self.scanning = False
            return

        update_interval = 1

        while self.num < end and self.scanning:
            self.generate_crypto()
            self.update_poem_per_sec()
            self.current += self.power_format
            self.counter += self.power_format

            self.num += self.power_format

            if self.num % update_interval == 0:
                QApplication.processEvents()

        self.num = end
        self.scanning = False

    def update_display_reverse(self, start, end):
        self.num = self.current
        if self.current < int(self.start_edit.text(), 16):
            self.timer.stop()
            self.scanning = False
            return
        update_interval = 1
        processed_count = 0

        while self.num >= start:
            self.generate_crypto()
            self.update_poem_per_sec()
            self.current -= self.power_format
            self.counter += self.power_format

            self.num -= self.power_format
            processed_count += 1
            if not self.scanning:
                break
            if processed_count >= update_interval:
                processed_count = 0
                QApplication.processEvents()
        self.num = start
        self.scanning = False

    def update_poem_per_sec(self):
        elapsed_time = time.time() - self.start_time

        if elapsed_time == 0:
            poem_per_sec = 0
        else:
            poem_per_sec = self.counter / elapsed_time

        poem_per_sec = round(poem_per_sec, 2)

        total_poem_scanned_text = self.total_poem_scanned_edit.text()
        total_poem_scanned = locale.atoi(total_poem_scanned_text) + self.counter

        total_poem_scanned_formatted = locale.format_string("%d", total_poem_scanned, grouping=True)
        poem_per_sec_formatted = locale.format_string("%.2f", poem_per_sec, grouping=True)

        self.total_poem_scanned_edit.setText(total_poem_scanned_formatted)
        self.poem_per_sec_edit.setText(poem_per_sec_formatted)
        self.start_time = time.time()
        self.counter = 0