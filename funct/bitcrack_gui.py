"""
@author: Team Mizogg
"""
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import os
import signal
import subprocess
import platform
from console_gui import ConsoleWindow
from command_thread import CommandThread
from speaker import Speaker

class BitcrackFrame(QMainWindow):
    def __init__(self):
        super().__init__()

        self.scanning = False
        self.timer = QTimer(self)
        self.commandThread = None
        
        main_layout = QVBoxLayout()

        bitcrack_config = self.create_bitcrackGroupBox()
        main_layout.addWidget(bitcrack_config)
        
        key_space_config = self.create_keyspaceGroupBox()
        main_layout.addWidget(key_space_config)

        output_file_config = self.create_outputFileGroupBox()
        main_layout.addWidget(output_file_config)

        buttonLayout = QHBoxLayout()
        StartButton = QPushButton("Start BitCrack OpenCL", self)
        StartButton.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start BitCrack OpenCL </span>')
        StartButton.setStyleSheet(
                "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
            )
        StartButton.clicked.connect(self.run_gpu_open)
        StartButton.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        buttonLayout.addWidget(StartButton)
        StartButtonc = QPushButton("Start BitCrack Cuda", self)
        StartButtonc.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Start BitCrack Cuda </span>')
        StartButtonc.setStyleSheet(
                "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
            )
        StartButtonc.clicked.connect(self.run_gpu_cuda)
        StartButtonc.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        buttonLayout.addWidget(StartButtonc)

        main_layout.addLayout(buttonLayout)

        stop_button = self.create_stop_button()
        stop_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Stop All Running Scans </span>')
        stop_button.setStyleSheet(
            "QPushButton { font-size: 12pt; background-color: #1E1E1E; color: white; }"
            "QPushButton:hover { font-size: 12pt; background-color: #5D6062; color: white; }"
        )
        stop_button.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_back))
        main_layout.addWidget(stop_button)

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
        self.keyspaceLineEdit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Type in your own HEX Range separated with : </span>')
        keyspaceLayout.addWidget(self.keyspaceLineEdit)
        keyspaceMainLayout.addLayout(keyspaceLayout)

        keyspacerange_layout = QHBoxLayout()
        self.keyspace_slider = QSlider(Qt.Orientation.Horizontal)
        self.keyspace_slider.setMinimum(1)
        self.keyspace_slider.setMaximum(256)
        self.keyspace_slider.setValue(66)
        self.keyspace_slider.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.generic_scroll_01), 0.3)
        self.keyspace_slider.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Drag Left to Right to Adjust Range </span>')
        keyspacerange_layout1 = QHBoxLayout()
        keyspacerange_layout1.addWidget(self.keyspace_slider)
        self.keyspace_slider.valueChanged.connect(self.update_keyspace_range)
        self.bitsLabel = QLabel("Bits:", self)
        self.bitsLineEdit = QLineEdit(self)
        self.bitsLineEdit.setText("66")
        self.bitsLineEdit.textChanged.connect(self.updateSliderAndRanges)
        keyspacerange_layout1.addWidget(self.bitsLabel)
        keyspacerange_layout1.addWidget(self.bitsLineEdit)
        keyspaceMainLayout.addLayout(keyspacerange_layout)
        keyspaceMainLayout.addLayout(keyspacerange_layout1)
        return keyspaceGroupBox


    def update_keyspace_range(self, value):
        start_range = hex(2 ** (value - 1))[2:]
        end_range = hex(2 ** value - 1)[2:]
        self.keyspaceLineEdit.setText(f"{start_range}:{end_range}")
        self.bitsLineEdit.setText(str(value))

    def updateSliderAndRanges(self, text):
        try:
            bits = int(text)
            bits = max(0, min(bits, 256))
            if bits == 256:
                start_range = "8000000000000000000000000000000000000000000000000000000000000000"
                end_range = "fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140"
            else:
                start_range = hex(2 ** (bits - 1))[2:]
                end_range = hex(2 ** bits - 1)[2:]
            self.keyspace_slider.setValue(bits)
            self.keyspaceLineEdit.setText(f"{start_range}:{end_range}")
        except ValueError:
            range_message = "Range should be in Bit 1-256 "
            QMessageBox.information(self, "Range Error", range_message)

    def create_stop_button(self):
        stopButton = QPushButton("Stop ALL", self)
        stopButton.clicked.connect(self.stop_hunt)
        stopButton.setObjectName("stopButton")
        return stopButton

    # Function to create the Output File Configuration GUI
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
        self.inputFileButton.setStyleSheet("color: #E7481F;")
        self.inputFileButton.clicked.connect(self.browse_input_file)
        self.inputFileButton.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Type the Name of database txt file or Browse location </span>')
        outputFileLayout.addWidget(self.inputFileButton)

        self.save_prog = QCheckBox("💾 Save Progress 💾")
        self.save_prog.setStyleSheet("color: #E7481F;")
        self.save_prog.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Save The Progress of BitCrack Scan (default) ON</span>')
        self.save_prog.setChecked(True)
        outputFileLayout.addWidget(self.save_prog)

        self.save_progButton = QPushButton("💾 Check Progress 💾")
        self.save_progButton.clicked.connect(self.check_prog)
        self.save_progButton.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Check The Progress of BitCrack </span>')
        outputFileLayout.addWidget(self.save_progButton)

        self.found_progButton = QPushButton("🔥 Check if Found 🔥")
        self.found_progButton.clicked.connect(self.found_prog)
        self.found_progButton.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Click Here to See if your a Winner </span>')
        outputFileLayout.addWidget(self.found_progButton)

        return outputFileGroupBox

    # Function to create the BitCrack OpenCL and CUDA Configuration GUI
    def create_bitcrackGroupBox(self):
        bitcrackGroupBox = QGroupBox(self)
        bitcrackGroupBox.setTitle("BitCrack OpenCL and Cuda Configuration")
        bitcrackGroupBox.setStyleSheet("QGroupBox { border: 3px solid #E7481F; padding: 5px; }")
        self.bitcrackLayout = QVBoxLayout(bitcrackGroupBox)

        self.deviceLayout = QHBoxLayout()

        # Button to check GPU information
        self.GPUButton = QPushButton("🔋 Check GPU 🪫", bitcrackGroupBox)
        self.GPUButton.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> List available devices </span>')
        self.GPUButton.clicked.connect(self.list_if_gpu)
        self.deviceLayout.addWidget(self.GPUButton)

        # Dropdown for block size selection
        self.blocksSizeLabel = QLabel("Block Size:", self)
        self.deviceLayout.addWidget(self.blocksSizeLabel)
        self.blocksSize_choice = QComboBox()
        for i in range(8, 153, 2):
            self.blocksSize_choice.addItem(str(i))
        self.blocksSize_choice.setCurrentIndex(12)
        self.blocksSize_choice.setMinimumWidth(60)
        self.blocksSize_choice.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> The number of CUDA blocks </span>')
        self.deviceLayout.addWidget(self.blocksSize_choice)

        # Dropdown for thread count selection
        self.threadLabel_n = QLabel("Number of Threads:", self)
        self.deviceLayout.addWidget(self.threadLabel_n)
        self.threadComboBox_n = QComboBox()
        self.threadComboBox_n.addItems(['32', '64', '96', '128', '256', '512'])
        self.threadComboBox_n.setCurrentIndex(4)
        self.threadComboBox_n.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Threads per block </span>')
        self.deviceLayout.addWidget(self.threadComboBox_n)

        # Dropdown for points size selection
        self.pointsSizeLabel = QLabel("Points Size:", self)
        self.deviceLayout.addWidget(self.pointsSizeLabel)
        self.pointsSize_choice = QComboBox()
        self.pointsSize_choice.addItems(['128', '256', '512', '1024', '2048'])
        self.pointsSize_choice.setCurrentIndex(1)
        self.pointsSize_choice.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Each thread will process NUMBER keys at a time </span>')
        self.deviceLayout.addWidget(self.pointsSize_choice)

        # Input field for stride/jump/magnitude
        self.strideLabel = QLabel("Stride/Jump/Magnitude:", bitcrackGroupBox)
        self.deviceLayout.addWidget(self.strideLabel)
        self.strideLineEdit = QLineEdit("1", bitcrackGroupBox)
        self.strideLineEdit.setPlaceholderText('10000')
        self.strideLineEdit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Increment by NUMBER </span>')
        self.deviceLayout.addWidget(self.strideLineEdit)

        self.gpuIdLabel = QLabel("CUDA ONLY List of GPU(s) to use:", bitcrackGroupBox)
        self.deviceLayout.addWidget(self.gpuIdLabel)

        self.gpuIdLineEdit = QLineEdit("0", bitcrackGroupBox)
        self.gpuIdLineEdit.setPlaceholderText('0, 1, 2')
        self.gpuIdLineEdit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Use device with ID equal to N  (Example = 0 for main or for more than 1GPU = 0, 1, 2) </span>')
        self.deviceLayout.addWidget(self.gpuIdLineEdit)
        
        self.bitcrackLayout.addLayout(self.deviceLayout)

        return bitcrackGroupBox

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

    # Function to check progress
    def check_prog(self):
        self.read_and_display_file('input/progress.txt', "Progress file found.", "Progress")

    # Function to check if found
    def found_prog(self):
        self.read_and_display_file("found/found.txt", "File found. Check for Winners 😀.", "No Winners Yet 😞")

    # Function to browse for an input file
    def browse_input_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Text Files (*.txt);;Binary Files (*.bin);;All Files (*.*)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            file_name = os.path.basename(file_path)
            self.inputFileLineEdit.setText(file_name)

    # Function to list GPU information
    def list_if_gpu(self):
        # Specify the base path
        base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bitcrack", "cudaInfo.exe")

        command = [base_path]
        self.consoleWindow.append_output(" ".join(command))
        self.run(command)

    # Function to run a command and display its output
    def run(self, command):
        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
        for line in self.process.stdout:
            output = line.strip()
            self.consoleWindow.append_output(output)
        self.process.stdout.close()

    # Function to run BitCrack with OpenCL
    def run_gpu_open(self):
        command = self.construct_command("clBitcrack")
        self.execute_command('"' + '" "'.join(command) + '"')

    # Function to run BitCrack with CUDA
    def run_gpu_cuda(self):
        command = self.construct_command("cuBitcrack")
        self.execute_command('"' + '" "'.join(command) + '"')

    # Function to construct the BitCrack command based on user inputs
    def construct_command(self, mode):
        gpu_ids = self.gpuIdLineEdit.text().strip()
        gpu_blocks = self.blocksSize_choice.currentText()
        gpu_points = self.pointsSize_choice.currentText()
        thread_count_n = int(self.threadComboBox_n.currentText())
        stride = self.strideLineEdit.text().strip()

        # Specify the base path
        base_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "bitcrack", mode)

        command = [base_path]
        command.extend(["-d", gpu_ids])
        command.extend(["-b", gpu_blocks])
        command.extend(["-p", gpu_points])
        command.extend(["-t", str(thread_count_n)])
        command.extend(["--stride", stride])
        # Keyspace
        keyspace = self.keyspaceLineEdit.text().strip()
        if keyspace:
            command.extend(["--keyspace", keyspace])

        # Output file
        output_file_relative_path = ["found", "found.txt"]
        output_file_path = os.path.join(*output_file_relative_path)
        command.extend(["-o", output_file_path])

        # Look type
        look = self.lookComboBox.currentText().strip()
        if look == 'compress':
            command.append("-c")
        elif look == 'uncompress':
            command.append("-u")

        # Input file
        file = self.inputFileLineEdit.text().strip()
        input_file_relative_path = ["input", file]
        input_file_path = os.path.join(*input_file_relative_path)
        command.extend(["-i", input_file_path])

        if self.save_prog.isChecked():
            progress_file_relative_path = ["input", "progress.txt"]
            progress_file_path = os.path.join(*progress_file_relative_path)
            command.extend(["--continue", progress_file_path])

        return command

    # Function to execute a BitCrack command
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

    # Function to handle command completion
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

    # Function to stop the BitCrack process
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

    # Function to handle application closure
    def closeEvent(self, event):
        self.stop_hunt()
        event.accept()

def main():
    app = QApplication([])
    window = BitcrackFrame()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
