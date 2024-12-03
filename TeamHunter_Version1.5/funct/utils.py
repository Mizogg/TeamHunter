import time
import locale
import random
from PyQt6.QtWidgets import QProgressBar, QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QFont, QColor

max_value = 2147483647

class CustomProgressBar(QProgressBar):
    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate progress percentage
        progress = self.value() / self.maximum() * 100

        # Format progress string
        progress_str = f"Progress: {progress:.5f}%"

        font = QFont("Courier", 10)
        font.setBold(True)
        painter.setFont(font)
        
        if self.value() > 0:
            painter.setPen(QColor("#000000"))

        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, progress_str)

def update_per_sec(self, per_sec_edit, total_scanned_edit):
    elapsed_time = time.time() - self.start_time

    if elapsed_time == 0:
        per_sec = 0
    else:
        per_sec = self.counter / elapsed_time

    per_sec = round(per_sec, 2)

    total_scanned_text = total_scanned_edit.text()
    total_scanned = locale.atoi(total_scanned_text) + self.counter

    total_scanned_formatted = locale.format_string("%d", total_scanned, grouping=True)
    per_sec_formatted = locale.format_string("%.2f", per_sec, grouping=True)

    total_scanned_edit.setText(total_scanned_formatted)
    per_sec_edit.setText(per_sec_formatted)
    self.start_time = time.time()
    self.counter = 0

def update_display_random(self, start, end):
    if not self.scanning:
        self.timer.stop()
        return

    def find_valid_key():
        rng = random.SystemRandom()
        self.num = rng.randint(start, end)
        return True

    while not find_valid_key():
        pass

    total_range = end - start
    if total_range == 0:
        scaled_current_step = 0
    else:
        scaled_current_step = (self.num - start) / total_range * max_value

    self.progress_bar.setMaximum(max_value)
    self.progress_bar.setValue(int(scaled_current_step))
    self.generate_crypto()
    self.counter += self.power_format

    QApplication.processEvents()

def update_display_sequence(self, start, end):
    self.num = self.current
    if self.current > end:
        self.timer.stop()
        self.scanning = False
        return

    total_steps = end - start
    update_interval = 1

    while self.num < end and self.scanning:
        current_step = self.num - start
        scaled_current_step = (current_step / total_steps) * max_value
        self.progress_bar.setMaximum(max_value)
        self.progress_bar.setValue(int(scaled_current_step))
        self.generate_crypto()
        self.update_keys_per_sec()
        self.current += self.power_format
        self.counter += self.power_format

        self.num += self.power_format

        if self.num % update_interval == 0:
            QApplication.processEvents()

    self.num = end
    self.scanning = False

def update_display_reverse(self, start, end):
    self.num = self.current
    if self.current < start:
        self.timer.stop()
        self.scanning = False
        return

    total_steps = end - start
    update_interval = 1
    processed_count = 0

    while self.num >= start:
        current_step = end - self.num
        scaled_current_step = ((end - self.num) / total_steps) * max_value
        self.progress_bar.setMaximum(max_value)
        self.progress_bar.setValue(max_value - int(scaled_current_step))
        self.generate_crypto()
        self.update_keys_per_sec()
        self.current -= self.power_format
        self.counter += self.power_format

        self.num -= self.power_format
        processed_count += 1
        if not self.scanning:
            break
        if processed_count >= update_interval:
            processed_count = 0
            QApplication.processEvents()
    self.num = start
    self.scanning = False
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