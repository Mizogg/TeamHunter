"""
@author: Team Mizogg
"""
import sys
import hashlib
import base58
import os
import struct
import binascii
from Crypto.Hash import RIPEMD160
from PyQt6.QtCore import Qt, QMetaObject, pyqtSlot, Q_ARG
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPlainTextEdit, QPushButton, QComboBox, QFileDialog, QDialog, QLineEdit
sys.path.extend(['images'])
#target_address = "1F654t1HxrZtg7uhcXyZeFvRsyB8HCnBXJ"

ICO_ICON = "images/main/miz.ico"
TITLE_ICON = "images/main/title.png"

class FoundDialog(QDialog):
    def __init__(self, FOUNDTEXT, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Target Found")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.setMinimumSize(640, 600)
        pixmap = QPixmap(f"{TITLE_ICON}")
        title_label = QLabel()
        title_label.setPixmap(pixmap)
        title_label.setFixedSize(pixmap.size())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(title_label)

        title_label = QLabel("!!!! 🎉 🥳CONGRATULATIONS🥳 🎉 !!!!")
        layout.addWidget(title_label)
        informative_label = QLabel("© MIZOGG 2018 - 2024")
        layout.addWidget(informative_label)
        detail_label = QPlainTextEdit(FOUNDTEXT)
        layout.addWidget(detail_label)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

class ConsoleWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.consoleOutput = QPlainTextEdit(self)
        self.consoleOutput.setReadOnly(True)
        self.consoleOutput.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Enter a target wallet address in the provided field. Load a Bitcoin Core wallet file (wallet.dat) using the "Load Wallet File" button or by dragging and dropping the file into the window. The tool will display details about the encrypted keys, public keys, and any matches with the target address.  </span>')
        self.layout.addWidget(self.consoleOutput)

        button_widget = QWidget(self)
        button_layout = QHBoxLayout(button_widget)

        self.clearButton = QPushButton("Clear", self)
        self.selectAllButton = QPushButton("Select All", self)
        self.copyButton = QPushButton("Copy", self)

        button_layout.addWidget(self.clearButton)
        button_layout.addWidget(self.selectAllButton)
        button_layout.addWidget(self.copyButton)

        self.layout.addWidget(button_widget)

        self.clearButton.clicked.connect(self.clear_console)
        self.selectAllButton.clicked.connect(self.select_all)
        self.copyButton.clicked.connect(self.copy_text)

    def set_output(self, output):
        self.consoleOutput.setPlainText(output)

    def append_output(self, output):
        QMetaObject.invokeMethod(self.consoleOutput, "appendPlainText", Qt.ConnectionType.QueuedConnection, Q_ARG(str, output))
        line_count = self.consoleOutput.document().blockCount()

    @pyqtSlot()
    def clear_console(self):
        self.consoleOutput.clear()

    @pyqtSlot()
    def select_all(self):
        self.consoleOutput.selectAll()

    @pyqtSlot()
    def copy_text(self):
        cursor = self.consoleOutput.textCursor()
        selected_text = cursor.selectedText()
        QApplication.clipboard().setText(selected_text)


class WalletFrame(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        #self.target_address = target_address  # Initialize with default target_address

    def init_ui(self):
        self.setWindowTitle("Bitcoin Wallet Analyzer")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.setGeometry(100, 100, 800, 600)
        pixmap = QPixmap(f"{TITLE_ICON}")
        title_label = QLabel()
        title_label.setPixmap(pixmap)
        title_label.setFixedSize(pixmap.size())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        main_layout = QVBoxLayout(self.centralWidget)
        main_layout.addWidget(title_label)
        self.consoleLabel = QLabel("Read Encrypted Key:", self)
        self.consoleWindow = ConsoleWindow(self)
        main_layout.addWidget(self.consoleLabel)
        main_layout.addWidget(self.consoleWindow)

        self.consoleLabel2 = QLabel("Read Wallet:", self)
        self.consoleWindow2 = ConsoleWindow(self)
        main_layout.addWidget(self.consoleLabel2)
        main_layout.addWidget(self.consoleWindow2)

        targetLabel = QLabel("Target Wallet Address :")
        main_layout.addWidget(targetLabel)
        self.targetAddressLineEdit = QLineEdit()
        self.targetAddressLineEdit.setText("1F654t1HxrZtg7uhcXyZeFvRsyB8HCnBXJ")
        self.targetAddressLineEdit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Type in your Wallet address if Known : </span>')
        main_layout.addWidget(self.targetAddressLineEdit)

        # Load Wallet File button
        self.loadButton = QPushButton("Load Wallet File", self)
        self.loadButton.clicked.connect(self.load_wallet_file)
        main_layout.addWidget(self.loadButton)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(".dat"):
                self.read_wallet(file_path)
                self.read_wallet_ckey(file_path)
                break

    def load_wallet_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Wallet Files (*.dat)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                self.read_wallet(file_paths[0])
                self.read_wallet_ckey(file_paths[0])

    @staticmethod
    def sha256(data):
        return hashlib.sha256(data).digest()

    @staticmethod
    def ripemd160(data):
        h = RIPEMD160.new()
        h.update(data)
        return h.digest()

    def pubkeytopubaddress(self, pubkey):
        self.consoleWindow.append_output(f"Public key: {binascii.hexlify(pubkey).decode()}")
        digest = self.sha256(pubkey)
        self.consoleWindow.append_output(f"SHA-256: {binascii.hexlify(digest).decode()}")
        ripemd = self.ripemd160(digest)
        self.consoleWindow.append_output(f"RIPEMD-160: {binascii.hexlify(ripemd).decode()}")
        prefixed_ripemd = b'\x00' + ripemd
        self.consoleWindow.append_output(f"Prefixed RIPEMD-160: {binascii.hexlify(prefixed_ripemd).decode()}")
        checksum = self.sha256(self.sha256(prefixed_ripemd))[:4]
        self.consoleWindow.append_output(f"Checksum: {binascii.hexlify(checksum).decode()}")
        address = prefixed_ripemd + checksum
        encoded_address = base58.b58encode(address).decode()
        self.consoleWindow.append_output(f"Encoded address: {encoded_address}")
        return encoded_address

    def hex_padding(self, s, length):
        return s.zfill(length)

    def read_encrypted_key(self, wallet_filename):
        with open(wallet_filename, "rb") as wallet_file:
            wallet_file.seek(12)
            magic_bytes = wallet_file.read(8)
            if magic_bytes != b"\x62\x31\x05\x00\x09\x00\x00\x00":
                self.consoleWindow.append_output(f"ERROR: file is not a Bitcoin Core wallet, magic bytes: {magic_bytes}")
                return None

        with open(wallet_filename, 'rb') as wallet_file:
            data = wallet_file.read()

        mkey_offset = data.find(b'\x04mkey\x01\x00\x00\x00')
        if mkey_offset == -1:
            self.consoleWindow.append_output("ERROR: Encrypted master key not found in the Bitcoin Core wallet file")
            return None

        mkey_data = data[mkey_offset + 8:mkey_offset + 8 + 49 + 9 + 4 + 4]
        encrypted_master_key, salt, method, iter_count = struct.unpack_from("<49s9sII", mkey_data)

        if method != 0:
            self.consoleWindow.append_output(f"Warning: unexpected Bitcoin Core key derivation method {str(method)}")

        iv = binascii.hexlify(encrypted_master_key[16:32]).decode()
        ct = binascii.hexlify(encrypted_master_key[-16:]).decode()
        iterations = self.hex_padding('{:x}'.format(iter_count), 8)

        target_mkey = binascii.hexlify(encrypted_master_key).decode() + binascii.hexlify(salt).decode() + iterations
        mkey_encrypted = binascii.hexlify(encrypted_master_key).decode()

        self.consoleWindow.append_output(f"Mkey_encrypted: {mkey_encrypted}")
        self.consoleWindow.append_output(f"target mkey  : {target_mkey}")
        self.consoleWindow.append_output(f"ct           : {ct}")
        self.consoleWindow.append_output(f"salt         : {binascii.hexlify(salt).decode()}")
        self.consoleWindow.append_output(f"iv           : {iv}")
        self.consoleWindow.append_output(f"rawi         : {iterations}")
        self.consoleWindow.append_output(f"iter         : {str(int(iterations, 16))}")

    def read_wallet(self, file_path):
        self.read_encrypted_key(file_path)

        with open(file_path, 'rb') as wallet:
            data = wallet.read()

        mkey_offset = data.find(b'mkey')
        if mkey_offset == -1:
            self.consoleWindow.append_output("There is no Master Key in the file")
            return

        mkey_data = data[mkey_offset - 72:mkey_offset - 72 + 48]
        self.consoleWindow.append_output(f"Mkey_encrypted: {self.hex_padding(binascii.hexlify(mkey_data).decode(), 8)}")

        offset = 0

        ckey_offset = data.find(b'ckey', offset)
        if ckey_offset != -1:
            ckey_data = data[ckey_offset - 52:ckey_offset - 52 + 123]
            ckey_encrypted = ckey_data[:48]
            public_key_length = ckey_data[56]
            public_key = ckey_data[57:57 + public_key_length]

            self.consoleWindow.append_output(f"encrypted ckey: {self.hex_padding(binascii.hexlify(ckey_encrypted).decode(), 8)}")
            self.consoleWindow.append_output(f"public key    : {self.hex_padding(binascii.hexlify(public_key).decode(), 8)}")
            self.consoleWindow.append_output(f"public address: {self.pubkeytopubaddress(public_key)}")

    def tohex(self, data):
        return data.hex()

    def pubkeytopubaddress_ckey(self, pubkey):
        digest = self.sha256(pubkey)
        ripemd = self.ripemd160(digest)
        prefixed_ripemd = b'\x00' + ripemd
        checksum = self.sha256(self.sha256(prefixed_ripemd))[:4]
        address = prefixed_ripemd + checksum
        encoded_address = base58.b58encode(address).decode()
        return encoded_address, address

    def read_wallet_ckey(self, file_path):
        target_address = self.targetAddressLineEdit.text()

        with open(file_path, 'rb') as wallet:
            data = wallet.read()

        mkey_offset = data.find(b'mkey')
        if mkey_offset == -1:
            print("There is no Master Key in the file")
            return

        mkey_data = data[mkey_offset - 72:mkey_offset - 72 + 48]
        output_lines = []
        output_lines.append(f"Mkey_encrypted: {self.tohex(mkey_data)}")

        ckey_count = 0
        offset = 0

        while True:
            ckey_offset = data.find(b'ckey', offset)
            if ckey_offset == -1:
                break

            ckey_data = data[ckey_offset - 52:ckey_offset - 52 + 123]
            ckey_encrypted = ckey_data[:48]
            public_key_length = ckey_data[56]
            public_key = ckey_data[57:57 + public_key_length]

            output_lines.append(f"encrypted ckey: {self.tohex(ckey_encrypted)}")
            output_lines.append(f"public key    : {self.tohex(public_key)}")

            encoded_address, raw_address = self.pubkeytopubaddress_ckey(public_key)
            output_lines.append(f"public address: {encoded_address}\n")

            if encoded_address == target_address:
                found_text = (
                    f"Match found for address {target_address}!\n"
                    f"Encrypted ckey: {self.tohex(ckey_encrypted)}\n"
                    f"Public key    : {self.tohex(public_key)}\n"
                    f"Raw address   : {self.tohex(raw_address)}\n"
                    f"Mkey_encrypted: {self.tohex(mkey_data)}\n"
                )
                self.consoleWindow2.append_output(found_text)
                found_dialog = FoundDialog(found_text, self)
                found_dialog.exec()

            ckey_count += 1
            offset = ckey_offset + 4

        output_lines.append(f"{ckey_count} ckeys were found")
        for line in output_lines:
            self.consoleWindow2.append_output(line)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WalletFrame()
    window.show()
    sys.exit(app.exec())
