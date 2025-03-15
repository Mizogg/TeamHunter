"""
@author: Team Mizogg
"""
from PyQt6.QtCore import QMetaObject, Qt, Q_ARG
from PyQt6.QtWidgets import *
from funct import console_gui

class RangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Hexadecimal Range Calculator")
        self.resize(800, 600)

        mainLayout = QVBoxLayout(self)

        keyspaceGroupBox = self.create_keyspaceGroupBox()
        mainLayout.addWidget(keyspaceGroupBox)

        self.consoleWindow = console_gui.ConsoleWindow(self)
        mainLayout.addWidget(self.consoleWindow)


    def create_keyspaceGroupBox(self):
        keyspaceGroupBox = QGroupBox(self)
        keyspaceGroupBox.setTitle("Key Space Configuration")
        keyspaceGroupBox.setStyleSheet("QGroupBox { border: 3px solid #E7481F; padding: 5px; }")
        keyspaceMainLayout = QVBoxLayout(keyspaceGroupBox)

        self.keyspaceLabel = QLabel("Key Space:", self)
        keyspaceMainLayout.addWidget(self.keyspaceLabel)

        self.start_edit = QLineEdit("80000000000000000")
        self.start_edit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Type the start range in HEX </span>')

        self.end_edit = QLineEdit("FFFFFFFFFFFFFFFFF")
        self.end_edit.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Type the end range in HEX </span>')
        self.keyspace_slider = QSlider(Qt.Orientation.Horizontal)
        self.keyspace_slider.setMinimum(1)
        self.keyspace_slider.setMaximum(256)
        self.keyspace_slider.setValue(68)
        self.keyspace_slider.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;"> Drag Left to Right to Adjust Range </span>')
        keyspacerange_layout = QVBoxLayout()
        keyspacerange_layout.addWidget(self.start_edit)
        keyspacerange_layout.addWidget(self.end_edit)
        keyspacerange_layout.addWidget(self.keyspace_slider)

        keyspaceMainLayout.addLayout(keyspacerange_layout)

        self.keyspace_slider.valueChanged.connect(self.update_keyspace_range)
        self.bitsLabel = QLabel("Bits:", self)
        keyspaceMainLayout.addWidget(self.bitsLabel)

        self.bitsLineEdit = QLineEdit(self)
        self.bitsLineEdit.setText("68")
        self.bitsLineEdit.textChanged.connect(self.updateSliderAndRanges)
        keyspaceMainLayout.addWidget(self.bitsLineEdit)

        percentLayout = QHBoxLayout()
        percentLabel = QLabel("Percentage:")
        percentLayout.addWidget(percentLabel)
        self.percentLineEdit = QLineEdit("90")
        percentLayout.addWidget(self.percentLineEdit)
        keyspaceMainLayout.addLayout(percentLayout)

        calculateButton = QPushButton("Calculate", self)
        calculateButton.clicked.connect(self.calculate_percentage)
        keyspaceMainLayout.addWidget(calculateButton)

        hexRangeGroupBox = self.create_hexRangeGroupBox()
        keyspaceMainLayout.addWidget(hexRangeGroupBox)

        return keyspaceGroupBox

    def create_hexRangeGroupBox(self):
        hexRangeGroupBox = QGroupBox(self)
        hexRangeGroupBox.setTitle("Range Division Tools")
        hexRangeGroupBox.setStyleSheet("QGroupBox { border: 3px solid #E7481F; padding: 5px; }")
        hexRangeMainLayout = QVBoxLayout(hexRangeGroupBox)

        power_label = QLabel("Show")
        power_label.setObjectName("powerLabel")
        self.format_combo_box_divs = QComboBox()
        self.format_combo_box_divs.addItems(
            ['1', '2', '4', '8', '16', '32', '64', '128', '256', '512', '1024', '2048', '4096', '8192', '16384', '32768', '65536']
        )
        select_power_layout = QHBoxLayout()
        select_power_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        select_power_layout.addWidget(power_label)
        select_power_layout.addWidget(self.format_combo_box_divs)

        self.Check_button = QPushButton("Check")
        self.Check_button.clicked.connect(self.div_range)
        hexRangeMainLayout.addLayout(select_power_layout)
        hexRangeMainLayout.addWidget(self.Check_button)

        calculateButton1 = QPushButton("Calculate and Percent", self)
        calculateButton1.clicked.connect(self.calculate_percentage_and_div_range)
        hexRangeMainLayout.addWidget(calculateButton1)

        return hexRangeGroupBox

    def div_range(self):
        try:
            start_value = self.start_edit.text()
            end_value = self.end_edit.text()
            num_divs = int(self.format_combo_box_divs.currentText())
            self.start_hex = int(start_value, 16)
            self.end_hex = int(end_value, 16)
            
            chunk_size = (self.end_hex - self.start_hex) // num_divs
            
            if self.end_hex < self.start_hex:
                error_message = "Start HEX is greater than Stop HEX"
                self.consoleWindow.append_output(error_message)
            else:
                ranges = [(self.start_hex + i * chunk_size, self.start_hex + (i + 1) * chunk_size) for i in range(num_divs)]
                start_index = self.start_hex
                
                for i, (priv_start, priv_end) in enumerate(ranges, start=1):
                    priv_start_hex = f"{priv_start:X}"
                    priv_end_hex = f"{priv_end:X}"
                    
                    if start_index >= priv_start and start_index < priv_end:
                        displayprint = f' Range {i}:\t{priv_start_hex} - {priv_end_hex}\t<<-- Current Range'
                    else:
                        displayprint = f' Range {i}:\t{priv_start_hex} - {priv_end_hex}'
                        
                    self.consoleWindow.append_output(displayprint)
        
        except ValueError as e:
            error_message = f"Value Error: {str(e)}"
            self.consoleWindow.append_output(error_message)


    def update_keyspace_range(self, value):
        start_range = 2 ** (value - 1)
        end_range = 2 ** value - 1
        self.start_edit.setText(f"{start_range:X}")
        self.end_edit.setText(f"{end_range:X}")
        self.bitsLineEdit.setText(str(value))

    def updateSliderAndRanges(self, text):
        try:
            bits = int(text)
            self.keyspace_slider.setValue(bits)

            if bits == 256:
                start_range = "8000000000000000000000000000000000000000000000000000000000000000"
                end_range = "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364140"
            else:
                start_range = 2 ** (bits - 1)
                end_range = 2 ** bits - 1
                start_range = f"{start_range:X}"
                end_range = f"{end_range:X}"
        except ValueError:
            range_message = "Range should be in Bit 1-256 "
            QMessageBox.information(self, "Range Error", range_message)

    def calculate_percentage(self):
        try:
            start_hex = self.start_edit.text()
            end_hex = self.end_edit.text()
            start = int(start_hex, 16)
            end = int(end_hex, 16)
            percent = float(self.percentLineEdit.text()) / 100

            total_keys = end - start  # Calculate total keys in the current range

            result = start + int(percent * total_keys)
            result_hex = hex(result).upper().replace("0X", "")
            
            # Calculate percentage based on the current range
            percentage = (result - start) / total_keys * 100

            output = (
                f"Range: {start_hex}:{end_hex}\n"
                f"Result: {result_hex}\n"
                f"Keys in this Range: {int(percent * total_keys):,}\n"
                f"Calculated Percentage: {percentage:.5f}% of Keys in this Range"
            )
            
            self.consoleWindow.append_output(output)
            
            # Update start for the next calculation
            start = result

        except ValueError as e:
            QMessageBox.information(self, "Input Error", str(e))

    def calculate_percentage_and_div_range(self):
        try:
            start_hex = self.start_edit.text()
            end_hex = self.end_edit.text()
            self.start_hex = int(start_hex, 16)
            self.end_hex = int(end_hex, 16)

            num_divs = int(self.format_combo_box_divs.currentText())
            chunk_size = (self.end_hex - self.start_hex) // num_divs
            
            if self.end_hex < self.start_hex:
                error_range = (
                    f'\n\n !!!!!  ERROR !!!!!! \n Your Start HEX {start_hex} is MORE than your Stop HEX {end_hex}'
                )
                self.consoleWindow.append_output(error_range)
            else:
                ranges = [(self.start_hex + i * chunk_size, self.start_hex + (i + 1) * chunk_size) for i in range(num_divs)]
                start_index = self.start_hex
                
                for i, (priv_start, priv_end) in enumerate(ranges, start=1):
                    # Format ranges without '0x' and in uppercase
                    priv_start_hex = f"{priv_start:X}"
                    priv_end_hex = f"{priv_end:X}"
                    
                    percent = float(self.percentLineEdit.text()) / 100
                    start = int(priv_start_hex, 16)
                    end = int(priv_end_hex, 16)
                    
                    total_keys = end - start  # Calculate total keys for the current range
                    result = start + int(percent * total_keys)
                    result_hex = hex(result).upper().replace("0X", "")
                    
                    percentage = (result - start) / total_keys * 100

                    percentage_output = (
                        f"Range {i}:\t{priv_start_hex} - {priv_end_hex}\n"
                        f"Result: {result_hex}\n"
                        f"Keys in this Range: {int(percent * total_keys):,}\n"
                        f"Calculated Percentage: {percentage:.5f}%\n"
                    )
                    
                    if start_index >= priv_start and start_index < priv_end:
                        percentage_output += "<<-- Current Range"

                    self.consoleWindow.append_output(percentage_output)
        
        except ValueError as e:
            QMessageBox.information(self, "Input Error", str(e))