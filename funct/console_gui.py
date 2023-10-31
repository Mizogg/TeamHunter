"""

@author: Team Mizogg
"""
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSlot

class ConsoleWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.consoleOutput = QPlainTextEdit(self)
        self.consoleOutput.setReadOnly(True)
        self.consoleOutput.setMinimumSize(300, 250)
        self.layout.addWidget(self.consoleOutput)

        # Create a widget for the buttons
        button_widget = QWidget(self)
        button_layout = QHBoxLayout(button_widget)

        self.clearButton = QPushButton("Clear", self)
        self.clearButton.setStyleSheet(
                "QPushButton { font-size: 16pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 16pt; background-color: #A13316; color: white; }"
            )
        button_layout.addWidget(self.clearButton)

        self.selectAllButton = QPushButton("Select All", self)
        self.selectAllButton.setStyleSheet(
                "QPushButton { font-size: 16pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 16pt; background-color: #A13316; color: white; }"
            )
        button_layout.addWidget(self.selectAllButton)

        self.copyButton = QPushButton("Copy", self)
        self.copyButton.setStyleSheet(
                "QPushButton { font-size: 16pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 16pt; background-color: #A13316; color: white; }"
            )
        button_layout.addWidget(self.copyButton)

        self.layout.addWidget(button_widget)

        self.clearButton.clicked.connect(self.clear_console)
        self.selectAllButton.clicked.connect(self.select_all)
        self.copyButton.clicked.connect(self.copy_text)

    def append_output(self, output):
        self.consoleOutput.appendPlainText(output)

    @pyqtSlot()
    def clear_console(self):
        self.consoleOutput.clear()

    @pyqtSlot()
    def select_all(self):
        self.consoleOutput.selectAll()

    @pyqtSlot()
    def copy_text(self):
        cursor = self.consoleOutput.textCursor()
        selected_text = cursor.selectedText()
        clipboard = QApplication.clipboard()
        clipboard.setText(selected_text)