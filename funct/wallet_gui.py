import os
import sys
import re
import subprocess
import signal
import platform
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from console_gui import ConsoleWindow
from command_thread import CommandThread

kmre = re.compile(b'\x07keymeta!([\x02|\x03][\x00-\xFF].{32})')
secre = re.compile(b'(\x01\x01\x04[\x10-\x20].{34})')
ICO_ICON = "webfiles/css/images/main/miz.ico"
TITLE_ICON = "webfiles/css/images/main/title.png"

import hashlib
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend  # Import default_backend

def decrypt(data: bytes, password: str) -> str:
    if not password:
        raise ValueError("Password cannot be empty.")
    key = hashlib.sha256(password.encode()).digest()

    decrypted_data = decrypt_with_key(data, key)

    return decrypted_data

def decrypt_with_key(data: bytes, key: bytes) -> bytes:
    # Ensure that the IV size matches the block size (16 bytes for AES)
    iv = b'1234567890123456'  # Replace with your 16-byte IV

    decryption_algorithm = algorithms.AES(key)
    mode = modes.CFB(iv)

    decryptor = Cipher(decryption_algorithm, mode, backend=default_backend()).decryptor()
    decrypted_data = decryptor.update(data) + decryptor.finalize()

    return decrypted_data

def extractPrivKeys(filebinary):
    secset=set()
    for match in secre.findall(filebinary):
        key=match.hex()
        numtoread=(int.from_bytes(bytes.fromhex(str(key[6:8])),'big'))
        keyexpo=bytes.fromhex(key[8:][:numtoread*2])
        secint=(int.from_bytes(keyexpo,'big'))
        secset.add(secint)
    return(secset)

def extractKeyMetas(filebinary):
    kmetaset=set()
    for match in kmre.findall(filebinary):
        key=match.hex()
        kmetaset.add(key)
    return(kmetaset)

class WalletFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wallet Recovery")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.setMinimumSize(640, 440)
        self.scanning = False
        self.timer = QTimer(self)
        self.commandThread = None

        main_layout = QVBoxLayout()
        outputFile_config = self.create_outputFileGroupBox()
        main_layout.addWidget(outputFile_config)

        # Add a password input field
        self.passwordLineEdit = QLineEdit(self)
        self.passwordLineEdit.setPlaceholderText("Enter Password")
        main_layout.addWidget(self.passwordLineEdit)

        buttonLayout = self.create_button_layout([
            ("Analyze Wallet", "CHECK", self.analyze_wallet, "#1E1E1E", "#5D6062"),
            ("Dump Wallet", "Dump Wallet Information", self.dump_start, "#1E1E1E", "#5D6062"),
            ("Start Recovery", "Start Recovery", self.recovery_start, "#E7481F", '#A13316'),
            ("Stop ALL", "Stop Wallet and All Running programs", self.recovery_stop, "#1E1E1E", "#5D6062"),
        ])

        main_layout.addLayout(buttonLayout)

        self.consoleWindow = ConsoleWindow(self)
        main_layout.addWidget(self.consoleWindow)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_button(self, label, tooltip, click_handler, background_color="#E7481F", hover_color="#E7481F"):
        button = QPushButton(label, self)
        button.setToolTip(f'<span style="font-size: 12pt; font-weight; bold; color: black;"> {tooltip} </span>')
        button.setStyleSheet(
            f"QPushButton {{ font-size: 16pt; background-color: {background_color}; color: white; }}"
            f"QPushButton:hover {{ font-size: 16pt; background-color: {hover_color}; color: white; }}"
        )
        button.clicked.connect(click_handler)
        return button

    def create_button_layout(self, buttons):
        buttonLayout = QHBoxLayout()
        for label, tooltip, click_handler, background_color, *hover_color in buttons:
            hover_color = hover_color[0] if hover_color else background_color
            button = self.create_button(label, tooltip, click_handler, background_color, hover_color)
            buttonLayout.addWidget(button)
        return buttonLayout

    def create_outputFileGroupBox(self):
        outputFileGroupBox = QGroupBox(self)
        outputFileGroupBox.setTitle("File Configuration")
        outputFileGroupBox.setStyleSheet("QGroupBox { border: 3px solid #E7481F; padding: 5px; }")
        outputFileLayout = QHBoxLayout(outputFileGroupBox)
        self.inputFileLabel = QLabel("Input File:", self)
        outputFileLayout.addWidget(self.inputFileLabel)
        self.inputFileLineEdit = QLineEdit("bitcoincore-wallet.dat", self)
        self.inputFileLineEdit.setPlaceholderText('Click browse to find your Wallet File')
        self.inputFileLineEdit.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Type the Name of Wallet File or Browse location </span>')
        outputFileLayout.addWidget(self.inputFileLineEdit)
        self.inputFileButton = QPushButton("Browse", self)
        self.inputFileButton.setStyleSheet("color: #E7481F;")
        self.inputFileButton.clicked.connect(self.browse_input_file)
        self.inputFileButton.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Type the Name of Wallet File or Browse location </span>')
        outputFileLayout.addWidget(self.inputFileButton)

        self.dumpFileLineEdit = QLineEdit("dump.txt", self)
        self.dumpFileLineEdit.setPlaceholderText('Dump Wallet File')
        self.dumpFileLineEdit.setToolTip('Specify the name to Dump Wallet Information')
        outputFileLayout.addWidget(self.dumpFileLineEdit)

        return outputFileGroupBox

    def browse_input_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("wallet Files (*.dat);;All Files (*.*)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            file_name = os.path.basename(file_path)
            self.inputFileLineEdit.setText(file_name)


    def analyze_wallet(self):
        wallet_file_path = self.inputFileLineEdit.text()
        if not wallet_file_path:
            self.consoleWindow.append_output("⚠️ Please select a wallet file.")
            return
        try:
            walletbinary = open(wallet_file_path, 'rb').read()
            keymetas = extractKeyMetas(walletbinary)
            secrets = extractPrivKeys(walletbinary)
            wallet_data = f'There are potentially {len(keymetas)} Keymetas and {len(secrets)} Private Keys in this wallet'
            self.consoleWindow.append_output(wallet_data)

        except FileNotFoundError as e:
            self.consoleWindow.append_output(f"Error: {e}")
        except ValueError as e:
            self.consoleWindow.append_output(f"Error: {e}")
        except Exception as e:
            self.consoleWindow.append_output(f"An error occurred: {str(e)}")


    def recovery_start(self):
        command = f'{sys.executable} '
        error_message = "⚠️ Please select a wallet file."
        #self.execute_command(command, error_message)

    def dump_start(self):
        wallet_file_path = self.inputFileLineEdit.text()
        password = self.passwordLineEdit.text()
        if not wallet_file_path:
            self.consoleWindow.append_output("⚠️ Please select a wallet file.")
            return

        if not password:
            self.consoleWindow.append_output("⚠️ Please enter a password.")
            return

        try:
            walletbinary = open(wallet_file_path, 'rb').read()
            decrypted_contents = decrypt(walletbinary, password)
            dec_data = f"Decrypted contents of '{wallet_file_path}': {decrypted_contents}"
            self.consoleWindow.append_output(dec_data)

        except FileNotFoundError as e:
            self.consoleWindow.append_output(f"Error: {e}")
        except ValueError as e:
            self.consoleWindow.append_output(f"Error: {e}")
        except Exception as e:
            self.consoleWindow.append_output(f"An error occurred: {str(e)}")



    @pyqtSlot()
    def execute_command(self, command, error_message):
        if not command:
            self.consoleWindow.append_output(error_message)
            return
        if self.scanning:
            return

        self.scanning = True

        if self.commandThread and self.commandThread.isRunning():
            self.commandThread.terminate()

        self.commandThread = CommandThread(command)
        self.commandThread.commandOutput.connect(self.consoleWindow.append_output)
        self.commandThread.commandFinished.connect(self.command_finished)
        self.commandThread.start()
        self.timer.start(100)

    @pyqtSlot(int)
    def command_finished(self, returncode):
        self.timer.stop()
        self.scanning = False
        if returncode == 0:
            finish_scan = "Command execution finished successfully"
            self.consoleWindow.append_output(finish_scan)
        elif returncode == 'Closed':
            finish_scan = "Process has been stopped by the user"
            self.consoleWindow.append_output(finish_scan)
        else:
            error_scan = "Command execution failed"
            self.consoleWindow.append_output(error_scan)

    def recovery_stop(self):
        if self.commandThread and self.commandThread.isRunning():
            if platform.system() == "Windows":
                subprocess.Popen(["taskkill", "/F", "/T", "/PID", str(self.commandThread.process.pid)])
            else:
                os.killpg(os.getpgid(self.commandThread.process.pid), signal.SIGTERM)
            
            self.timer.stop()
            self.scanning = False
            returncode = 'Closed'
            self.command_finished(returncode)

    def closeEvent(self, event):
        self.recovery_stop()
        event.accept()

def main():
    app = QApplication([])
    window = WalletFrame()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()