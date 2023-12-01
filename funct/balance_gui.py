"""
@author: Team Mizogg
"""
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from libs import team_balance

ICO_ICON = "images/main/miz.ico"
TITLE_ICON = "images/main/title.png"

class BalanceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("BTC Balance Check")
        self.setWindowIcon(QIcon(f"{ICO_ICON}"))
        self.setMinimumSize(640, 440)
        pixmap = QPixmap(f"{TITLE_ICON}")
        title_label = QLabel()
        title_label.setPixmap(pixmap)
        title_label.setFixedSize(pixmap.size())
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btc_label = QLabel("BTC Address:")
        self.address_input = QLineEdit()
        
        self.Check_button = QPushButton("Check Balance (1,3,bc1)")
        self.cancel_button = QPushButton("Cancel")
        
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.btc_label)
        layout.addWidget(self.address_input)
        layout.addWidget(self.Check_button)
        layout.addWidget(self.cancel_button)
        
        # Create a QLabel for displaying balance information
        self.balance_label = QLabel()
        layout.addWidget(self.balance_label)
        self.setLayout(layout)
        
        self.Check_button.clicked.connect(self.get_balance)
        self.cancel_button.clicked.connect(self.reject)
        
    def get_balance(self):
        # Get the Bitcoin address from the input field
        address = self.address_input.text()
        confirmed_balance_btc, received_btc, unconfirmed_balance_btc, tx_count = team_balance.check_balance(address)
        # Create a formatted string with balance information
        BTCOUT = f"""               BTC Address: {address}
            >> Confirmed Balance: {confirmed_balance_btc:.8f} BTC     >> Unconfirmed Balance: {unconfirmed_balance_btc:.8f} BTC
            >> Total Received: {received_btc:.8f} BTC                 >> Transaction Count: {tx_count}"""

        # Display the balance information (you can show it in a label or text widget)
        self.balance_label.setText(
            BTCOUT
        )
