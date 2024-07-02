"""

@author: Team Mizogg
"""
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QFont, QColor

class CustomProgressBar(QProgressBar):
    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        progress_str = f"Progress: {self.value() / self.maximum() * 100:.5f}%"

        font = QFont("Courier", 10)
        font.setBold(True)
        painter.setFont(font)
        
        if self.value() > 0:
            painter.setPen(QColor("#000000"))

        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, progress_str)