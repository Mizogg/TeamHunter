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
sys.path.extend(['input'])

ICO_ICON = "images/main/miz.ico"
TITLE_ICON = "images/main/title.png"

from bloomfilter import BloomFilter


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

class UpdateBloomFilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scanning = False
        self.timer = QTimer(self)
        self.setWindowTitle("Update Bloom Filter")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.setMinimumSize(640, 440)
        pixmap = QPixmap(f"{TITLE_ICON}")
        # Create a QLabel and set the pixmap as its content
        title_label = QLabel()
        title_label.setPixmap(pixmap)
        title_label.setFixedSize(pixmap.size())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.filename = "input/Bitcoin_addresses_LATEST.txt.gz"
        self.txt_filename = "input/Bitcoin_addresses_LATEST.txt.txt"
        self.update_button = QPushButton("1. Download New Database (Requires Internet)")
        self.update_button.setStyleSheet(
                "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
            )
        self.extract_button = QPushButton("2. Extract ZIP file to TEXT")
        self.extract_button.setStyleSheet(
                "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
            )
        self.covert_button = QPushButton("3. Convert TEXT file to BloomFilter Database")
        self.covert_button.setStyleSheet(
                "QPushButton { font-size: 12pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 12pt; background-color: #A13316; color: white; }"
            )
        self.download_label = QLabel("Downloading:")
        self.extraction_label = QLabel("Extracting:")
        self.progress_bar = QProgressBar()
        self.extraction_progress_bar = QProgressBar()
        self.consoleWindow = ConsoleWindow(self)

        self.load_extract_button = QPushButton("Load File for Extraction")
        self.load_convert_button = QPushButton("Load File for Conversion")
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.update_button)
        layout.addWidget(self.download_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.extract_button)
        layout.addWidget(self.load_extract_button)
        layout.addWidget(self.extraction_label)
        layout.addWidget(self.extraction_progress_bar)
        layout.addWidget(self.covert_button)
        layout.addWidget(self.load_convert_button)
        layout.addWidget(self.consoleWindow)
        self.setLayout(layout)

        self.update_button.clicked.connect(self.update_bloom_filter)
        self.extract_button.clicked.connect(self.extract_txt)
        self.covert_button.clicked.connect(self.bloom_filter)
        self.load_extract_button.clicked.connect(self.load_file_for_extraction)
        self.load_convert_button.clicked.connect(self.load_file_for_conversion)

    def update_bloom_filter(self):
        url_str = "http://addresses.loyce.club/Bitcoin_addresses_LATEST.txt.gz"
        url = QUrl(url_str)

        if os.path.exists(self.filename):
            confirm = QMessageBox.question(
                self,
                "File Exists",
                "The file already exists. Do you want to extract it instead of downloading again?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
            )
            if confirm == QMessageBox.StandardButton.Yes:
                self.extract_txt()
            elif confirm == QMessageBox.StandardButton.Cancel:
                return  # Do nothing and return to the initial state
            else:
                # Continue with the download
                self.consoleWindow.append_output(f"\nDownload from {self.url_edit} Starting Please Wait ")
                self.network_manager = QNetworkAccessManager()
                self.network_manager.finished.connect(self.download_finished)

                request = QNetworkRequest(url)
                self.reply = self.network_manager.get(request)
                self.reply.downloadProgress.connect(self.download_data_ready)  # Connect to downloadProgress

                self.progress_bar.setValue(0)

    def extract_txt(self):
        self.txt_filename = self.filename.replace(".gz", ".txt")
        with gzip.open(self.filename, 'rb') as gz_file:
            with open(self.txt_filename, 'wb') as txt_file:
                total_size = os.path.getsize(self.filename)  # Get the total size of the gzipped file
                extracted_size = 0
                self.consoleWindow.append_output(f"\n Extraction Starting  Please wait ")
                while True:
                    chunk = gz_file.read(1024)
                    if not chunk:
                        break
                    txt_file.write(chunk)

                    extracted_size += len(chunk)
                    extraction_progress = int(extracted_size / total_size * 100)
                    self.extraction_progress_bar.setValue(extraction_progress)
        message = f"Zip File {self.filename} has been Successfully Extracted to {self.txt_filename}"
        self.consoleWindow.append_output(message)
        QMessageBox.information(self, "Success", message)

    def load_file_for_extraction(self):
        file_dialog = QFileDialog()
        file_dialog.setOptions(QFileDialog.Option.DontUseNativeDialog)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Gzipped Files (*.gz);;All Files (*)")

        if file_dialog.exec() == QDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.filename = selected_files[0]
                self.consoleWindow.append_output(f"Selected file for extraction: {self.filename}")



    def load_file_for_conversion(self):
        file_dialog = QFileDialog()
        file_dialog.setOptions(QFileDialog.Option.DontUseNativeDialog)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Text Files (*.txt);;All Files (*)")

        if file_dialog.exec() == QDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.txt_filename = selected_files[0]
                self.consoleWindow.append_output(f"Selected file for conversion: {self.txt_filename}")

    def download_data_ready(self, bytes_received, bytes_total):
        if bytes_total > 0:
            progress = int(bytes_received / bytes_total * 100)
            self.progress_bar.setValue(progress)


    def count_lines(self, file):
        return sum(1 for line in open(file, 'r'))

    def add_to_bf(self, file, nom, bf_filter):
        i = 0
        line_10 = 100000
        f = open(file)
        while i < nom:
            if line_10 == i:
                print(f"\nTotal line -> {str(line_10)}")
                self.consoleWindow.append_output(f"\nTotal line -> {str(line_10)}")
                line_10 += 100000
            text = f.readline().strip()
            if text[:2] == '0x': bf_filter.add(text.lower()[2:])
            else: bf_filter.add(text)
            i += 1
        f.close()

    def bloom_filter(self):
        file_txt = self.txt_filename
        file_bf = 'input/btc.bf'
        line_count = self.count_lines(file_txt)
        print("all lines -> " + str(line_count))
        self.consoleWindow.append_output("all lines -> " + str(line_count))
        print("[I] Bloom Filter START")
        self.consoleWindow.append_output("[I] Bloom Filter START")
        print("[I] File input -> " + file_txt)
        self.consoleWindow.append_output("[I] File input -> " + file_txt)
        print("[I] File output -> " + file_bf)
        self.consoleWindow.append_output("[I] File output -> " + file_bf)
        bf = BloomFilter(size=line_count, fp_prob=1e-16)
        print("[I] ADD Bloom Filter")
        self.consoleWindow.append_output("[I] ADD Bloom Filter")
        self.add_to_bf(file_txt, line_count, bf)

        print("[I] Bloom Filter Statistic")
        print(
            "[+] Capacity: {} item(s)".format(bf.size),
            "[+] Number of inserted items: {}".format(len(bf)),
            "[+] Filter size: {} bit(s)".format(bf.filter_size),
            "[+] False Positive probability: {}".format(bf.fp_prob),
            "[+] Number of hash functions: {}".format(bf.num_hashes),
            "[+] Input file: {}".format(file_txt),
            "[+] Output file: {}".format(file_bf),
            sep="\n",
            end="\n\n",
        )

        # Save to file
        print("[I] Bloom Filter Start Save File")

        self.consoleWindow.append_output("[I] Bloom Filter Statistic")
        output_message = (
            "[+] Capacity: {} item(s)\n"
            "[+] Number of inserted items: {}\n"
            "[+] Filter size: {} bit(s)\n"
            "[+] False Positive probability: {}\n"
            "[+] Number of hash functions: {}\n"
            "[+] Input file: {}\n"
            "[+] Output file: {}".format(
                bf.size, len(bf), bf.filter_size, bf.fp_prob, bf.num_hashes, file_txt, file_bf
            )
        )
        self.consoleWindow.append_output(output_message)


        self.consoleWindow.append_output("[I] Bloom Filter Start Save File")
        with open(file_bf, "wb") as fp:
            bf.save(fp)
        print("[I] Bloom Filter END Save File")
        self.consoleWindow.append_output("[I] Bloom Filter END Save File")
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UpdateBloomFilterDialog()
    window.show()
    sys.exit(app.exec())