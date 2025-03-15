"""
@author: Team Mizogg
"""
import subprocess
import platform
from PyQt6.QtCore import QThread, pyqtSignal

class CommandThread(QThread):
    commandOutput = pyqtSignal(str)
    commandFinished = pyqtSignal(int)

    def __init__(self, command):
        super().__init__()
        self.command = command
        self.process = None

    def run(self):
        self.commandOutput.emit(" ".join(self.command)) 

        try:
            if platform.system() == "Windows":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                self.process = subprocess.Popen(
                    self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', startupinfo=startupinfo
                )
            elif platform.system() == "Linux":
                self.process = subprocess.Popen(
                    self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8'
                )
            else:
                raise NotImplementedError(f"Unsupported platform: {platform.system()}")

            for line in iter(self.process.stdout.readline, ''):
                output = line.rstrip('\n')
                self.commandOutput.emit(output)

            self.process.stdout.close()
            self.commandFinished.emit(self.process.wait())

        except Exception as e:
            self.commandOutput.emit(f"Error: {str(e)}")
            self.commandFinished.emit(-1)

        finally:
            if self.process and self.process.poll() is None:
                self.process.kill()

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.kill()
