# -*- coding: utf-8 -*-
"""
@author: Team Mizogg
"""
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import random
import sys
from game.speaker import Speaker

class StartScreen(QWidget):
    startGame = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        combined_text = """
        <html><center>
        <font size="18" color="#E7481F">🐍 Snake Game 🐍</font>
        <br><br><font size="8" color="#E7481F">
        Use the arrow keys to control the snake or "W," "A," "S," "D".
        </font><br>
        <br>
        <br><font size="4">
        This is a classic Snake game.<br>
        Your goal is to control the snake using the arrow keys and collect the Bitcoin (BTC) symbols on the board.<br>
        Be careful not to crash into yourself. AND Donn't Collect Bad Food <br>
        The longer your snake gets, the higher your score! Good luck and have fun!
        </font>
        <br><br><font size="8">
        Image Good food: <img src="webfiles/css/images/main/btc.png">
        <br><br>
        Image Bad food: <img src="webfiles/css/images/main/bad.png">
        <br><br>
        <img src="webfiles/css/images/main/head.png"><img src="webfiles/css/images/main/body.png"><img src="webfiles/css/images/main/body.png"><img src="webfiles/css/images/main/body.png"><img src="webfiles/css/images/main/body.png"><img src="webfiles/css/images/main/body.png"><img src="webfiles/css/images/main/body.png"><img src="webfiles/css/images/main/body.png"><img src="webfiles/css/images/main/body.png"><img src="webfiles/css/images/main/body.png"><img src="webfiles/css/images/main/body.png">
                </font></center><br><br><br></html>
        """
        instructions = QLabel(combined_text)

        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.startButton = QPushButton("Start Game")
        self.startButton.setStyleSheet(
                "QPushButton { font-size: 16pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 16pt; background-color: #A13316; color: white; }"
            )
        self.startButton.clicked.connect(self.start_game)

        layout.addWidget(instructions)
        layout.addWidget(self.startButton)
        self.setLayout(layout)

    def start_game(self):
        self.startGame.emit()

class EndScreen(QWidget):
    restartGame = pyqtSignal()

    def __init__(self, score):
        super().__init__()
        self.initUI(score)

    def initUI(self, score):
        layout = QVBoxLayout()

        gameover_text = (f"""
        <html><center>
        <font size="18" color="#E7481F">🐍 Snake Game 🐍</font>
        <br><br><font size="8" color="#E7481F">
        Game Over
        <br>
        Ammount of Bitcoin: {score}.00000000 BTC
        </font><br>
        <br>

        <br><font size="6">
        Try Again ?
        </font>
        </center><br><br><br></html>
        """)
        gameover_lable = QLabel(gameover_text)
        gameover_lable.setAlignment(Qt.AlignmentFlag.AlignCenter)

        restartButton = QPushButton("Restart Game")
        restartButton.setStyleSheet(
                "QPushButton { font-size: 16pt; background-color: #E7481F; color: white; }"
                "QPushButton:hover { font-size: 16pt; background-color: #A13316; color: white; }"
            )
        restartButton.clicked.connect(self.restart_game)

        layout.addWidget(gameover_lable)
        layout.addWidget(restartButton)
        self.setLayout(layout)

    def restart_game(self):
        self.restartGame.emit()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.start_screen = StartScreen()
        self.setCentralWidget(self.start_screen)
        self.start_screen.startGame.connect(self.start_game)
        self.end_screen = None
        self.board = None  # Add a board attribute


    def start_game(self):
        if self.end_screen:
            self.end_screen.hide()
        if self.board:
            self.board.hide()
        self.start_screen.hide()
        self.board = Board(self)
        self.statusbar = self.statusBar()
        self.statusbar.setStyleSheet("font-size: 16pt; border: 2px solid #E7481F;")
        self.board.msg2statusbar.connect(self.statusbar.showMessage)
        self.board.gameOver.connect(self.game_over)
        self.setCentralWidget(self.board)
        self.board.start()

    def game_over(self, score):
        self.end_screen = EndScreen(score)
        self.setCentralWidget(self.end_screen)
        self.end_screen.restartGame.connect(self.restart_game)
        Speaker.play_death()

    def restart_game(self):
        if self.end_screen:
            self.end_screen.hide()
        self.board = Board(self)
        self.statusbar = self.statusBar()
        self.statusbar.setStyleSheet("font-size: 16pt; border: 2px solid #E7481F;")
        self.board.msg2statusbar.connect(self.statusbar.showMessage)
        self.board.gameOver.connect(self.game_over)
        self.setCentralWidget(self.board)
        self.board.start()

class Board(QFrame):
    msg2statusbar = pyqtSignal(str)
    gameOver = pyqtSignal(int)
    SPEED = 80
    WIDTHINBLOCKS = 60
    HEIGHTINBLOCKS = 40

    def __init__(self, parent):
        super().__init__(parent)
        
        self.timer = QBasicTimer()
        self.snake = [[5, 10], [5, 11]]
        self.current_x_head = self.snake[0][0]
        self.current_y_head = self.snake[0][1]
        self.load_images() 
        
        # Move these initializations up
        self.food = []
        self.food_timestamps = {}  # A dictionary to store timestamps of food items
        self.bad_food = []  # List to keep track of bad food
        
        self.grow_snake = False
        self.board = []
        self.direction = 1
        
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Move the drop_food method call to the end of the __init__ method
        self.drop_food(1, 2)


    def load_images(self):
        image_path = "webfiles/css/images/main/"  # Adjust the path to your image directory
        image_size = (40, 40)  # Adjust the desired image size

        self.dot = QPixmap(image_path + "body.png").scaled(image_size[0], image_size[1])
        self.head = QPixmap(image_path + "head.png").scaled(image_size[0], image_size[1])
        self.apple = QPixmap(image_path + "btc.png").scaled(image_size[0], image_size[1])
        self.bad_apple = QPixmap(image_path + "bad.png").scaled(image_size[0], image_size[1])


    def square_width(self):
        return self.contentsRect().width() / Board.WIDTHINBLOCKS

    def square_height(self):
        return self.contentsRect().height() / Board.HEIGHTINBLOCKS

    def start(self):
        score = str(len(self.snake) - 2)
        score_run = (f"Ammount of Bitcoin: {score}.00000000 BTC")

        self.msg2statusbar.emit(score_run)
        self.timer.start(Board.SPEED, self)


    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardtop = int(rect.bottom() - Board.HEIGHTINBLOCKS * self.square_height())  # Convert to int

        # Scale the images
        head_pixmap = self.head.scaled(int(self.square_width()), int(self.square_height()))
        dot_pixmap = self.dot.scaled(int(self.square_width()), int(self.square_height()))
        apple_pixmap = self.apple.scaled(int(self.square_width()), int(self.square_height()))
        bad_apple_pixmap = self.bad_apple.scaled(int(self.square_width()), int(self.square_height()))


        for pos in self.snake:
            if pos == self.snake[0]:
                painter.drawPixmap(int(rect.left() + pos[0] * self.square_width()),  # Convert to int
                                  int(boardtop + pos[1] * self.square_height()),  # Convert to int
                                  head_pixmap)
            else:
                painter.drawPixmap(int(rect.left() + pos[0] * self.square_width()),  # Convert to int
                                  int(boardtop + pos[1] * self.square_height()),  # Convert to int
                                  dot_pixmap)
        for pos in self.food:
            painter.drawPixmap(int(rect.left() + pos[0] * self.square_width()),  # Convert to int
                              int(boardtop + pos[1] * self.square_height()),  # Convert to int
                              apple_pixmap)
                              
        for pos in self.bad_food:
            painter.drawPixmap(int(rect.left() + pos[0] * self.square_width()),  # Convert to int
                               int(boardtop + pos[1] * self.square_height()),  # Convert to int
                               bad_apple_pixmap)



    def draw_square(self, painter, x, y):
        color = QColor(0x228B22)
        painter.fillRect(int(x + 1), int(y + 1), int(self.square_width() - 2), int(self.square_height() - 2), color)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Left or key == Qt.Key.Key_A:
            if self.direction != 2:
                self.direction = 1
        elif key == Qt.Key.Key_Right or key == Qt.Key.Key_D:
            if self.direction != 1:
                self.direction = 2
        elif key == Qt.Key.Key_Down or key == Qt.Key.Key_S:
            if self.direction != 4:
                self.direction = 3
        elif key == Qt.Key.Key_Up or key == Qt.Key.Key_W:
            if self.direction != 3:
                self.direction = 4


    def move_snake(self):
        if self.direction == 1:
            self.current_x_head, self.current_y_head = self.current_x_head - 1, self.current_y_head
            if self.current_x_head < 0:
                self.current_x_head = Board.WIDTHINBLOCKS - 1
        if self.direction == 2:
            self.current_x_head, self.current_y_head = self.current_x_head + 1, self.current_y_head
            if self.current_x_head == Board.WIDTHINBLOCKS:
                self.current_x_head = 0
        if self.direction == 3:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head + 1
            if self.current_y_head == Board.HEIGHTINBLOCKS:
                self.current_y_head = 0
        if self.direction == 4:
            self.current_x_head, self.current_y_head = self.current_x_head, self.current_y_head - 1
            if self.current_y_head < 0:
                self.current_y_head = Board.HEIGHTINBLOCKS
        head = [self.current_x_head, self.current_y_head]
        self.snake.insert(0, head)
        if not self.grow_snake:
            self.snake.pop()
        else:
            score = str(len(self.snake) - 2)
            score_run = (f"Ammount of Bitcoin: {score}.00000000 BTC")
            self.msg2statusbar.emit(score_run)
            self.grow_snake = False

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.check_for_bad_food()  # Check and update bad food
            self.move_snake()
            self.is_food_collision()
            self.is_suicide()
            self.update()

    def check_for_bad_food(self):
        current_time = QDateTime.currentMSecsSinceEpoch()
        fifteen_seconds = 15 * 1000  # 15000 milliseconds or 15 seconds

        for pos in self.food[:]:
            if current_time - self.food_timestamps[tuple(pos)] >= fifteen_seconds:
                self.food.remove(pos)
                self.bad_food.append(pos)
                del self.food_timestamps[tuple(pos)]  # Remove the timestamp entry


    def is_suicide(self):
        for i in range(1, len(self.snake)):
            if self.snake[i] == self.snake[0]:
                self.gameOver.emit(len(self.snake) - 2)
                self.timer.stop()

    def is_food_collision(self):
        for pos in self.food[:]:
            if pos == self.snake[0]:
                self.food.remove(pos)
                self.drop_food(1, 2)
                self.grow_snake = True
                Speaker.playsound(Speaker.obj(Speaker.row_deleted), 0.2)

        for pos in self.bad_food:
            if pos == self.snake[0]:
                self.gameOver.emit(len(self.snake) - 2)
                self.timer.stop()

    def drop_food(self, min_food=1, max_food=1):
        num_food = random.randint(min_food, max_food)
        current_time = QDateTime.currentMSecsSinceEpoch()

        for _ in range(num_food):
            while True:
                x = random.randint(3, 58)
                y = random.randint(3, 38)
                if all(pos != [x, y] for pos in self.food) and \
                   all(pos != [x, y] for pos in self.bad_food) and \
                   all(pos != [x, y] for pos in self.snake):
                    self.food.append([x, y])
                    self.food_timestamps[(x, y)] = current_time  # Store the timestamp
                    break



def main():
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()