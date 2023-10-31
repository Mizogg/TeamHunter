"""

@author: Team Mizogg
"""
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QApplication
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QTimer


SKIPED_FILE = 'input/skipped.txt'
# ShowRangesDialog: Custom QDialog for displaying and managing ranges.
class ShowRangesDialog(QDialog):
    def __init__(self, ranges):
        super().__init__()
        self.setWindowTitle("Show Ranges")
        self.setWindowIcon(QIcon('images/ico'))
        self.setMinimumSize(640, 440)
        self.ranges = ranges
        self.hex_mode = False
        self.initUI()     
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        width = self.table.horizontalHeader().length() + 200
        height = min(400, self.table.rowCount() * 200)
        self.setFixedSize(width, height)

    def initUI(self):
        # Initialize the user interface components.
        layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()

        # Toggle Hex/Decimal button
        self.toggle_button = QPushButton("Switch to Decimal" if not self.hex_mode else "Switch to HEX")
        self.toggle_button.setFixedWidth(200)
        self.toggle_button.clicked.connect(self.toggle_view)
        button_layout.addWidget(self.toggle_button)

        # Copy to Clipboard button
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.setFixedWidth(200)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(self.copy_button)
        
        layout.addLayout(button_layout)

        # Table for displaying ranges
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Start", "End", "Delete"])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)

        # Populate table with ranges
        for i, (start, end) in enumerate(self.ranges):
            self.add_range_row(i, start, end)

        layout.addWidget(self.table)
        
    def copy_to_clipboard(self):
        # Copy ranges to clipboard
        with open(SKIPED_FILE, 'r') as f:
            clipboard_text = f.read()

        clipboard = QApplication.clipboard()
        clipboard.setText(clipboard_text)
        
        self.copy_button.setText("Copied!")
        
        timer = QTimer(self)
        timer.timeout.connect(lambda: self.copy_button.setText("Copy to Clipboard"))
        timer.start(2000)

    def add_range_row(self, row, start, end):
        # Add a row to the table for a range
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(self.to_dec(start) if self.hex_mode else str(start)))
        self.table.setItem(row, 1, QTableWidgetItem(self.to_dec(end) if self.hex_mode else str(end)))

        delete_button = QPushButton("Delete")
        delete_button.setStyleSheet("color: red")
        delete_button.clicked.connect(lambda _, row=row: self.delete_row(row))
        self.table.setCellWidget(row, 2, delete_button)

    def toggle_view(self):
        # Toggle between Hex and Decimal view
        self.hex_mode = not self.hex_mode
        self.toggle_button.setText("Switch to Decimal" if not self.hex_mode else "Switch to HEX")

        for i in range(self.table.rowCount()):
            start, end = self.ranges[i]
            self.table.item(i, 0).setText(self.to_dec(start) if self.hex_mode else str(start))
            self.table.item(i, 1).setText(self.to_dec(end) if self.hex_mode else str(end))

    def delete_row(self, row):
        if row >= 0 and row < len(self.ranges):
            # Delete a row from the table and update ranges
            self.table.removeRow(row)
            del self.ranges[row]
            self.update_skipped_file()

    def to_dec(self, num):
        return str(int(num,16))


    def update_skipped_file(self):
        # Update the skipped.txt file with current ranges
        with open(SKIPED_FILE, 'w') as f:
            for start, end in self.ranges:
                f.write(f"{start}:{end}\n")
                
    def get_ranges(self):
        # Get the ranges from the table
        ranges = []

        for row in range(self.table.rowCount()):
            start = int(self.table.item(row, 0).text())
            end = int(self.table.item(row, 1).text())
            ranges.append((start, end))  # Append as a tuple

        return ranges