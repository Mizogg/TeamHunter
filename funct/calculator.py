import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QLCDNumber, QDoubleSpinBox, QFormLayout, QGridLayout, QLineEdit, QAbstractSpinBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut, QPixmap
from PyQt6 import QtGui, QtCore
from libs import secp256k1 as ice, load_bloom, team_brain
from bloomfilter import BloomFilter
import os
from console_gui import ConsoleWindow
from funct import win_gui
addfind = load_bloom.load_bloom_filter()

WINNER_FOUND = "found/found.txt"
IMAGES_MAIN = "images/main/"
ICO_ICON = "images/main/miz.ico"
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap(f"{IMAGES_MAIN}titlesmall.png")
        title_label = QLabel(self)
        title_label.setPixmap(pixmap)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        combined_text = """
        <html><center>
        <font size="6" color="#E7481F">₿🖩 Crytpo Calculator 🖩₿</font>
        </html>
        """

        welcome_label = QLabel(combined_text)
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.consoleWindow = ConsoleWindow(self)
        self.consoleWindow1 = ConsoleWindow(self)
        self.container = QWidget()
        self.layout = QGridLayout()
        
        self.button1 = QPushButton("1")
        self.button2 = QPushButton("2")
        self.button3 = QPushButton("3")
        self.button4 = QPushButton("4")
        self.button5 = QPushButton("5")
        self.button6 = QPushButton("6")
        self.button7 = QPushButton("7")
        self.button8 = QPushButton("8")
        self.button9 = QPushButton("9")
        self.button0 = QPushButton("0")
        self.buttonDot = QPushButton(".")
        self.buttonSign = QPushButton("+/-")
        self.buttonEqual = QPushButton("=")
        self.plusButton = QPushButton("+")
        self.minusButton = QPushButton("-")
        self.multiplyButton = QPushButton("*")
        self.divideButton = QPushButton("/")
        self.modButton = QPushButton("%")
        self.clearAllButton = QPushButton("C")
        self.exponentButton = QPushButton("^")

        self.numInput = QLineEdit("")
        self.numInput.keyPressEvent = self.keyPressEvent

        self.setStyleSheet("QMainWindow{background: #fdfdfd;} \
                    QApplication{background:rgba(76, 175, 80, 0.3);} \
                    QLineEdit{height:55px;font-size:36px;} \
                    QPushButton { font-size: 16pt; background-color: #E7481F; color: white; } \
                    QPushButton:hover { font-size: 16pt; background-color: #A13316; color: white; }")

        self.layout.addWidget(self.numInput, 1, 0, 1, 5)

        self.layout.addWidget(self.exponentButton,2,0,1,1)
        self.layout.addWidget(self.clearAllButton,2,2,1,1)
        self.layout.addWidget(self.modButton,2,1,1,1)
        self.layout.addWidget(title_label,1,5,3,4)
        self.layout.addWidget(welcome_label,3,5,3,4)
        self.layout.addWidget(self.button7,3,0,1,1)
        self.layout.addWidget(self.button8,3,1,1,1)
        self.layout.addWidget(self.button9,3,2,1,1)
        self.layout.addWidget(self.button4,4,0,1,1)
        self.layout.addWidget(self.button5,4,1,1,1)
        self.layout.addWidget(self.button6,4,2,1,1)
        self.layout.addWidget(self.button1,5,0,1,1)
        self.layout.addWidget(self.button2,5,1,1,1)
        self.layout.addWidget(self.button3,5,2,1,1)
        self.layout.addWidget(self.button0,6,1,1,1)
        self.layout.addWidget(self.buttonDot,6,2,1,1)
        self.layout.addWidget(self.buttonSign,6,0,1,1)
        self.layout.addWidget(self.buttonEqual,6,4,1,1)
        self.layout.addWidget(self.plusButton,2,4,1,1)
        self.layout.addWidget(self.minusButton,3,4,1,1)
        self.layout.addWidget(self.multiplyButton,4,4,1,1)
        self.layout.addWidget(self.divideButton,5,4,1,1)
        self.layout.addWidget(self.consoleWindow, 7, 0, 1, 4)
        self.layout.addWidget(self.consoleWindow1, 7, 4, 1, 5)

        self.button0.setCheckable(True)
        self.button1.setCheckable(True)
        self.button2.setCheckable(True)
        self.button3.setCheckable(True)
        self.button4.setCheckable(True)
        self.button5.setCheckable(True)
        self.button6.setCheckable(True)
        self.button7.setCheckable(True)
        self.button8.setCheckable(True)
        self.button9.setCheckable(True)
        self.buttonDot.setCheckable(True)
        self.buttonSign.setCheckable(True)
        self.plusButton.setCheckable(True)
        self.minusButton.setCheckable(True)
        self.multiplyButton.setCheckable(True)
        self.divideButton.setCheckable(True)
        self.plusButton.setCheckable(True)
        self.modButton.setCheckable(True)
        self.exponentButton.setCheckable(True)
        
        self.button0.clicked.connect(self.buttonClicked)
        self.button1.clicked.connect(self.buttonClicked)
        self.button2.clicked.connect(self.buttonClicked)
        self.button3.clicked.connect(self.buttonClicked)
        self.button4.clicked.connect(self.buttonClicked)
        self.button5.clicked.connect(self.buttonClicked)
        self.button6.clicked.connect(self.buttonClicked)
        self.button7.clicked.connect(self.buttonClicked)
        self.button8.clicked.connect(self.buttonClicked)
        self.button9.clicked.connect(self.buttonClicked)
        self.buttonDot.clicked.connect(self.buttonClicked)
        self.buttonSign.clicked.connect(self.buttonClicked)
        self.plusButton.clicked.connect(self.takeInput)
        self.minusButton.clicked.connect(self.takeInput)
        self.multiplyButton.clicked.connect(self.takeInput)
        self.divideButton.clicked.connect(self.takeInput)
        self.modButton.clicked.connect(self.takeInput)
        self.exponentButton.clicked.connect(self.takeInput)        
        self.buttonEqual.clicked.connect(self.calculate)
        self.clearAllButton.clicked.connect(self.numInput.clear)
        
        self.setCentralWidget(self.container)
        self.container.setLayout(self.layout)
        
    def keyPressEvent(self, e):
        if e.text()  == "+":
            self.takeInput()
            self.plusButton.setChecked(True)
        elif e.text()  == "-":
            self.takeInput()
            self.minusButton.setChecked(True)
        elif e.text()  == "*":
            self.takeInput()
            self.multiplyButton.setChecked(True)
        elif e.text()  == "/":
            self.takeInput()
            self.divideButton.setChecked(True)
        elif e.text()  == "%":
            self.takeInput()
            self.modButton.setChecked(True)
        elif e.text()  == "^":
            self.takeInput()
            self.exponentButton.setChecked(True)
        elif e.text()  == "=":
            self.calculate()
        elif e.text() >="0" and e.text()<="9" or e.text()==".":
            prevStr = self.numInput.text()
            self.numInput.setText(prevStr+e.text())
    
    def buttonClicked(self):
        if(self.button0.isChecked()):
            self.check = 0
        elif(self.button1.isChecked()):
            self.check = 1
        elif(self.button2.isChecked()):
            self.check = 2
        elif(self.button3.isChecked()):
            self.check = 3
        elif(self.button4.isChecked()):
            self.check = 4
        elif(self.button5.isChecked()):
            self.check = 5
        elif(self.button6.isChecked()):
            self.check = 6
        elif(self.button7.isChecked()):
            self.check = 7
        elif(self.button8.isChecked()):
            self.check = 8
        elif(self.button9.isChecked()):
            self.check = 9
        elif(self.buttonDot.isChecked()):
            self.check = 10
        elif(self.buttonSign.isChecked()):
            self.check = 11

        if self.check == 0:
            prevStr = self.numInput.text()
            self.numInput.setText(prevStr+"0")
            self.button0.setChecked(False)
        elif self.check == 1:
            prevStr = self.numInput.text()
            self.numInput.setText(prevStr+"1")
            self.button1.setChecked(False)
        elif self.check == 2:
            prevStr = self.numInput.text()
            self.numInput.setText(prevStr+"2")
            self.button2.setChecked(False)
        elif self.check == 3:
            prevStr = self.numInput.text()
            self.numInput.setText(prevStr+"3")
            self.button3.setChecked(False)
        elif self.check == 4:
            prevStr = self.numInput.text()
            self.numInput.setText(prevStr+"4")
            self.button4.setChecked(False)
        elif self.check == 5:
            prevStr = self.numInput.text()
            self.numInput.setText(prevStr+"5")
            self.button5.setChecked(False)
        elif self.check == 6:
            prevStr = self.numInput.text()
            self.numInput.setText(prevStr+"6")
            self.button6.setChecked(False)
        elif self.check == 7:
            prevStr = self.numInput.text()
            self.numInput.setText(prevStr+"7")
            self.button7.setChecked(False)
        elif self.check == 8:
            prevStr = self.numInput.text()
            self.numInput.setText(prevStr+"8")
            self.button8.setChecked(False)
        elif self.check == 9:
            prevStr = self.numInput.text()
            self.numInput.setText(prevStr+"9")
            self.button9.setChecked(False)
        elif self.check == 10:
            prevStr = self.numInput.text()
            self.numInput.setText(prevStr+".")
            self.buttonDot.setChecked(False)
        elif self.check == 11:
            prevStr = self.numInput.text()
            self.numInput.setText("-"+prevStr)
            self.buttonSign.setChecked(False)

    def calculate(self):
        if(self.plusButton.isChecked()):
            self.value = 1
        elif(self.minusButton.isChecked()):
            self.value = 2
        elif(self.multiplyButton.isChecked()):
            self.value = 3
        elif(self.divideButton.isChecked()):
            self.value = 4
        elif(self.modButton.isChecked()):
            self.value = 5
        elif(self.exponentButton.isChecked()):
            self.value = 6
        self.num2 = float(self.numInput.text())
        answer = 0
        if self.value == 1:
            answer = self.num1+self.num2
            self.plusButton.setChecked(False)
        elif self.value == 2:
            answer = self.num1-self.num2
            self.minusButton.setChecked(False)
        elif self.value == 3:
            answer = self.num1*self.num2
            self.multiplyButton.setChecked(False)
        elif self.value == 4:
            answer = self.num1/self.num2
            self.divideButton.setChecked(False)
        elif self.value == 5:
            answer = self.num1%self.num2
            self.modButton.setChecked(False)
        elif self.value == 6:
            answer = pow(self.num1, self.num2)
            self.exponentButton.setChecked(False)
        self.numInput.setText(str(answer))
        self.brains_btc(answer)

    def brains_btc(self, passphrase):
        try:
            wallet = team_brain.BrainWallet()
            private_key, uaddr = wallet.generate_address_from_passphrase(str(passphrase))
            brainvartext = (f'\n\n BrainWallet: {passphrase} \n Private Key In HEX : {private_key} \n Bitcoin Adress : {uaddr}')
            self.consoleWindow.append_output(brainvartext)
            dec_value = str(int(private_key, 16))
            caddr = ice.privatekey_to_address(0, True, int(dec_value))
            uaddrice = ice.privatekey_to_address(0, False, int(dec_value))
            wifc = ice.btc_pvk_to_wif(private_key)
            wifu = ice.btc_pvk_to_wif(private_key, False)
            saddr = ice.privatekey_to_address(1, True, int(dec_value))
            bech32 = ice.privatekey_to_address(2, True, int(dec_value))
            #ethaddr = ice.privatekey_to_ETH_address(int(dec_value))
            out_info = f"""
============ICELANDS LIB Output==========
: Private Key HEX                   : {private_key}
: PrivateKey (dec)                  : {dec_value}
: Private Key WIF UnCompressed      : {wifu}
: BTC Address UnCompressed      : {uaddrice}
: Private Key WIF Compressed        : {wifc}
: BTC Address Compressed        : {caddr}
: BTC Address Segwit            : {saddr}
: BTC Address Bech32            : {bech32}
====================================="""
            self.consoleWindow1.append_output(out_info)
            if caddr in addfind or uaddrice in addfind or saddr in addfind or bech32 in addfind:
                joined_text = f'{brainvartext}{out_info}'
                winner_dialog = win_gui.WinnerDialog(joined_text, self)
                winner_dialog.exec()
                try:
                    with open(WINNER_FOUND, "a") as f:
                        f.write(out_info)
                except FileNotFoundError:
                    os.makedirs(os.path.dirname(WINNER_FOUND), exist_ok=True)

                    with open(WINNER_FOUND, "w") as f:
                        f.write(out_info)

        except ValueError:
            print("Invalid input. Please enter a valid Menmonics.")
        
    def takeInput(self):
        self.num1 = float(self.numInput.text())
        self.numInput.clear()