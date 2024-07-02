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
        # Emit the initial command to indicate starting
        self.commandOutput.emit(self.command)

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

            # Read command output line by line and emit each line
            for line in iter(self.process.stdout.readline, ''):
                output = line.rstrip('\n')
                self.commandOutput.emit(output)

            # Close the stdout stream and wait for the process to complete
            self.process.stdout.close()
            self.commandFinished.emit(self.process.wait())

        except Exception as e:
            # Emit any exceptions that occur during command execution
            self.commandOutput.emit(f"Error: {str(e)}")
            self.commandFinished.emit(-1)  # Use a custom error code or handle differently

        finally:
            if self.process and self.process.poll() is None:
                self.process.kill()  # Ensure process termination if not already done

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.kill()  # Terminate the process if running
