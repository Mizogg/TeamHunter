"""

@author: Team Mizogg
"""
import random
from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtCore import Qt, QObject, pyqtSignal
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

class MatrixDrop:
    def __init__(self, col, max_rows):
        self.col = col
        self.max_rows = max_rows
        self.row = random.randint(-10, -1)
        self.speed = random.randint(1, 3)

    def move(self):
        self.row += self.speed

    def is_visible(self):
        return 0 <= self.row < self.max_rows

class Smoke_up:
    def __init__(self, row, col, max_rows):
        self.row = row
        self.col = col
        self.max_rows = max_rows
        self.speed = random.randint(1, 5)
        self.ttl = random.randint(15, 30)

    def move(self):
        self.row -= self.speed
        self.ttl -= 1

    def is_visible(self):
        return 0 <= self.row < self.max_rows and self.ttl > 0

class LavaBubble:
    def __init__(self, row, col, max_rows):
        self.row = row
        self.col = col
        self.max_rows = max_rows
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.randint(1, 3)
        self.ttl = random.randint(15, 30)

    def move(self):
        self.row += self.direction * self.speed
        self.ttl -= 1
        if random.random() < 0.1:
            self.direction *= -1

    def is_visible(self):
        return 0 <= self.row < self.max_rows and self.ttl > 0

class blocking_grid:
    def __init__(self, row, col, max_rows):
        self.row = row
        self.col = col
        self.max_rows = max_rows
        self.speed = random.randint(1, 5)
        self.ttl = random.randint(15, 30)
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

    def move(self):

        self.row += self.direction[0] * self.speed
        self.col += self.direction[1] * self.speed
        self.row = max(0, min(self.row, self.max_rows - 1))
        self.col = max(0, min(self.col, self.max_rows - 1))
        
        self.ttl -= 1

        if random.random() < 0.2:
            self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])

    def is_visible(self):
        return 0 <= self.row < self.max_rows and self.ttl > 0