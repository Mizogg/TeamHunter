"""

@author: Team Mizogg
"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QPlainTextEdit, QComboBox, QHBoxLayout
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import Qt

ICO_ICON = "webfiles/css/images/main/miz.ico"
TITLE_ICON = "webfiles/css/images/main/title.png"

class RangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Range Divsion Tools ")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.setMinimumSize(640, 440)
        pixmap = QPixmap(f"{TITLE_ICON}")
        # Create a QLabel and set the pixmap as its content
        title_label = QLabel()
        title_label.setPixmap(pixmap)
        title_label.setFixedSize(pixmap.size())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hex_label = QLabel("HEX  Start:")
        self.hex_input_edit = QLineEdit()
        self.hex_label_stop = QLabel("HEX  Stop:")
        self.hex_input_edit_stop = QLineEdit()
        
        power_label = QLabel("Show")
        power_label.setObjectName("powerLabel")
        self.format_combo_box_divs = QComboBox()
        self.format_combo_box_divs.addItems(
            ['2', '4', '8', '16', '32', '64', '128', '256', '512', '1024', '2048', '4096', '8192', '16384', '32768', '65536']
        )
        select_power_layout = QHBoxLayout()
        select_power_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        select_power_layout.addWidget(power_label)
        select_power_layout.addWidget(self.format_combo_box_divs)
        
        self.Check_button = QPushButton("Check")
        self.Check_button.setStyleSheet(
                "QPushButton { font-size: 16pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 16pt; background-color: #A13316; color: white; }"
            )
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(
            "QPushButton { font-size: 16pt; background-color: #1E1E1E; color: white; }"
            "QPushButton:hover { font-size: 16pt; background-color: #5D6062; color: white; }"
        )
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.hex_label)
        layout.addWidget(self.hex_input_edit)
        layout.addWidget(self.hex_label_stop)
        layout.addWidget(self.hex_input_edit_stop)
        layout.addLayout(select_power_layout)
        layout.addWidget(self.Check_button)
        layout.addWidget(self.cancel_button)

        self.output_label = QPlainTextEdit()
        self.output_label.setReadOnly(True)
        self.output_label.setFont(QFont("Courier"))
        layout.addWidget(self.output_label)
        self.setLayout(layout)

        self.Check_button.clicked.connect(self.div_range)
        self.cancel_button.clicked.connect(self.reject)

    def div_range(self):
        start_value = self.hex_input_edit.text()
        end_value = self.hex_input_edit_stop.text()
        num_divs = int(self.format_combo_box_divs.currentText())
        try:
            self.start_hex = int(start_value, 16)
            self.end_hex = int(end_value, 16)
            chunk_size = (self.end_hex - self.start_hex) // num_divs
            if self.end_hex < self.start_hex:
                error_range= (f'\n\n !!!!!  ERROR !!!!!! \n Your Start HEX {start_value} is MORE that your Stop HEX {end_value}')

            else:
                ranges = [(self.start_hex + i * chunk_size, self.start_hex + (i + 1) * chunk_size) for i in range(num_divs)]
                start_index = self.start_hex
                for i in range(num_divs - 1, -1, -1):
                    priv_start = ranges[i][0]
                    priv_end = ranges[i][1]
                    if start_index >= priv_start and start_index < priv_end:
                        displayprint = f' Range {i + 1}:\t{hex(priv_start)} - {hex(priv_end)}\t<<-- Current Range'
                        self.output_label.appendPlainText(displayprint)
                    else:
                        displayprint = f' Range {i + 1}:\t{hex(priv_start)} - {hex(priv_end)}'
                        self.output_label.appendPlainText(displayprint)
        except ValueError:
            self.output_label.appendPlainText("Invalid input. Please enter a Check Ranges.")