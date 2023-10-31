"""
@author: Team Mizogg
"""
import subprocess
from PyQt6.QtCore import QThread, pyqtSignal

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
            self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, encoding='utf-8'
        )
        for line in self.process.stdout:
            output = line.strip()
            self.commandOutput.emit(output)
        self.process.stdout.close()
        self.commandFinished.emit(self.process.wait())