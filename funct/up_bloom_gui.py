"""

@author: Team Mizogg
"""
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import gzip
import os
import subprocess
import sys


ICO_ICON = "webfiles/css/images/main/miz.ico"
TITLE_ICON = "webfiles/css/images/main/title.png"

class ConsoleWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.consoleOutput = QPlainTextEdit(self)
        self.consoleOutput.setReadOnly(True)
        self.consoleOutput.setMinimumSize(300, 200)
        self.layout.addWidget(self.consoleOutput)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.consoleOutput.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    @pyqtSlot(str)
    def append_output(self, output):
        self.consoleOutput.appendPlainText(output)

class CommandThread(QThread):
    commandOutput = pyqtSignal(str)
    commandFinished = pyqtSignal(int)

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.process = None

    def run(self):
        self.commandOutput.emit(self.command)
        self.process = subprocess.Popen(
            self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
        )
        for line in self.process.stdout:
            output = line.strip()
            self.commandOutput.emit(output)
        self.process.stdout.close()
        self.commandFinished.emit(self.process.wait())

class UpdateBloomFilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scanning = False
        self.timer = QTimer(self)
        self.commandThread = None
        self.setWindowTitle("Update Bloom Filter")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.setMinimumSize(640, 440)
        pixmap = QPixmap(f"{TITLE_ICON}")
        # Create a QLabel and set the pixmap as its content
        title_label = QLabel()
        title_label.setPixmap(pixmap)
        title_label.setFixedSize(pixmap.size())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.url_edit = QLineEdit("http://addresses.loyce.club/Bitcoin_addresses_LATEST.txt.gz")
        self.url_edit.setPlaceholderText("Enter URL")
        self.update_button = QPushButton("Update")
        self.update_button.setStyleSheet(
                "QPushButton { font-size: 16pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 16pt; background-color: #A13316; color: white; }"
            )
        self.download_label = QLabel("Downloading:")
        self.extraction_label = QLabel("Extracting:")
        self.progress_bar = QProgressBar()
        self.extraction_progress_bar = QProgressBar()
        self.consoleWindow = ConsoleWindow(self)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.url_edit)
        layout.addWidget(self.update_button)
        layout.addWidget(self.download_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.extraction_label)
        layout.addWidget(self.extraction_progress_bar)
        layout.addWidget(self.consoleWindow)
        self.setLayout(layout)

        self.update_button.clicked.connect(self.update_bloom_filter)

    def update_bloom_filter(self):
        url_str = self.url_edit.text()
        url = QUrl(url_str)
        self.filename = "Bitcoin_addresses_LATEST.txt.gz"
        
        # Check if the file already exists
        if os.path.exists(self.filename):
            confirm = QMessageBox.question(self, "File Exists", "The file already exists. Do you want to remove it?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    os.remove(self.filename)
                except OSError as e:
                    QMessageBox.critical(self, "Error", f"Error removing existing file: {e}")
                    return
            else:
                return
        self.consoleWindow.append_output(f"\nDownload from {self.url_edit} Starting Please Wait ")
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.download_finished)
        
        request = QNetworkRequest(url)
        self.reply = self.network_manager.get(request)
        self.reply.downloadProgress.connect(self.download_data_ready)  # Connect to downloadProgress

        self.progress_bar.setValue(0)

    def download_data_ready(self, bytes_received, bytes_total):
        if bytes_total > 0:
            progress = int(bytes_received / bytes_total * 100)
            self.progress_bar.setValue(progress)

    def download_finished(self):
        self.consoleWindow.append_output(f"\n Download Finished Now Extracting Please wait")
        if self.reply.error() == QNetworkReply.NetworkError.NoError:
            with open(self.filename, "wb") as file:
                file.write(self.reply.readAll())

            txt_filename = self.filename.replace(".gz", ".txt")
            with gzip.open(self.filename, 'rb') as gz_file:
                with open(txt_filename, 'wb') as txt_file:
                    total_size = os.path.getsize(self.filename)  # Get the total size of the gzipped file
                    extracted_size = 0
                    self.consoleWindow.append_output(f"\n Extraction Starting Please wait ")
                    while True:
                        chunk = gz_file.read(1024)
                        if not chunk:
                            break
                        txt_file.write(chunk)

                        extracted_size += len(chunk)
                        extraction_progress = int(extracted_size / total_size * 100)
                        self.extraction_progress_bar.setValue(extraction_progress)
            self.consoleWindow.append_output(f"\n Extraction Finished Converting Please wait this will run in the back and look like not responing until completed can take 20mins")
            python_cmd = f'python Cbloom.py {txt_filename} btc.bf'
            self.execute_command(python_cmd)

            QMessageBox.information(self, "Success", "Bloom filter updated successfully.")
        else:
            QMessageBox.critical(self, "Error", f"Download error: {self.reply.errorString()}")

        # Clean up downloaded file
        os.remove(self.filename)

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
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdateBloomFilterDialog()
    window.show()
    sys.exit(app.exec())