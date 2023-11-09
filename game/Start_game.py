from PyQt6 import uic, QtTest
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from game.speaker import Speaker
import game.tetris as tetris
import sys
import os
import sys
sys.path.extend(['game'])

ICO_ICON = "webfiles/css/images/main/miz.ico"
TITLE_ICON = "webfiles/css/images/main/title.png"

class LauncherWindow(QDialog):
    def __init__(self):
        super(LauncherWindow, self).__init__()
        uic.loadUi("game/UI/Launcher.ui", self)
        self.setWindowTitle("PyQt6 Tetris")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.app = QApplication([])
        self.show()
        #-----------------
        self.buttonLaunch = self.findChild(QPushButton, "LaunchButton")
        self.buttonUpdate = self.findChild(QPushButton, "CheckUpdatesButton")
        self.buttonExit = self.findChild(QPushButton, "ExitButton")
        #-----------------========
        self.buttonLaunch.clicked.connect(self.LaunchPress)
        self.buttonUpdate.clicked.connect(self.UpdatePress)
        self.buttonExit.clicked.connect(self.ExitPress)
        #-----------------========
        self.buttonExit.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        self.buttonUpdate.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        self.buttonLaunch.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        #-----------------
        self.versionText = self.findChild(QLabel, "VersionText")
        self.versionText.setText("ver. 0.6")
                    
    def showLauncher(self):
        self.show()
        self.game.hide()
        self.smoothTransform(630, 360)

    def LaunchPress(self):
        Speaker.playsound(Speaker.obj(Speaker.menu_accept))
        self.smoothTransform(360, 480)
        self.hide()
        self.game = tetris.launchGame()
        self.game.closed.connect(self.showLauncher)

    def UpdatePress(self):
        Speaker.playsound(Speaker.obj(Speaker.menu_accept))
        self.msgBox = QMessageBox(QMessageBox.Icon.Information, "Unavailable", "This feature is currently unavailable", QMessageBox.StandardButton.Ok)

        self.msgBox.exec()

    def ExitPress(self):
        Speaker.playsound(Speaker.obj(Speaker.menu_back))
        self.app.quit()

    def smoothTransform(self, width, height): 
        old_h = self.height()
        old_w = self.width()
        end_x = round(self.x() + ((self.width() - width)/2))
        end_y = round(self.y() + ((self.height() - height)/2))
        tick_duration = 20 #minimal tick duration in ms (one frame when transforming the window) 
        prevH = 9999
        prevW = 9999
        x = self.x()
        y = self.y()
        i = 0
        while not (self.height() == height and self.width() == width):
            i+=1
            diff_h = (height - self.height())/9
            diff_w = (width - self.width())/9
            offset_w = old_w - self.width()
            offset_h = old_h - self.height()
            new_x = round(x + (offset_w/2))
            new_y = round(y + (offset_h/2))
            self.move(new_x, new_y)
            if(i%2==0):Speaker.scroll() #play scrolling sound on every second frame
            if(prevW != diff_w or prevH != diff_h):
                prevW = diff_w
                prevH = diff_h
                self.setFixedHeight(round(self.height() + diff_h))
                self.setFixedWidth( round(self.width() + diff_w))
            else:
                self.move(end_x, end_y)
                self.setFixedHeight(height)
                self.setFixedWidth(width)
                break
            QtTest.QTest.qWait(tick_duration)

def main():
    app = QApplication([])
    window = LauncherWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()