"""
@author: Team Mizogg
"""
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import base58, binascii
import sys
sys.path.append('libs')
import libs
from libs import secp256k1 as ice
from libs import team_brain
from libs import team_word

ICO_ICON = "webfiles/css/images/main/miz.ico"
TITLE_ICON = "webfiles/css/images/main/title.png"

class ConversionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Conversion Tools ")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.setMinimumSize(740, 440)
        pixmap = QPixmap(f"{TITLE_ICON}")
        # Create a QLabel and set the pixmap as its content
        title_label = QLabel()
        title_label.setPixmap(pixmap)
        title_label.setFixedSize(pixmap.size())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hex_layout = QHBoxLayout()
        self.hex_label = QLabel("HEX TO DEC :")
        self.hex_input_edit = QLineEdit()
        self.hex_button = QPushButton("Check Hex")

        hex_layout.addWidget(self.hex_label)
        hex_layout.addWidget(self.hex_input_edit)
        hex_layout.addWidget(self.hex_button)

        dec_layout = QHBoxLayout()
        self.dec_label = QLabel("DEC TO HEX :")
        self.dec_input_edit = QLineEdit()
        self.dec_button = QPushButton("Check Dec")
        
        dec_layout.addWidget(self.dec_label)
        dec_layout.addWidget(self.dec_input_edit)
        dec_layout.addWidget(self.dec_button)

        wif_layout = QHBoxLayout()
        self.wif_label = QLabel("WIF :")
        self.wif_input_edit = QLineEdit()
        self.wif_button = QPushButton("Check WIF")

        wif_layout.addWidget(self.wif_label)
        wif_layout.addWidget(self.wif_input_edit)
        wif_layout.addWidget(self.wif_button)
        
        brain_layout = QHBoxLayout()
        self.brain_label = QLabel("Brain words :")
        self.brain_input_edit = QLineEdit()
        self.brain_button = QPushButton("Check Brain")
        
        brain_layout.addWidget(self.brain_label)
        brain_layout.addWidget(self.brain_input_edit)
        brain_layout.addWidget(self.brain_button)

        mnm_layout = QHBoxLayout()
        self.mnm_label = QLabel("Menmonics :")
        self.mnm_input_edit = QLineEdit()
        self.mnm_button = QPushButton("Check Words")
        
        mnm_layout.addWidget(self.mnm_label)
        mnm_layout.addWidget(self.mnm_input_edit)
        mnm_layout.addWidget(self.mnm_button)

        self.cancel_button = QPushButton("Cancel")
        
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addLayout(hex_layout)
        layout.addLayout(dec_layout)
        layout.addLayout(wif_layout)
        layout.addLayout(brain_layout)
        layout.addLayout(mnm_layout)
        layout.addWidget(self.cancel_button)

        self.output_label = QPlainTextEdit()
        self.output_label.setReadOnly(True)
        self.output_label.setFont(QFont("Courier"))
        layout.addWidget(self.output_label)
        self.setLayout(layout)
        
        self.hex_button.clicked.connect(self.to_dec)
        self.dec_button.clicked.connect(self.to_hex)
        self.wif_button.clicked.connect(self.wif_in)
        self.brain_button.clicked.connect(self.brain_in)
        self.mnm_button.clicked.connect(self.word_in)
        self.cancel_button.clicked.connect(self.reject)

    def to_dec(self):
        num = self.hex_input_edit.text()
        try:
            dec_value = str(int(num, 16))
            caddr = ice.privatekey_to_address(0, True, int(dec_value))
            uaddr = ice.privatekey_to_address(0, False, int(dec_value))
            wifc = ice.btc_pvk_to_wif(num)
            wifu = ice.btc_pvk_to_wif(num, False)
            out_info = (f'\n HEX Input: {num} \n Private Key In Dec : {dec_value} \nBTC Address Compressed: {caddr} \nWIF Compressed: {wifc} \nBTC Address Uncompressed: {uaddr} \nWIF Uncompressed: {wifu}')
            self.output_label.appendPlainText(out_info)
        except ValueError:
            self.output_label.appendPlainText("Invalid input. Please enter a valid hexadecimal.")

    def to_hex(self):
        num = self.dec_input_edit.text()
        try:
            dec_value = int(num)
            caddr = ice.privatekey_to_address(0, True, dec_value)
            uaddr = ice.privatekey_to_address(0, False, dec_value)
            
            hex_value = hex(dec_value).upper()  # Convert to hexadecimal and make it uppercase
            wifc = ice.btc_pvk_to_wif(hex_value)
            wifu = ice.btc_pvk_to_wif(hex_value, False)
            out_info = (f'\n Dec Input: {num} \n Private Key In Hec : {hex_value} \nBTC Address Compressed: {caddr} \nWIF Compressed: {wifc} \nBTC Address Uncompressed: {uaddr} \nWIF Uncompressed: {wifu}')
            self.output_label.appendPlainText(out_info)
        except ValueError:
            self.output_label.appendPlainText("Invalid input. Please enter a valid decimal number.")

    def wif_in(self):
        wif = self.wif_input_edit.text()
        try:
            if wif.startswith('5H') or wif.startswith('5J') or wif.startswith('5K'):
                first_encode = base58.b58decode(wif)
                private_key_full = binascii.hexlify(first_encode)
                private_key = private_key_full[2:-8]
                private_key_hex = private_key.decode("utf-8")
                dec = int(private_key_hex, 16)
                uaddr = ice.privatekey_to_address(0, False, dec)
                out_info = (f'\n WIF Input: {wif} \n Private Key In Hec : {private_key_hex} \n Private Key In Dec : {dec} \n Bitcoin Uncompressed Adress : {uaddr}')
                self.output_label.appendPlainText(out_info)
            elif wif.startswith('K') or wif.startswith('L'):
                first_encode = base58.b58decode(wif)
                private_key_full = binascii.hexlify(first_encode)
                private_key = private_key_full[2:-8]
                private_key_hex = private_key.decode("utf-8")
                dec = int(private_key_hex[0:64], 16)
                caddr = ice.privatekey_to_address(0, True, dec)
                out_info = (f'\n WIF Input: {wif} \n Private Key In Hec : {private_key_hex} \n Private Key In Dec : {dec} \n Bitcoin Compressed Adress : {caddr}')
                self.output_label.appendPlainText(out_info)
        except ValueError:
            self.output_label.appendPlainText("Invalid input. Please enter a valid WIF Wallet.")

    def brain_in(self):
        passphrase = self.brain_input_edit.text()
        try:
            wallet = team_brain.BrainWallet()
            private_key, caddr = wallet.generate_address_from_passphrase(passphrase)
            brainvartext = (f'\n BrainWallet: {passphrase} \n Private Key In HEX : {private_key} \n Bitcoin Adress : {caddr}')
            self.output_label.appendPlainText(brainvartext)
        except ValueError:
            self.output_label.appendPlainText("Invalid input. Please enter a valid Brain Wallet.")

    def word_in(self):
        mnem = self.mnm_input_edit.text()
        try:
            seed = team_word.mnem_to_seed(mnem)
            for r in range (1,3):
                pvk = team_word.bip39seed_to_private_key(seed, r)
                pvk2 = team_word.bip39seed_to_private_key2(seed, r)
                pvk3 = team_word.bip39seed_to_private_key3(seed, r)
                dec = (int.from_bytes(pvk, "big"))
                HEX = "%064x" % dec
                dec2 = (int.from_bytes(pvk2, "big"))
                HEX2 = "%064x" % dec2
                dec3 = (int.from_bytes(pvk3, "big"))
                HEX3 = "%064x" % dec3
                cpath = f"m/44'/0'/0'/0/{r}"
                ppath = f"m/49'/0'/0'/0/{r}"
                bpath = f"m/84'/0'/0'/0/{r}"
                caddr = ice.privatekey_to_address(0, True, (int.from_bytes(pvk, "big")))
                p2sh = ice.privatekey_to_address(1, True, (int.from_bytes(pvk2, "big")))
                bech32 = ice.privatekey_to_address(2, True, (int.from_bytes(pvk3, "big")))
                wordvartext = (f'\n Bitcoin {cpath} :  {caddr} \n Dec : {dec} \n   Hex : {HEX}  \n Bitcoin {ppath} :  {p2sh}\n Dec : {dec2} \n  Hex : {HEX2} \n Bitcoin {bpath} : {bech32}\n  Dec : {dec3} \n  Hex : {HEX3} ')
                self.output_label.appendPlainText(wordvartext)
        except ValueError:
            self.output_label.appendPlainText("Invalid input. Please enter a valid Menmonics.")