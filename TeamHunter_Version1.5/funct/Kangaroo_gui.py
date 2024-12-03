from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import bit
import ctypes
import platform
import sys
import os
import random
import glob
import subprocess
import signal
import platform
import multiprocessing
from funct.console_gui import ConsoleWindow
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from funct.command_thread import CommandThread
from funct.range_div_gui import RangeDialog
##
class KangarooFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cpu_count = multiprocessing.cpu_count()
        self.scanning = False
        self.user_stopped = False
        self.timer = QTimer(self)
        self.commandThread = None

        main_layout = QVBoxLayout()

        Kangaroo_config = self.create_threadGroupBox()
        main_layout.addWidget(Kangaroo_config)
        
        Keysapce_config = self.create_keyspaceGroupBox()
        main_layout.addWidget(Keysapce_config)

        public_config = self.Public_in_GroupBox()
        main_layout.addWidget(public_config)

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
        keyspaceLabel.setStyleSheet("font-size: 10pt; font-weight: bold; color: #E7481F;")
        keyspaceLayout.addWidget(keyspaceLabel)
        self.keyspaceLineEdit = QLineEdit("4000000000000000000000000000000000:7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
        self.keyspaceLineEdit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Type in your own HEX Range separated with : </span>')
        keyspaceLayout.addWidget(self.keyspaceLineEdit)
        keyspaceMainLayout.addLayout(keyspaceLayout)
        keyspacerange_layout = QHBoxLayout()
        self.keyspace_slider = QSlider(Qt.Orientation.Horizontal)
        self.keyspace_slider.setMinimum(1)
        self.keyspace_slider.setMaximum(256)
        self.keyspace_slider.setValue(135)
        self.keyspace_slider.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Drag Left to Right to Adjust Range (Address Mode 1-160 BSGS Mode 50-160)</span>')
        keyspacerange_layout1 = QHBoxLayout()
        keyspacerange_layout1.addWidget(self.keyspace_slider)
        self.keyspace_slider.valueChanged.connect(self.update_keyspace_range)
        self.bitsLabel = QLabel("Bits:", self)
        self.bitsLabel.setStyleSheet("font-size: 10pt; font-weight: bold; color: #E7481F;")
        self.bitsLineEdit = QLineEdit(self)
        self.bitsLineEdit.setText("135")
        self.bitsLineEdit.textChanged.connect(self.updateSliderAndRanges)
        keyspacerange_layout1.addWidget(self.bitsLabel)
        keyspacerange_layout1.addWidget(self.bitsLineEdit)
        keyspaceMainLayout.addLayout(keyspacerange_layout)
        keyspaceMainLayout.addLayout(keyspacerange_layout1)
        return keyspaceGroupBox

    def update_keyspace_range(self, value):
        start_range = 2 ** (value - 1)
        end_range = 2 ** value - 1
        self.keyspaceLineEdit.setText(f"{start_range:X}:{end_range:X}")
        self.bitsLineEdit.setText(str(value))

    def updateSliderAndRanges(self, text):
        try:
            bits = int(text)
            bits = max(1, min(bits, 256))
            if bits == 256:
                start_range = "8000000000000000000000000000000000000000000000000000000000000000"
                end_range = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140"
            else:
                start_range = 2 ** (bits - 1)
                end_range = 2 ** bits - 1
                start_range = f"{start_range:X}"
                end_range = f"{end_range:X}"
            
            self.keyspace_slider.setValue(bits)
            self.keyspaceLineEdit.setText(f"{start_range}:{end_range}")
        
        except ValueError:
            range_message = "Range should be in Bit 1-256"
            QMessageBox.information(self, "Range Error", range_message)

    def range_check(self):
        self.range_dialog = RangeDialog()
        self.range_dialog.show()

    def create_stop_button(self):
        stopButton = QPushButton("Stop kangaroo", self)
        stopButton.clicked.connect(self.stop_hunt)
        stopButton.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Stop kangaroo  </span>')
        stopButton.setStyleSheet(
            "QPushButton { font-size: 12pt; background-color: #1E1E1E; color: white; }"
            "QPushButton:hover { font-size: 12pt; background-color: #5D6062; color: white; }"
        )
        return stopButton

    def create_start_button(self):
        StartButton = QPushButton("Start kangaroo", self)
        StartButton.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start kangaroo </span>')
        StartButton.setStyleSheet(
                "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
            )
        StartButton.clicked.connect(self.run_Kangaroo)
        return StartButton


    def Public_in_GroupBox(self):
        Public_FileGroupBox = QGroupBox(self)
        Public_FileGroupBox.setTitle("Public Key Input")
        Public_FileGroupBox.setStyleSheet("QGroupBox { border: 3px solid #E7481F; padding: 5px; }")
        Public_FileLayout = QHBoxLayout(Public_FileGroupBox)
        self.Public_FileLabel1 = QLabel(" Type here:", self)
        self.Public_FileLabel1.setStyleSheet("font-size: 10pt; font-weight: bold; color: #E7481F;")
        self.Public_FileLabel = QLineEdit("02145d2611c823a396ef6712ce0f712f09b9b4f3135e3e0aa3230fb9b6d08d1e16")
        Public_FileLayout.addWidget(self.Public_FileLabel1)
        Public_FileLayout.addWidget(self.Public_FileLabel)

        self.found_progButton = QPushButton("🔥 Check if Found 🔥")
        self.found_progButton.clicked.connect(self.found_prog)
        self.found_progButton.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Click Here to See if your a Winner </span>')
        Public_FileLayout.addWidget(self.found_progButton)

        self.range_progButton = QPushButton("💾 Range Tools 💾")
        self.range_progButton.clicked.connect(self.range_check)
        self.range_progButton.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Ranges ....... </span>')
        Public_FileLayout.addWidget(self.range_progButton)

        return Public_FileGroupBox

    def create_threadGroupBox(self):
        self.KangarooLayout = QVBoxLayout()
        threadGroupBox = QGroupBox(self)
        threadGroupBox.setTitle("Kangaroo Configuration")
        threadGroupBox.setStyleSheet("QGroupBox { border: 3px solid #E7481F; padding: 15px; }")
        self.row1Layout = QHBoxLayout()
        self.threadLabel = QLabel("Number of CPUs:", self)
        self.threadLabel.setStyleSheet("font-size: 10pt; font-weight: bold; color: #E7481F;")
        self.row1Layout.addWidget(self.threadLabel)
        self.threadComboBox_key = QComboBox()
        for i in range(1, self.cpu_count + 1):
            self.threadComboBox_key.addItem(str(i))
        self.threadComboBox_key.setCurrentIndex(2)
        self.threadComboBox_key.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Number of CPU to use. default = Total-3</span>')
        self.row1Layout.setStretchFactor(self.threadComboBox_key, 1)
        self.row1Layout.addWidget(self.threadComboBox_key)
        self.strideLineEdit = QLineEdit("72057594037927935")
        self.strideLineEdit.setPlaceholderText('72057594037927935')
        self.strideLineEdit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Total range search in 1 loop. default=72057594037927935</span>')
        self.row1Layout.addWidget(self.strideLineEdit)

        DP_label = QLabel('DP Ammount:')
        DP_label.setStyleSheet("font-size: 10pt; font-weight: bold; color: #E7481F;")
        DP_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.row1Layout.addWidget(DP_label)
        self.ammount_DP = QComboBox()
        self.ammount_DP.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
        self.ammount_DP.setCurrentIndex(4)
        self.row1Layout.addWidget(self.ammount_DP)

        max_label = QLabel('MaxStep :')
        max_label.setStyleSheet("font-size: 10pt; font-weight: bold; color: #E7481F;")
        max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.row1Layout.addWidget(max_label)
        self.ammount_maxStep = QComboBox()
        self.ammount_maxStep.addItems(['0', '1', '2'])
        self.ammount_maxStep.setCurrentIndex(2)
        self.row1Layout.addWidget(self.ammount_maxStep)

        self.move_modeLabel = QLabel("Movement Mode:", self)
        self.move_modeLabel.setStyleSheet("font-size: 10pt; font-weight: bold; color: #E7481F;")
        self.row1Layout.addWidget(self.move_modeLabel)
        self.move_modeEdit = QComboBox(self)
        self.move_modeEdit.addItem("rand")
        self.move_modeEdit.addItem("rand1")
        self.move_modeEdit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start from a random value in the given range from min:max and search 0XFFFFFFFFFFFFFF values then again take a new random </span>')
        self.row1Layout.addWidget(self.move_modeEdit)

        self.KangarooLayout.addLayout(self.row1Layout)
        
        threadGroupBox.setLayout(self.KangarooLayout)
        return threadGroupBox
    
    def found_prog(self):
        file_path = 'KEYFOUNDKEYFOUND.txt'
        self.read_and_display_file(file_path, "😀😀 Kangaroo File found. Check for Winners 😀😀.", "😞😞No Winners Yet 😞😞")


    def read_and_display_file(self, file_path, success_message, error_message):
        self.consoleWindow.append_output(f"Attempting to read file: {file_path}")
        try:
            if not os.path.exists(file_path):
                self.consoleWindow.append_output(f"⚠️ {error_message} File not found. Please check the file path.")
                return None
                
            with open(file_path, 'r') as file:
                output_from_text = file.read()
                self.consoleWindow.append_output(success_message)
                self.consoleWindow.append_output(output_from_text)
                return output_from_text
        except FileNotFoundError:
            self.consoleWindow.append_output(f"⚠️ {error_message} File not found. Please check the file path.")
            return None
        except Exception as e:
            self.consoleWindow.append_output(f"An error occurred: {str(e)}")
            return None

    def run_Kangaroo(self):
        command = self.construct_command_key()
        self.execute_command(command)

    def construct_command_key(self):

        ncore = int(self.threadComboBox_key.currentText())
        increment = int(self.strideLineEdit.text().strip())
        public_key = self.Public_FileLabel.text().strip()
        keyspace = self.keyspaceLineEdit.text().strip()
        thread_count_key = int(self.threadComboBox_key.currentText())
        move_mode = self.move_modeEdit.currentText()
        dp = int(self.ammount_DP.currentText())
        max_step = int(self.ammount_maxStep.currentText())

        command = ["python", "kangaroo.py"]

        command.extend(["-p", public_key])
        
        start_range, end_range = keyspace.split(':')
        start_range_hex = start_range
        end_range_hex = end_range
        command.extend(["-keyspace", f"{start_range_hex}:{end_range_hex}"])

        command.extend(["-ncore", str(thread_count_key)])

        command.extend(["-n", str(increment)])

        move_mode = self.move_modeEdit.currentText()
        if move_mode == 'rand':
            command.append("-rand")
        
        elif move_mode == 'rand1':
            command.append("-rand1")
        command.extend(["-dp", str(dp)])
        command.extend(["-mx", str(max_step)])
        return command

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

    def stop_hunt(self):
        if self.commandThread and self.commandThread.isRunning():
            self.user_stopped = True
            if platform.system() == "Windows":
                subprocess.Popen(["taskkill", "/F", "/T", "/PID", str(self.commandThread.process.pid)])
            else:
                os.killpg(os.getpgid(self.commandThread.process.pid), signal.SIGTERM)
            
            self.timer.stop()
            self.scanning = False

    @pyqtSlot(int)
    def command_finished(self, returncode):
        self.timer.stop()
        self.scanning = False

        if self.user_stopped:
            self.consoleWindow.append_output("Process has been stopped by the user")
        elif returncode == 0:
            self.consoleWindow.append_output("Command execution finished successfully")
        else:
            self.consoleWindow.append_output("Command execution failed")

        self.user_stopped = False

    def closeEvent(self, event):
        self.stop_hunt()
        event.accept()

def main():
    app = QApplication([])
    window = KangarooFrame()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()