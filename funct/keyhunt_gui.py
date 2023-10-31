"""
@author: Team Mizogg
"""
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import os
import subprocess
import signal
import platform
import multiprocessing
from console_gui import ConsoleWindow
from command_thread import CommandThread

class KeyHuntFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cpu_count = multiprocessing.cpu_count()
        self.scanning = False
        self.timer = QTimer(self)
        self.commandThread = None
        
        main_layout = QVBoxLayout()

        bitcrack_config = self.create_threadGroupBox()
        main_layout.addWidget(bitcrack_config)
        
        Keysapce_config = self.create_keyspaceGroupBox()
        main_layout.addWidget(Keysapce_config)

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

    def create_keyspaceGroupBox(self):
        keyspaceGroupBox = QGroupBox(self)
        keyspaceGroupBox.setTitle("Key Space Configuration")
        keyspaceGroupBox.setStyleSheet("QGroupBox { border: 3px solid #E7481F; padding: 5px; }")
        keyspaceMainLayout = QVBoxLayout(keyspaceGroupBox)
        keyspaceLayout = QHBoxLayout()
        keyspaceLabel = QLabel("Key Space:")
        keyspaceLayout.addWidget(keyspaceLabel)
        self.keyspaceLineEdit = QLineEdit("20000000000000000:3ffffffffffffffff")
        self.keyspaceLineEdit.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Type in your own HEX Range separated with : </span>')
        keyspaceLayout.addWidget(self.keyspaceLineEdit)
        keyspaceMainLayout.addLayout(keyspaceLayout)
        keyspacerange_layout = QHBoxLayout()
        keyspace_slider = QSlider(Qt.Orientation.Horizontal)
        keyspace_slider.setMinimum(1)
        keyspace_slider.setMaximum(256)
        keyspace_slider.setValue(66)
        keyspace_slider.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Drag Left to Right to Adjust Range </span>')
        slider_value_display = QLabel(keyspaceGroupBox)
        keyspacerange_layout.addWidget(keyspace_slider)
        keyspacerange_layout.addWidget(slider_value_display)
        keyspaceMainLayout.addLayout(keyspacerange_layout)

        keyspace_slider.valueChanged.connect(lambda value, k=self.keyspaceLineEdit, s=slider_value_display: self.update_keyspace_range(value, k, s))
        return keyspaceGroupBox


    def update_keyspace_range(self, value, keyspaceLineEdit, slider_value_display):
        if value == 256:
            start_range = hex(2**(value - 1))[2:]
            end_range = "fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141"
            self.keyspaceLineEdit.setText(f"{start_range}:{end_range}")
            slider_value_display.setText(str(value))
        else:
            start_range = hex(2**(value - 1))[2:]
            end_range = hex(2**value - 1)[2:]
            self.keyspaceLineEdit.setText(f"{start_range}:{end_range}")
            slider_value_display.setText(str(value))

    def create_stop_button(self):
        stopButton = QPushButton("Stop ALL", self)
        stopButton.clicked.connect(self.stop_hunt)
        stopButton.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Stop Keyhunt and All Running programs </span>')
        stopButton.setStyleSheet(
            "QPushButton { font-size: 16pt; background-color: #1E1E1E; color: white; }"
            "QPushButton:hover { font-size: 16pt; background-color: #5D6062; color: white; }"
        )
        return stopButton

    def create_start_button(self):
        StartButton = QPushButton("Start KeyHunt", self)
        StartButton.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Start Keyhunt </span>')
        StartButton.setStyleSheet(
                "QPushButton { font-size: 16pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 16pt; background-color: #A13316; color: white; }"
            )
        StartButton.clicked.connect(self.run_keyhunt)
        return StartButton

    def create_outputFileGroupBox(self):
        outputFileGroupBox = QGroupBox(self)
        outputFileGroupBox.setTitle("File Configuration and Look Type (Compressed/Uncompressed)")
        outputFileGroupBox.setStyleSheet("QGroupBox { border: 3px solid #E7481F; padding: 5px; }")
        outputFileLayout = QHBoxLayout(outputFileGroupBox)
        self.lookLabel = QLabel("Look Type:", self)
        outputFileLayout.addWidget(self.lookLabel)
        self.lookComboBox = QComboBox()
        self.lookComboBox.addItem("compress")
        self.lookComboBox.addItem("uncompress")
        self.lookComboBox.addItem("both")
        self.lookComboBox.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Search for compressed keys (default). Can be used with also search uncompressed keys  </span>')
        outputFileLayout.addWidget(self.lookComboBox)
        self.inputFileLabel = QLabel("Input File:", self)
        outputFileLayout.addWidget(self.inputFileLabel)
        self.inputFileLineEdit = QLineEdit("btc.txt", self)
        self.inputFileLineEdit.setPlaceholderText('Click browse to find your BTC database')
        self.inputFileLineEdit.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Type the Name of database txt file or Browse location </span>')
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

    def create_threadGroupBox(self):
        self.keyhuntLayout = QVBoxLayout()
        threadGroupBox = QGroupBox(self)
        threadGroupBox.setTitle("Key Hunt Configuration")
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
        self.cryptoLabel = QLabel("Crypto:", self)
        self.row1Layout.addWidget(self.cryptoLabel)
        self.cryptoComboBox = QComboBox()
        self.cryptoComboBox.addItem("btc")
        self.cryptoComboBox.addItem("eth")
        self.cryptoComboBox.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Crypto Scanning Type BTC or ETH (default BTC)</span>')
        self.row1Layout.addWidget(self.cryptoComboBox)
        self.modeLabel = QLabel("Mode:", self)
        self.row1Layout.addWidget(self.modeLabel)
        self.modeComboBox = QComboBox()
        self.modeComboBox.addItem("address")
        self.modeComboBox.addItem("rmd160")
        self.modeComboBox.addItem("xpoint")
        self.modeComboBox.addItem("bsgs")
        self.modeComboBox.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Keyhunt can work in diferent ways at different speeds. The current availables modes are:</span>')
        self.row1Layout.addWidget(self.modeComboBox)
        self.move_modeLabel = QLabel("Movement Mode:", self)
        self.row1Layout.addWidget(self.move_modeLabel)
        self.move_modeEdit = QComboBox(self)
        self.move_modeEdit.addItem("random")
        self.move_modeEdit.addItem("sequential")
        self.move_modeEdit.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Direction of Scan </span>')
        self.row1Layout.addWidget(self.move_modeEdit)
        self.modeComboBox.currentIndexChanged.connect(self.update_movement_mode_options)
        self.strideLabel = QLabel("Stride/Jump/Magnitude:", self)
        self.row1Layout.addWidget(self.strideLabel)
        self.strideLineEdit = QLineEdit("1")
        self.strideLineEdit.setPlaceholderText('10000')
        self.strideLineEdit.setToolTip('<span style="font-size: 12pt; font-weight: bold; color: black;"> Increment by NUMBER </span>')
        self.row1Layout.addWidget(self.strideLineEdit)

        options_layout2 = QHBoxLayout()
        self.bitsLabel = QLabel("Bits:", self)
        options_layout2.addWidget(self.bitsLabel)
        self.bitsLineEdit = QLineEdit(self)
        options_layout2.addWidget(self.bitsLineEdit)
        options_layout2.setStretchFactor(self.bitsLineEdit, 1)

        self.kValueLabel = QLabel("K Value:", self)
        options_layout2.addWidget(self.kValueLabel)
        self.kValueLineEdit = QLineEdit(self)
        options_layout2.addWidget(self.kValueLineEdit)
        options_layout2.setStretchFactor(self.kValueLineEdit, 1)
        
        self.nValueLabel = QLabel("N Value:", self)
        options_layout2.addWidget(self.nValueLabel)
        self.nValueLineEdit = QLineEdit(self)
        self.nValueLineEdit.setPlaceholderText('0x1000000000000000')
        options_layout2.addWidget(self.nValueLineEdit)
        options_layout2.setStretchFactor(self.nValueLineEdit, 2)

        self.keyhuntLayout.addLayout(self.row1Layout)
        self.keyhuntLayout.addLayout(options_layout2)
        
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
        self.read_and_display_file('KEYFOUNDKEYFOUND.txt', "Keyhunt File found. Check of Winners 😀 .", "No Winners Yet 😞")

    def browse_input_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Text Files (*.txt);;Binary Files (*.bin);;All Files (*.*)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            file_name = os.path.basename(file_path)
            self.inputFileLineEdit.setText(file_name)

    def run_keyhunt(self):
        command = self.construct_command_key()
        self.execute_command('"' + '" "'.join(command) + '"')

    def construct_command_key(self):
        mode = self.modeComboBox.currentText().strip()
        thread_count_key = int(self.threadComboBox_key.currentText())
        self.thread_count_key = thread_count_key
        base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "keyhunt", "keyhunt")

        command = [base_path, "-m", mode, "-t", str(self.thread_count_key)]

        file = self.inputFileLineEdit.text().strip()
        if file:
            input_file_relative_path = ["input", file]
            input_file_path = os.path.join(*input_file_relative_path)
            command.extend(["-f", input_file_path])

        move_mode = self.move_modeEdit.currentText().strip()
        if move_mode == 'random':
            if mode == 'bsgs':
                command.extend(["-B", move_mode])
            else:
                command.append("-R")
        elif move_mode == 'sequential':
            if mode == 'bsgs':
                command.extend(["-B", move_mode])
            else:
                command.append("-S")
        elif move_mode == 'backward' and mode == 'bsgs':
            command.extend(["-B", move_mode])
        elif move_mode == 'dance' and mode == 'bsgs':
            command.extend(["-B", move_mode])
        elif move_mode == 'both' and mode == 'bsgs':
            command.extend(["-B", move_mode])

        crypto = self.cryptoComboBox.currentText().strip()
        if crypto == "eth":
            command.extend(["-c", crypto])

        keyspace = self.keyspaceLineEdit.text().strip()
        if keyspace:
            if mode == 'bsgs':
                pass
            else:
                command.extend(["-r", keyspace])

        stride = self.strideLineEdit.text().strip()
        if stride:
            command.extend(["-I", stride])

        bits = self.bitsLineEdit.text().strip()
        if bits:
            command.extend(["-b", bits])

        n_value = self.nValueLineEdit.text().strip()
        if n_value:
            command.extend(["-n", n_value])

        k_value = self.kValueLineEdit.text().strip()
        if k_value:
            command.extend(["-k", k_value])

        look = self.lookComboBox.currentText().strip()
        if look:
            command.extend(["-l", look])

        return command

    def update_movement_mode_options(self):
        mode = self.modeComboBox.currentText()
        if mode == "bsgs":
            self.move_modeEdit.clear()
            self.move_modeEdit.addItem("random")
            self.move_modeEdit.addItem("sequential")
            self.move_modeEdit.addItem("backward")
            self.move_modeEdit.addItem("both")
            self.move_modeEdit.addItem("dance")
        else:
            self.move_modeEdit.clear()
            self.move_modeEdit.addItem("random")
            self.move_modeEdit.addItem("sequential")

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

    def stop_hunt(self):
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
        self.stop_hunt()
        event.accept()

def main():
    app = QApplication([])
    window = KeyHuntFrame()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()