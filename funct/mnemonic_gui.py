"""
@author: Team Mizogg
"""
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import os
import subprocess
import platform
import multiprocessing
import signal
from console_gui import ConsoleWindow
from command_thread import CommandThread

class MnemonicFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cpu_count = multiprocessing.cpu_count()
        self.scanning = False
        self.timer = QTimer(self)
        self.commandThread = None
        
        main_layout = QVBoxLayout()

        mnemonic_config = self.create_mnemonic_GroupBox()
        main_layout.addWidget(mnemonic_config)
        
        outputFile_config = self.create_outputFileGroupBox()
        main_layout.addWidget(outputFile_config)

        buttonLayout = QHBoxLayout()
        start_button = self.create_start_button()
        stop_button = self.create_stop_button()

        buttonLayout.addWidget(start_button)
        buttonLayout.addWidget(stop_button)

        main_layout.addLayout(buttonLayout)

        self.consoleWindow = ConsoleWindow(self)
        main_layout.addWidget(self.consoleWindow)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_stop_button(self):
        stopButton = QPushButton("Stop ALL", self)
        stopButton.clicked.connect(self.stop_mnemonic)
        stopButton.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Stop Mnemonic and All Running programs </span>')
        stopButton.setStyleSheet(
            "QPushButton { font-size: 16pt; background-color: #1E1E1E; color: white; }"
            "QPushButton:hover { font-size: 16pt; background-color: #5D6062; color: white; }"
        )
        return stopButton

    def create_start_button(self):
        StartButton = QPushButton("Start Mnemonic", self)
        StartButton.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Start Mnemonic </span>')
        StartButton.setStyleSheet(
                "QPushButton { font-size: 16pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 16pt; background-color: #A13316; color: white; }"
            )
        StartButton.clicked.connect(self.run_mnemonic)
        return StartButton

    def create_outputFileGroupBox(self):
        outputFileGroupBox = QGroupBox(self)
        outputFileGroupBox.setTitle("File Configuration Input and Output")
        outputFileGroupBox.setStyleSheet("QGroupBox { border: 3px solid #E7481F; padding: 5px; }")
        outputFileLayout = QHBoxLayout(outputFileGroupBox)
        self.inputFileLabel = QLabel("Input File:", self)
        outputFileLayout.addWidget(self.inputFileLabel)
        self.inputFileLineEdit = QLineEdit("h160.blf", self)
        self.inputFileLineEdit.setPlaceholderText('Click browse to find your BTC database h160.blf,h161.blf')
        self.inputFileLineEdit.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Type the Name of database blf file or Browse location h160.blf,h161.blf </span>')
        outputFileLayout.addWidget(self.inputFileLineEdit)
        self.inputFileButton = QPushButton("Browse", self)
        self.inputFileButton.setStyleSheet("color: #E7481F;")
        self.inputFileButton.clicked.connect(self.browse_input_file)
        self.inputFileButton.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Type the Name of database txt file or Browse location </span>')
        outputFileLayout.addWidget(self.inputFileButton)
        self.found_progButton = QPushButton("🔥 Check if Found 🔥")
        self.found_progButton.clicked.connect(self.found_prog)
        self.found_progButton.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Click Here to See if your a Winner </span>')
        outputFileLayout.addWidget(self.found_progButton)
        return outputFileGroupBox

    def create_mnemonic_GroupBox(self):
        self.keyhuntLayout = QVBoxLayout()
        threadGroupBox = QGroupBox(self)
        threadGroupBox.setTitle("Mnemonic Hunt Configuration")
        threadGroupBox.setStyleSheet("QGroupBox { border: 3px solid #E7481F; padding: 15px; }")
        self.row1Layout = QHBoxLayout()
        self.threadLabel = QLabel("Number of CPUs:", self)
        self.row1Layout.addWidget(self.threadLabel)
        self.threadComboBox_key = QComboBox()
        for i in range(1, self.cpu_count + 1):
            self.threadComboBox_key.addItem(str(i))
        self.threadComboBox_key.setCurrentIndex(2)
        self.threadComboBox_key.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Pick Your ammount to CPUs to start scaning with</span>')
        self.row1Layout.setStretchFactor(self.threadComboBox_key, 1)
        self.row1Layout.addWidget(self.threadComboBox_key)

        self.incrementalEntropyLabel = QLabel("Incremental Entropy (hex):", self)
        self.incrementalEntropyLineEdit = QLineEdit(self)
        self.incrementalEntropyLineEdit.setPlaceholderText('0000000000000000000000000000000')
        self.incrementalEntropyLineEdit.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Incremental entropy search, in order from specified hex number (Length - 8 , 16, 24 ,32 ,40 ,48 ,56 ,64) HEX characters </span>')
        self.stepLabel = QLabel("Step:", self)
        self.stepLineEdit = QLineEdit(self)
        self.stepLineEdit.setPlaceholderText('2')
        self.stepLineEdit.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Specify step to add in -entropy mode </span>')
        self.privateKeyIncrementLabel = QLabel("Private Key Increment:", self)
        self.privateKeyIncrementLineEdit = QLineEdit(self)
        self.privateKeyIncrementLineEdit.setPlaceholderText('2')
        self.privateKeyIncrementLineEdit.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Number of keys for incremental search (PrivateKeys) (+- value to the keys obtained from the mnemonic) </span>')
        self.row1Layout.addWidget(self.incrementalEntropyLabel)
        self.row1Layout.addWidget(self.incrementalEntropyLineEdit)
        self.row1Layout.addWidget(self.stepLabel)
        self.row1Layout.addWidget(self.stepLineEdit)
        self.row1Layout.addWidget(self.privateKeyIncrementLabel)
        self.row1Layout.addWidget(self.privateKeyIncrementLineEdit)

        radio_button_layout = QHBoxLayout()
        modeLabel = QLabel('Mode:')
        radio_button_layout.addWidget(modeLabel)
        self.modeComboBox = QComboBox()
        self.modeComboBox.addItems([
            'BTC+ETH', 'BTC', 'ETH', 'BTC (HASH160)', 'Public keys', 'Private keys (generator for brainflayer)',
            'Valid Mnemonic Generator', 'Bitcoin Cash', 'Bitcoin Diamond', 'Bitcoin SV', 'ILCoin', 'Tether',
            'CryptoVerificationCoin', 'Litecoin Cash', 'Zcash', 'DigiByte', 'Dogecoin', 'PIVX', 'Verge', 'Horizen',
            'Einsteinium', 'Groestlcoin', 'Bitcoin Gold', 'Litecoin', 'MonaCoin', 'ImageCoin', 'NavCoin', 'Neblio',
            'Axe', 'Peercoin', 'Particle', 'Qtum', 'Komodo', 'Ravencoin', 'Reddcoin', 'SafeInsure', 'SmartCash',
            'Stratis', 'Syscoin', 'Vertcoin', 'Viacoin', 'BeetleCoin', 'Dash', 'Xenios', 'Zcoin'
        ])
        self.modeComboBox.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;">Select the Crypto mode for the mnemonic hunt</span>')
        self.modeComboBox.setCurrentIndex(1)
        radio_button_layout.addWidget(self.modeComboBox)


        wordsLabel = QLabel('Number of Words:', self)
        radio_button_layout.addWidget(wordsLabel)
        self.wordsComboBox = QComboBox()
        self.wordsComboBox.addItems(['3', '6', '9', '12', '15', '18', '21', '24'])
        self.wordsComboBox.setCurrentIndex(3)
        self.wordsComboBox.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;">Select the number of words for the mnemonic</span>')
        radio_button_layout.addWidget(self.wordsComboBox)

        self.languageLabel = QLabel("Language:", self)
        self.languageComboBox = QComboBox(self)
        self.languageComboBox.addItems(['EN', 'CT', 'CS', 'KO', 'JA', 'IT', 'FR', 'SP'])
        self.languageComboBox.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Pick Language for Generation </span>')
        radio_button_layout.addWidget(self.languageLabel)
        radio_button_layout.addWidget(self.languageComboBox)

        div_button_layout = QHBoxLayout()
        self.derivationDepthLabel = QLabel("Derivation Depth:", self)
        self.derivationDepthLineEdit = QLineEdit('1',self)
        self.derivationDepthLineEdit.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> 1-1000 “derivation path.” Simply put, a derivation path defines a consistent method for generating the same set of accounts and wallets for a given private key </span>')
        div_button_layout.addWidget(self.derivationDepthLabel)
        div_button_layout.addWidget(self.derivationDepthLineEdit)

        derivationPathsLabel = QLabel('Derivation Paths:', self)
        div_button_layout.addWidget(derivationPathsLabel)
        self.derivationPathsLineEdit = QLineEdit(self)
        self.derivationPathsLineEdit.setPlaceholderText('paths.txt')
        self.derivationPathsLineEdit.setToolTip('<span style="font-size: 12pt; font-weight; bold; color: black;">Specify derivation paths to load from file make sure it is stored in the input folder </span>')
        div_button_layout.addWidget(self.derivationPathsLineEdit)

        self.debugCheckBox = QCheckBox("Debug Mode", self)
        self.debugCheckBox.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;">Enable debug mode for lower speed</span>')
        div_button_layout.addWidget(self.debugCheckBox)


        self.keyhuntLayout.addLayout(self.row1Layout)
        self.keyhuntLayout.addLayout(radio_button_layout)
        self.keyhuntLayout.addLayout(div_button_layout)
        threadGroupBox.setLayout(self.keyhuntLayout)
        return threadGroupBox
    
    def read_and_display_file(self, file_path, success_message, error_message):
        try:
            with open(file_path, 'r') as file:
                output_from_text = file.read()
                self.consoleWindow.append_output(success_message)
                self.consoleWindow.append_output(output_from_text)
        except FileNotFoundError:
            self.consoleWindow.append_output(f"⚠️ {error_message} File not found. Please check the file path.")
        except Exception as e:
            self.consoleWindow.append_output(f"An error occurred: {str(e)}")

    def found_prog(self):
        self.read_and_display_file('found.txt', "Mnemonic GUI File found. Check of Winners 😀 .", "No Winners Yet 😞")

    def browse_input_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Bloom Files (*.blf);;Text Files (*.txt);;All Files (*.*)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            file_name = os.path.basename(file_path)
            self.inputFileLineEdit.setText(file_name)

    def run_mnemonic(self):
        command = []
        command = self.construct_command_key()
        self.execute_command('"' + '" "'.join(command) + '"')

    def construct_command_key(self):
        mode = self.modeComboBox.currentIndex()
        thread_count_key = int(self.threadComboBox_key.currentText())
        number_of_words = self.wordsComboBox.currentText()

        self.thread_count_key = thread_count_key
        base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Mnemonic", "C#-Mnemonic-hash160")

        command = [base_path, "-m", str(mode), "-t", str(self.thread_count_key)]

        command.extend(["-w", number_of_words])
        if self.derivationDepthLineEdit.text():
            command.extend(["-d", self.derivationDepthLineEdit.text()])
        if self.incrementalEntropyLineEdit.text():
            command.extend(["-entropy", self.incrementalEntropyLineEdit.text()])
        if self.stepLineEdit.text():
            command.extend(["-step", self.stepLineEdit.text()])
        if self.privateKeyIncrementLineEdit.text():
            command.extend(["-n", self.privateKeyIncrementLineEdit.text()])
        file = self.inputFileLineEdit.text().strip()

        if self.languageComboBox.currentIndex() > 0:
            command.extend(["-lang", self.languageComboBox.currentText()])

        if self.derivationPathsLineEdit.text():
            div_file = self.derivationPathsLineEdit.text()
            div_file_relative_path = f"input/{div_file}"
            command.extend(["-PATH", div_file_relative_path])

        if file:
            input_files = file.split(',')  # Split the comma-separated list into individual files
            for input_file in input_files:
                input_file_relative_path = ["input", input_file.strip()]  # Trim whitespace around file names
                input_file_path = os.path.join(*input_file_relative_path)
                command.extend(["-b", input_file_path])

            
        if self.debugCheckBox.isChecked():
            command.extend(["-debug"])
        return command

    @pyqtSlot()
    def execute_command(self, command):
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

    def stop_mnemonic(self):
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
        self.stop_mnemonic()
        event.accept()

def main():
    app = QApplication([])
    window = MnemonicFrame()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()