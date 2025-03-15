"""
@author: Team Mizogg
"""
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import os
import subprocess
import signal
import time
import platform
import multiprocessing
from funct.console_gui import ConsoleWindow
from funct.command_thread import CommandThread
from game.speaker import Speaker

class CommandThread(QThread):
    commandOutput = pyqtSignal(str)
    commandFinished = pyqtSignal(int)

    def __init__(self, command):
        super().__init__()
        self.command = command
    
    def run(self):
        self.commandOutput.emit("Starting...(Check CMD window For Details)")
        self.process = subprocess.Popen(self.command, shell=True)
        # Define the interval for displaying the "Running" message
        display_interval = 30  # 30 seconds
        
        while self.process.poll() is None:
            time.sleep(display_interval)
            self.commandOutput.emit("Running...(Check CMD window For Details)")  # Emit the "Running" message every 30 seconds
        self.process.communicate()
        self.commandFinished.emit(self.process.returncode)

class VanbitFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cpu_count = multiprocessing.cpu_count()
        self.scanning = False
        self.timer = QTimer(self)
        self.commandThread = None
        
        main_layout = QVBoxLayout()

        vanbit_config = self.create_vanbitGroupBox()
        main_layout.addWidget(vanbit_config)
        
        Keysapce_config = self.create_keyspaceGroupBox()
        main_layout.addWidget(Keysapce_config)

        outputFile_config = self.create_outputFileGroupBox()
        main_layout.addWidget(outputFile_config)

        buttonLayout = QHBoxLayout()
        randomButton_van = QPushButton("Random VanBitCracken Cuda", self)
        randomButton_van.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start Random VanBitCracken Cuda </span>')
        randomButton_van.clicked.connect(self.run_VBCRandom)
        randomButton_van.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        buttonLayout.addWidget(randomButton_van)
        sequenceButton_van = QPushButton("Sequence VanBitCracken Cuda", self)
        sequenceButton_van.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start Sequence VanBitCracken Cuda </span>')
        sequenceButton_van.clicked.connect(self.run_VanBitCrackenS1)
        sequenceButton_van.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        buttonLayout.addWidget(sequenceButton_van)
        main_layout.addLayout(buttonLayout)
        buttonLayout_key = QHBoxLayout()
        randomButton_van_cpu = QPushButton("Random VanBitCracken CPU", self)
        randomButton_van_cpu.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start Random VanBitCracken With CPU </span>')
        randomButton_van_cpu.clicked.connect(self.run_VBCRandom_cpu)
        randomButton_van_cpu.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        buttonLayout_key.addWidget(randomButton_van_cpu)
        sequenceButton_van_cpu = QPushButton("Sequence VanBitCracken CPU", self)
        sequenceButton_van_cpu.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start Sequence VanBitCracken With CPU </span>')
        sequenceButton_van_cpu.clicked.connect(self.run_VanBitCrackenS1_cpu)
        sequenceButton_van_cpu.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        buttonLayout_key.addWidget(sequenceButton_van_cpu)
        main_layout.addLayout(buttonLayout_key)

        stopButton = self.create_stop_button()
        stopButton.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Stop All Running Scans </span>')
        stopButton.setStyleSheet(
            "QPushButton { font-size: 10pt; background-color: #1E1E1E; color: white; }"
            "QPushButton:hover { font-size: 10pt; background-color: #5D6062; color: white; }"
        )
        stopButton.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back))
        main_layout.addWidget(stopButton)

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
        self.keyspaceLineEdit = QLineEdit("80000000000000000:FFFFFFFFFFFFFFFFF")
        self.keyspaceLineEdit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Type in your own HEX Range separated with : </span>')
        keyspaceLayout.addWidget(self.keyspaceLineEdit)
        keyspaceMainLayout.addLayout(keyspaceLayout)
        keyspacerange_layout = QHBoxLayout()
        self.keyspace_slider = QSlider(Qt.Orientation.Horizontal)
        self.keyspace_slider.setMinimum(1)
        self.keyspace_slider.setMaximum(256)
        self.keyspace_slider.setValue(68)
        self.keyspace_slider.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.generic_scroll_01), 0.3)
        self.keyspace_slider.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Drag Left to Right to Adjust Range </span>')
        keyspacerange_layout1 = QHBoxLayout()
        keyspacerange_layout1.addWidget(self.keyspace_slider)
        self.keyspace_slider.valueChanged.connect(self.update_keyspace_range)
        self.bitsLabel = QLabel("Bits:", self)
        self.bitsLineEdit = QLineEdit(self)
        self.bitsLineEdit.setText("68")
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

    def create_stop_button(self):
        stopButton = QPushButton("Stop ALL", self)
        stopButton.clicked.connect(self.stop_hunt)
        stopButton.setStyleSheet(
            "QPushButton { font-size: 10pt; background-color: #1E1E1E; color: white; }"
            "QPushButton:hover { font-size: 10pt; background-color: #5D6062; color: white; }"
        )
        return stopButton

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
        self.lookComboBox.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Search for compressed keys (default). Can be used with also search uncompressed keys  </span>')
        outputFileLayout.addWidget(self.lookComboBox)
        self.inputFileLabel = QLabel("Input File:", self)
        outputFileLayout.addWidget(self.inputFileLabel)
        self.inputFileLineEdit = QLineEdit("btc.txt", self)
        self.inputFileLineEdit.setPlaceholderText('Click browse to find your BTC database')
        self.inputFileLineEdit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Type the Name of database txt file or Browse location </span>')
        outputFileLayout.addWidget(self.inputFileLineEdit)
        self.inputFileButton = QPushButton("Browse", self)
        self.inputFileButton.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Type the Name of database txt file or Browse location </span>')
        self.inputFileButton.clicked.connect(self.browse_input_file)
        outputFileLayout.addWidget(self.inputFileButton)
        self.found_progButton = QPushButton("🔥 Check if Found 🔥")
        self.found_progButton.clicked.connect(self.found_prog)
        self.found_progButton.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Click Here to See if your a Winner </span>')
        outputFileLayout.addWidget(self.found_progButton)
        return outputFileGroupBox

    def create_vanbitGroupBox(self):
        vanbitGroupBox = QGroupBox(self)
        vanbitGroupBox.setTitle("VanBitCracken Cuda Configuration")
        vanbitGroupBox.setStyleSheet("QGroupBox { border: 3px solid #E7481F; padding: 5px; }")
        self.vanbitLayout = QVBoxLayout(vanbitGroupBox)
        self.deviceLayout_van = QHBoxLayout()
        self.GPUButton = QPushButton("🔋 Check GPU 🪫", vanbitGroupBox)
        self.GPUButton.clicked.connect(self.list_if_gpu_van)
        self.GPUButton.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> List available devices </span>')
        self.deviceLayout_van.addWidget(self.GPUButton)
        self.GPUvsCPUButton = QPushButton("GPU 🆚 CPU", vanbitGroupBox)
        self.GPUvsCPUButton.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> See the performance of CPUvsGPU Power  </span>')
        self.GPUvsCPUButton.clicked.connect(self.list_if_gpu_van)
        self.deviceLayout_van.addWidget(self.GPUvsCPUButton)
        self.cpu_lable_van = QLabel("Number of CPUs:", self)
        self.deviceLayout_van.addWidget(self.cpu_lable_van)
        self.threadComboBox = QComboBox()
        for i in range(1, self.cpu_count + 1):
            self.threadComboBox.addItem(str(i))
        self.threadComboBox.setCurrentIndex(2)
        self.threadComboBox.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> The number of CPU available </span>')
        self.deviceLayout_van.addWidget(self.threadComboBox)
        
        self.groupSizeLabel = QLabel("Grid Size:", self)
        self.deviceLayout_van.addWidget(self.groupSizeLabel)
        self.gridSize_choice = QComboBox()
        self.gridSize_choice.addItems(['16','32', '64', '96', '128'])
        self.gridSize_choice.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> The number of GRID blocks Per CPU</span>')
        self.gridSize_choice.setCurrentIndex(1)
        self.deviceLayout_van.addWidget(self.gridSize_choice)
        self.gpuIdLabel_van = QLabel("CUDA ONLY List of GPU(s) to use:", vanbitGroupBox)
        self.deviceLayout_van.addWidget(self.gpuIdLabel_van)
        self.gpuIdLineEdit_van = QLineEdit("0", vanbitGroupBox)
        self.gpuIdLineEdit_van.setPlaceholderText('0, 1, 2')
        self.gpuIdLineEdit_van.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Use device with ID equal to N  (Example = 0 for main or for more than 1GPU = 0, 1, 2)</span>')
        self.deviceLayout_van.addWidget(self.gpuIdLineEdit_van)
        self.vanbitLayout.addLayout(self.deviceLayout_van)
        return vanbitGroupBox
    
    # Function to read and display file contents
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

    # Function to check if found
    def found_prog(self):
        self.read_and_display_file("found/found.txt", "File found. Check for Winners 😀.", "No Winners Yet 😞")

    def browse_input_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Text Files (*.txt);;Binary Files (*.bin);;All Files (*.*)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            file_name = os.path.basename(file_path)
            self.inputFileLineEdit.setText(file_name)

    def run(self, command):
        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
        for line in self.process.stdout:
            output = line.strip()
            self.consoleWindow.append_output(output)
        self.process.stdout.close()

    def run_VBCRandom(self):
        command = self.construct_command_van("VBCRandom")
        self.execute_command('"' + '" "'.join(command) + '"')

    def run_VanBitCrackenS1(self):
        command = self.construct_command_van("VanBitCrackenS1")
        self.execute_command('"' + '" "'.join(command) + '"')

    def construct_command_van(self, mode):
        thread_count_van = int(self.threadComboBox.currentText())

        # Specify the base path
        base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "vanbitcracken", mode)

        command = [base_path, "-t", str(thread_count_van), "-gpu"]

        gpu_ids = self.gpuIdLineEdit_van.text().strip()
        command.extend(["-gpuId", gpu_ids])

        gpu_grid = self.gridSize_choice.currentText()
        command.extend(["-g", gpu_grid])

        look = self.lookComboBox.currentText().strip()
        if look == 'both':
            command.append("-b")
        elif look == 'uncompress':
            command.append("-u")

        output_file_relative_path = ["found", "found.txt"]
        output_file_path = os.path.join(*output_file_relative_path)
        command.extend(["-o", output_file_path])

        keyspace = self.keyspaceLineEdit.text().strip()
        if keyspace:
            command.extend(["--keyspace", keyspace])

        input_file_relative_path = ["input", "btc.txt"]
        input_file_path = os.path.join(*input_file_relative_path)
        command.extend(["-i", input_file_path])

        self.consoleWindow.append_output(" ".join(command))
        return command

    def list_if_gpu_van(self):
        sender = self.sender()

        if sender == self.GPUButton:
            # Specify the base path
            base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "vanbitcracken", "VBCRandom")

            command = [base_path, "-l"]
            self.consoleWindow.append_output(" ".join(command))
            self.run(command)
        elif sender == self.GPUvsCPUButton:
            message_error = 'GPUvsCPU Test. \n This will cause the program to not respond for 10-20 seconds While Testing. \n Please wait after closing this screen.'
            self.pop_Result(message_error)
            # Specify the base path
            base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "vanbitcracken", "VBCRandom")

            command = [base_path, "-check"]
            self.consoleWindow.append_output(" ".join(command))
            self.run(command)

    def run_VBCRandom_cpu(self):
        command = self.construct_command_cpu("VBCRandom")
        self.execute_command('"' + '" "'.join(command) + '"')

    def run_VanBitCrackenS1_cpu(self):
        command = self.construct_command_cpu("VanBitCrackenS1")
        self.execute_command('"' + '" "'.join(command) + '"')

    def construct_command_cpu(self, mode):
        thread_count_van = int(self.threadComboBox.currentText())
        
        # Specify the base path
        base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "vanbitcracken", mode)

        command = [base_path, "-t", str(thread_count_van)]

        look = self.lookComboBox.currentText().strip()
        if look == 'both':
            command.append("-b")
        elif look == 'uncompress':
            command.append("-u")

        output_file_relative_path = ["found", "found.txt"]
        output_file_path = os.path.join(*output_file_relative_path)
        command.extend(["-o", output_file_path])

        keyspace = self.keyspaceLineEdit.text().strip()
        if keyspace:
            command.extend(["--keyspace", keyspace])

        input_file_relative_path = ["input", "btc.txt"]
        input_file_path = os.path.join(*input_file_relative_path)
        command.extend(["-i", input_file_path])

        self.consoleWindow.append_output(" ".join(command))
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

    def pop_Result(self, message_error):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Warning")
        msg_box.setText(message_error)
        msg_box.addButton(QMessageBox.StandardButton.Ok)
        msg_box.exec()

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
    window = VanbitFrame()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()