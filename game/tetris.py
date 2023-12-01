from PyQt6 import uic, QtTest
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from game.speaker import Speaker
import game.aboutWindow as aboutWindow
import keyboard
import random
        
ICO_ICON = "images/main/miz.ico"
TITLE_ICON = "images/main/title.png"
                                     
S = [['.....','..00.','.00..','.....','.....'],['..0..','..00.','...0.','.....','.....']]
Z = [['.....','.00..','..00.','.....','.....'],['..0..','.00..','.0...','.....','.....']]
I = [['..0..','..0..','..0..','..0..','.....'],['.....','.....','0000.','.....','.....']]
O = [['.....','.00..','.00..','.....','.....']]
J = [['.....','.0...','.000.','.....','.....'],['.....','..00.','..0..','..0..','.....'],
     ['.....','.....','.000.','...0.','.....'],['.....','..0..','..0..','.00..','.....']]
L = [['.....','...0.','.000.','.....','.....'],['.....','..0..','..0..','..00.','.....'],
     ['.....','.....','.000.','.0...','.....'],['.....','.00..','..0..','..0..','.....']]
T = [['.....','..0..','.000.','.....','.....'],['.....','..0..','..00.','..0..','.....'],
     ['.....','.....','.000.','..0..','.....'],['.....','..0..','.00..','..0..','.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [1,2,3,4,5,6,7]
color_palettes = [
    [QColor(0,88,248),  QColor(60,188,252), QColor(0,88,248),   QColor(203,232,247),QColor(0,165,247),  QColor(73,91,205),  QColor(0,247,221)   ],#0
    [QColor(0,168,0),   QColor(110,173,110),QColor(184,248,24), QColor(200,239,200),QColor(0,236,0),    QColor(104,151,104),QColor(163,255,179) ],#1
    [QColor(216,0,204), QColor(248,120,248),QColor(204,0,183),  QColor(206,192,204),QColor(176,0,218),  QColor(214,104,227),QColor(218,0,169)   ],#2
    [QColor(0,88,248),  QColor(123,168,249),QColor(88,216,84),  QColor(9,216,3),    QColor(190,216,190),QColor(197,214,246),QColor(3,216,175)   ],#3
    [QColor(228,0,88),  QColor(88,248,152), QColor(228,63,127), QColor(3,242,99),   QColor(228,141,175),QColor(211,246,225),QColor(242,94,94)   ],#4
    [QColor(88,248,152),QColor(104,136,252),QColor(3,249,101),  QColor(12,63,250),  QColor(139,249,183),QColor(218,226,254),QColor(58,246,97)   ],#5
    [QColor(248,56,0),  QColor(124,124,124),QColor(246,99,56),  QColor(183,183,183),QColor(249,144,113),QColor(203,178,162),QColor(247,202,189) ],#6
    [QColor(104,68,252),QColor(168,0,32),   QColor(161,139,250),QColor(167,42,66),  QColor(199,186,250),QColor(166,79,96),  QColor(64,20,247)   ],#7
    [QColor(0,88,248),  QColor(248,56,0),   QColor(67,132,250), QColor(246,100,58), QColor(130,173,251),QColor(246,166,142),QColor(188,210,250) ],#8
    [QColor(248,56,0),  QColor(252,160,68), QColor(246,95,51),  QColor(250,185,121),QColor(246,140,109),QColor(246,217,188),QColor(250,191,174) ],#9
     ]

#=====TETRIS FUNCTIONS======================================================================

class Figure(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def createField(locked_pos={}):
    board = [[0 for _ in range(15)] for _ in range(22)]

    for i in range(len(board)):
        for j in range(len(board[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                board[i][j] = c
    return board

def getShape():
    return Figure(7, 1, random.choice(shapes))

def convertShapeFormat(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j , shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0]-2, pos[1]-1)
    return positions

def validSpace(shape, board):
    accepted_pos = [[(j, i) for j in range(15) if board[i][j] == 0] for i in range(22)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convertShapeFormat(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def checkLost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def tryRotate(info):
    info.current_piece.rotation += 1
    if not (validSpace(info.current_piece, info.board)):
        info.current_piece.rotation -= 1
    else:
        Speaker.playsound(Speaker.obj(Speaker.generic_scroll_01), 0.3)

def tryMoveLeft(info):
    info.current_piece.x -= 1
    if not (validSpace(info.current_piece, info.board)):
        info.current_piece.x += 1
    else:
        Speaker.playsound(Speaker.obj(Speaker.generic_scroll_01), 0.3)

def tryMoveRight(info):
    info.current_piece.x += 1
    if not (validSpace(info.current_piece, info.board)):
        info.current_piece.x -= 1
    else:
        Speaker.playsound(Speaker.obj(Speaker.generic_scroll_01), 0.3)

def tryMoveDown(info):
    info.current_piece.y += 1
    if not (validSpace(info.current_piece, info.board)):
        info.current_piece.y -= 1
    else:
        Speaker.playsound(Speaker.obj(Speaker.generic_scroll_01), 0.3)

def clearRows(info, self):
    inc = 0
    for i in range(len(info.board)-1, -1, -1):
        row = info.board[i]
        if 0 not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del info.locked_positions[(j,i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(info.locked_positions), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                info.locked_positions[newKey] = info.locked_positions.pop(key)
    score_map = {0:0, 1:60, 2:120, 3:360, 4:1800}   
    if inc != 0:
        Speaker.playsound(Speaker.obj(Speaker.row_deleted), 0.2)
    prevLevel = checkLevel(info, True)
    info.lines += inc
    info.score += score_map[inc]*(info.level+1)
    checkLevel(info, False, prevLevel, self)
    self.levelText.setText("Level : " + str(info.level))
    self.scoreText.setText("Score : " + str(info.score))

def checkLevel(info, shouldReturn = False, prevLevel = 123, self = None):
    if shouldReturn:
        return info.level
    info.level = info.lines//10
    if prevLevel != 123:
        if prevLevel < info.level:
            playLevelSound(info.level, self)
    checkSpeed(info)

def checkSpeed(info):
    info.speed = info.level//2
    if info.level > 20:
        info.speed = 10

def playLevelSound(cur_lev, self):
    playTextAnimation(self)
    level = cur_lev%5
    if level == 0:
        Speaker.playsound(Speaker.obj(Speaker.lvl1), 0.4)
    if level == 1:
        Speaker.playsound(Speaker.obj(Speaker.lvl2), 0.4)
    if level == 2:
        Speaker.playsound(Speaker.obj(Speaker.lvl3), 0.4)
    if level == 3:
        Speaker.playsound(Speaker.obj(Speaker.lvl4), 0.4)
    if level == 4:
        Speaker.playsound(Speaker.obj(Speaker.lvl5), 0.4)

def playTextAnimation(self):
    self.animation = QPropertyAnimation(self.levelText, b'margin')
    self.animation.setStartValue(70)
    self.animation.setEndValue(0)
    self.animation.setDuration(1000)
    self.animation.setEasingCurve(QEasingCurve.Type.OutElastic)
    self.animation.start()

#=====QT CLASSES n WINDOWS=====================================================================================

class PlayWindow(QDialog):
    closed = pyqtSignal()   
    def __init__(self, info):
        self.needsReset = 0
        super(PlayWindow, self).__init__()
        uic.loadUi("game/UI/PlayWindow.ui", self)
        self.setWindowTitle("PyQt6 Tetris (Game window)")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        Speaker.play_background_music()
        self.pause = 1
        #-----------------
        self.buttonExit = self.findChild(QPushButton, "ExitButton")
        self.tableWidget = self.findChild(QTableWidget, "PlayTable")
        self.figureWidget = self.findChild(QTableWidget, "FigureWindow")
        self.buttonPause = self.findChild(QPushButton, "PauseButton")
        self.timeText = self.findChild(QLabel, "TimeText")
        self.levelText = self.findChild(QLabel, "LevelText")
        self.scoreText = self.findChild(QLabel, "ScoreText")
        self.linesText = self.findChild(QLabel, "LinesText")
        #-----------------
        self.buttonPause.clicked.connect(self.PausePress)
        self.buttonPause.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        self.buttonExit.clicked.connect(self.ExitB)
        self.buttonExit.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        #-----------------
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.figureWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.figureWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.gameTimer = QTimer()
        self.gameTimer.setInterval(25)
        self.gameTimer.timeout.connect(lambda: self.GameStateUpdate(info))
        self.time = 0
        self.buttonPause.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.buttonExit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.wasd_space = [0,0,0,0,0]

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_W or event.key() == Qt.Key.Key_Up:
            self.wasd_space[0] = 1
        if event.key() == Qt.Key.Key_A or event.key() == Qt.Key.Key_Left:
            self.wasd_space[1] = 1
        if event.key() == Qt.Key.Key_S or event.key() == Qt.Key.Key_Down:
            self.wasd_space[2] = 1
        if event.key() == Qt.Key.Key_D or event.key() == Qt.Key.Key_Right:
            self.wasd_space[3] = 1
        if event.key() == Qt.Key.Key_Space:
            self.wasd_space[4] = 1


    def GameStateUpdate(self, info):
        if(self.needsReset == 1):
            self.time = 0
            self.pause = 0
            self.PauseGame()
            self.gameTimer.stop()
            info.reset()
            for y in range(20):
                for x in range(15):
                    self.tableWidget.setItem(y, x, QTableWidgetItem(None))
            for y in range(5):
                for x in range(5):
                    self.figureWidget.setItem(y, x, QTableWidgetItem(None))
            self.buttonPause.setEnabled(True)
            self.buttonPause.setStyleSheet("""
                QPushButton {
                background-color: rgba(255, 255, 255, 0);
                border: 0;
                color: rgb(150, 150, 150);
                }
                QPushButton:hover{
                background-color: rgba(255, 255, 255, 45);
                color: rgb(255,255,255);
                }
            """)
            self.buttonPause.setText("Start")
            self.scoreText.setText("Score : 0")
            self.levelText.setText("Level : 0")
            self.linesText.setText("Lines : 0")
            self.timeText.setText("Time passed : 0")
            self.needsReset = 0

        if(self.pause != 1):

            self.time += 1

            info.board = createField(info.locked_positions)

            if (self.time % (11-info.speed) == 0):
                info.current_piece.y += 1
                Speaker.playsound(Speaker.obj(Speaker.generic_scroll_01), 0.15)

            if not(validSpace(info.current_piece, info.board)) and info.current_piece.y > 0:
                info.current_piece.y -= 1
                info.change_piece = True

            #==checking=for=input========================================================================

            if self.wasd_space[0] == 1:
                tryRotate(info)
                self.wasd_space [0] = 0

            if self.wasd_space[1] == 1:
                tryMoveLeft(info)
                self.wasd_space[1] = 0

            if (keyboard.is_pressed('s') or keyboard.is_pressed('down') or self.wasd_space[2] == 1):
                if (self.time % 2 == 0) :
                    tryMoveDown(info)
                    self.wasd_space[2] = 0

            if self.wasd_space[3] == 1:
                tryMoveRight(info)
                self.wasd_space[3] = 0
                                
            if self.wasd_space[4] == 1:
                for i in range(22):
                    info.current_piece.y += 1
                    if not(validSpace(info.current_piece, info.board)) and info.current_piece.y > 0:
                        info.current_piece.y -= 1
                        info.change_piece = True
                        break
                self.wasd_space[4] = 0

            if keyboard.is_pressed('p'):
                info.lines += 2
                info.score += 40
                self.time += 85

            #============================================================================================

            current_piece_blocks = convertShapeFormat(info.current_piece)

            for block in current_piece_blocks:
                x, y = block
                info.board[y][x] = info.current_piece.color

            if info.change_piece:
                Speaker.playsound(Speaker.obj(Speaker.block_fallen), 0.5)
                for block in current_piece_blocks:
                    info.locked_positions[block] = info.current_piece.color
                info.current_piece = info.next_piece
                info.next_piece = getShape()
                info.change_piece = False
                clearRows(info, self)

            if checkLost(info.locked_positions):
                self.timeText.setText("Game Over!")
                self.PauseGame()
                self.buttonPause.setEnabled(False)
                self.buttonPause.setStyleSheet("""
                    QPushButton {
                    background-color: rgba(255, 150, 150, 45);
                    border: 0;
                    color: rgb(20, 20, 20);
                    }
                    QPushButton:hover{
                    background-color: rgba(255, 150, 150, 65);
                    color: rgb(20,20,20);
                    }
                """)
                self.leadb = Leaderboard(info, self.time)
                self.leadb.closed.connect(self.leadbClosed)
                self.leadb.show()    
                
            self.UpdateCell(info)
            self.UpdatePreview(info)
            self.timeText.setText("Time passed : " + str(self.time//20) + "s")
            self.LinesText.setText("Lines : " + str(info.lines))

    def UpdateCell(self, info):
        for y in range(20):
            for x in range(15):
                item = info.board[y+2][x]
                tableWidgetItem = QTableWidgetItem(str(item))
                self.tableWidget.setItem(y, x, tableWidgetItem)
                if(self.tableWidget.item(y,x).text() == '0'):
                    blockColor = QColor(0,0,0)
                else:
                    blockColor = color_palettes[info.level%10][(int(self.tableWidget.item(y,x).text()) - 1)]     
                self.tableWidget.item(y, x).setBackground(blockColor)

    def UpdatePreview(self, info):
        for y in range(5):
            for x in range(5):
                self.figureWidget.setItem(y, x, QTableWidgetItem(str('.')))
        blockColor = color_palettes[info.level%10][(info.next_piece.color -1)]
        format = info.next_piece.shape[info.next_piece.rotation % len(info.next_piece.shape)]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '.':
                    self.figureWidget.item(i, j).setBackground(QColor(0,0,0))
                if column == '0':
                    self.figureWidget.item(i, j).setBackground(blockColor)

    def leadbClosed(self):
        self.leadb.hide()
        for y in range(20):
            for x in range(15):
                self.tableWidget.setItem(y, x, QTableWidgetItem(str('.')))
                self.tableWidget.item(y, x).setBackground(QColor(255,255,255))
                QtTest.QTest.qWait(1)
        self.close()

    def PauseGame(self):    
        if(self.pause):
            self.buttonPause.setStyleSheet("""
                QPushButton {
                background-color: rgba(255, 255, 255, 45);
                color: rgb(255,255,255);
                border: 0;
                }
                QPushButton:hover{
                background-color: rgba(255, 255, 255, 65);
                color: rgb(255,255,255);
                }
            """)
            self.buttonPause.setText("Pause")
            self.pause = 0
            self.gameTimer.start()
        else:
            self.buttonPause.setStyleSheet("""
                QPushButton {
                background-color: rgba(255, 255, 255, 0);
                border: 0;
                color: rgb(150, 150, 150);
                }
                QPushButton:hover{
                background-color: rgba(255, 255, 255, 45);
                color: rgb(255,255,255);
                }
            """)
            self.buttonPause.setText("Start")
            self.pause = 1

    def PausePress(self):
        if self.pause:
            Speaker.playsound(Speaker.obj(Speaker.menu_accept))
        self.PauseGame()

    def ExitB(self):         
        Speaker.playsound(Speaker.obj(Speaker.menu_back))
        self.close()

    def closeEvent(self, event):
        self.needsReset = 1
        self.closed.emit()
        QDialog.closeEvent(self, event)

class Leaderboard(QDialog):
    closed = pyqtSignal()
    def __init__(self, info, time):
        super(Leaderboard, self).__init__()
        uic.loadUi("game/UI/Leaderboard.ui", self)
        self.setWindowTitle("PyQt6 Tetris (Leaderboard)")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.buttonClose = self.findChild(QPushButton, "CloseButton")
        self.buttonClose.clicked.connect(self.CloseWindow)
        self.scoreText = self.findChild(QLabel, "ScoreText")
        self.timeText = self.findChild(QLabel, "TimeText")
        self.levelText = self.findChild(QLabel, "LevelText")
        #------------
        self.timeText.setText("Time : " + str(time//20) + "s")
        self.scoreText.setText("Score : " + str(info.score))
        self.levelText.setText("Level : " + str(info.level))
        Speaker.play_death()

    def CloseWindow(self):
        Speaker.stop_background_music()
        self.close()
         
    def closeEvent(self, event):
        Speaker.stop_background_music()  # Stop the background music
        self.closed.emit()
        QDialog.closeEvent(self, event)
                                                                 
class StartWindow(QDialog):
    closed = pyqtSignal()
    def __init__(self, info):
        super(StartWindow, self).__init__()
        uic.loadUi("game/UI/Title.ui", self)
        self.setWindowTitle("PyQt6 Tetris (Start window)")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.show()
        #------------
        self.info = info
        self.buttonStart = self.findChild(QPushButton, "StartButton")
        self.buttonAbout = self.findChild(QPushButton, "AboutButton")
        self.buttonExit = self.findChild(QPushButton, "ExitButton")
        #------------
        self.buttonStart.clicked.connect(self.StartB)
        self.buttonAbout.clicked.connect(self.AboutB)
        self.buttonExit.clicked.connect(self.ExitB)
        #------------
        self.buttonStart.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        self.buttonAbout.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        self.buttonExit.enterEvent = lambda e: Speaker.playsound(Speaker.obj(Speaker.menu_focus))
        #-----------------
        self.mainw = PlayWindow(info)
        self.mainw.closed.connect(self.showStart)

    def showStart(self):        
        self.show()
        self.mainw.hide()
        self.smoothTransform(360, 480)

    def StartB(self):
        Speaker.playsound(Speaker.obj(Speaker.menu_accept))
        self.smoothTransform(640, 480)
        self.hide()
        self.mainw.show()

    def smoothTransform(self, width, height): 
        old_h = self.height()
        old_w = self.width()
        end_x = round(self.x() + ((self.width() - width)/2))
        end_y = round(self.y() + ((self.height() - height)/2))
        tick_duration = 20 
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
            if(i%2==0):Speaker.scroll()
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

    def AboutB(self):
        Speaker.playsound(Speaker.obj(Speaker.menu_accept))
        self.msgBox = aboutWindow.TetrisAboutWindow()
        self.msgBox.show()

    def ExitB(self):
        Speaker.playsound(Speaker.obj(Speaker.menu_back))
        self.close()

    def closeEvent(self, event):  
        Speaker.stop_background_music()      
        self.closed.emit()
        QDialog.closeEvent(self, event)

class GameInfo():

    def __init__(self, locked_positions, board, change_piece, current_piece, next_piece, score, lines, level, speed):
        self.locked_positions = locked_positions
        self.board = board
        self.change_piece = change_piece
        self.current_piece = current_piece
        self.next_piece = next_piece
        self.score = score
        self.lines = lines
        self.level = level
        self.speed = speed

    def reset(self):
        self.locked_positions = {}
        self.board = createField(self.locked_positions)
        self.change_piece = False
        self.current_piece = getShape()
        self.next_piece = getShape()
        self.score = 0
        self.lines = 0
        self.level = 0
        self.speed = 0

#=================================##=================================#

def launchGame():
    locked_positions = {}
    board = createField(locked_positions)
    change_piece = False
    current_piece = getShape()
    next_piece = getShape()
    score = 0
    lines = 0
    level = 0
    speed = 0
    info = GameInfo(locked_positions, board, change_piece, current_piece, next_piece, score, lines, level, speed)
    UIWindow = StartWindow(info)
    return UIWindow

#=================================##=================================#
