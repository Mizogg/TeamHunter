"""
@author: Team Mizogg
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QTextBrowser, 
                           QPushButton, QScrollArea, QWidget)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
from game.speaker import Speaker
import webbrowser
import platform

version = '1.6'

ICO_ICON = "images/main/miz.ico"
TITLE_ICON = "images/main/title.png"
RED_ICON = "images/main/mizogg-eyes.png"

def open_website():
    webbrowser.open("https://mizogg.co.uk")

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About TeamHunter")
        self.setWindowIcon(QIcon(ICO_ICON))
        self.setMinimumSize(900, 700)

        # Create main layout
        main_layout = QVBoxLayout()
        
        # Header
        header_pixmap = QPixmap(TITLE_ICON)
        header_label = QLabel()
        header_label.setPixmap(header_pixmap)
        main_layout.addWidget(header_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Create a single text browser for all content
        content_browser = QTextBrowser()
        current_platform = platform.system()
        
        # Combine all content into one HTML document
        content_browser.setHtml(f"""
        <div style='text-align: center;'>
            <h1 style='margin-bottom: 20px;'>TeamHunter Puzzles GUI</h1>
            <h2 style=''>Version {version} ({current_platform})</h2>
            <p style='font-size: 16px; margin: 10px 0;'>Created by Team Mizogg</p>
        </div>
        
        <div style='margin-top: 30px;'>
            <h2 style='border-bottom: 1px solid #E7481F; padding-bottom: 5px;'>About TeamHunter</h2>
            <p>A comprehensive suite of Bitcoin tools designed for cryptocurrency enthusiasts, 
            researchers, and developers. TeamHunter combines multiple powerful utilities into 
            one user-friendly interface.</p>
            
            <h3>Features:</h3>
            <ul>
                <li>Advanced cryptographic operations</li>
                <li>Multiple search algorithms and methods</li>
                <li>Support for CPU and GPU processing</li>
                <li>Real-time monitoring and statistics</li>
                <li>Customizable search parameters</li>
                <li>User-friendly interface with dark mode</li>
            </ul>
            
            <h3>System Requirements:</h3>
            <ul>
                <li>Operating System: Windows 10/11, Linux</li>
                <li>Minimum RAM: 4GB (8GB+ recommended)</li>
                <li>Storage: 1GB free space</li>
                <li>Python 3.7 or higher</li>
                <li>GPU: Optional but recommended</li>
            </ul>
        </div>
        
        <div style='margin-top: 30px;'>
            <h2 style='border-bottom: 1px solid #E7481F; padding-bottom: 5px;'>Available Tools</h2>
            
            <h3>Core Tools:</h3>
            <ul>
                <li><b>BitCrack:</b> GPU-accelerated Bitcoin private key recovery tool</li>
                <li><b>VanBit:</b> Tool for generating vanity Bitcoin addresses</li>
                <li><b>KeyHunt:</b> Tool for hunting Bitcoin private keys</li>
                <li><b>Iceland2k14 Secp256k1:</b> Specialized cryptographic tools</li>
            </ul>
            
            <h3>Additional Tools:</h3>
            <ul>
                <li><b>Miz Mnemonic:</b> BIP39 mnemonic phrase generator and validator</li>
                <li><b>Brain Hunter:</b> Brain wallet generator and scanner</li>
                <li><b>Miz Poetry:</b> Poetry-based wallet generation tool</li>
                <li><b>XPUB Tool:</b> Extended public key derivation and analysis</li>
                <li><b>BTC Snake Game:</b> Entertainment module with Bitcoin theme</li>
                <li><b>Calculator:</b> Cryptocurrency conversion and calculations</li>
            </ul>
        </div>
        
        <div style='margin-top: 30px;'>
            <h2 style='border-bottom: 1px solid #E7481F; padding-bottom: 5px;'>Configuration Guidelines</h2>
            
            <h3>BitCrack Configuration:</h3>
            <p>RAM-based recommendations:</p>
            <ul>
                <li>16GB RAM: -b 104 -t 512 -p 2016</li>
                <li>8GB RAM: -b 104 -t 512 -p 1024</li>
            </ul>
            <p>Parameters:</p>
            <ul>
                <li>-b: Blocks</li>
                <li>-t: Threads</li>
                <li>-p: Points</li>
            </ul>

            <h3>KeyHunt Configuration:</h3>
            <p>RAM Usage Guidelines:</p>
            <ul>
                <li>2GB RAM: -k 128</li>
                <li>4GB RAM: -k 256</li>
                <li>8GB RAM: -k 512</li>
                <li>16GB RAM: -k 1024</li>
                <li>32GB RAM: -k 2048</li>
            </ul>
            <p>Available Modes:</p>
            <ul>
                <li>address: Basic address searching mode</li>
                <li>bsgs: Baby-Step Giant-Step algorithm mode</li>
            </ul>

            <h3>Secp256k1 Performance:</h3>
            <ul>
                <li>Point Addition: ~2.09 μs per operation</li>
                <li>Scalar Multiplication: ~3.1 μs per operation</li>
                <li>Address Generation: ~6.35 μs per address</li>
                <li>Batch Processing: Up to 3.5 Million keys/s per CPU</li>
            </ul>
        </div>
        
        <div style='margin-top: 30px;'>
            <h2 style='border-bottom: 1px solid #E7481F; padding-bottom: 5px;'>Support & Resources</h2>
            
            <h3>Official Resources:</h3>
            <ul>
                <li>Website: <a href="https://mizogg.co.uk" style="color: #E7481F;">https://mizogg.co.uk</a></li>
                <li>Support Email: Contact through website</li>
                <li>Donations: BTC: 3JKyVkRtxDrXEMtZY6Fy53VmvMAT6LKBo8</li>
            </ul>
            
            <h3>GitHub Repositories:</h3>
            <ul>
                <li><a href="https://github.com/iceland2k14/secp256k1" style="color: #E7481F;">Secp256k1 Library</a></li>
                <li><a href="https://github.com/albertobsd/keyhunt" style="color: #E7481F;">KeyHunt</a></li>
                <li><a href="https://github.com/WanderingPhilosopher/VanBitCrackenRandom2" style="color: #E7481F;">VanBit</a></li>
                <li><a href="https://github.com/brichard19/BitCrack" style="color: #E7481F;">BitCrack</a></li>
            </ul>
        </div>
        """)
        
        main_layout.addWidget(content_browser)

        # Website Button
        icon_size = QSize(26, 26)
        iconred = QIcon(QPixmap(RED_ICON))
        self.miz_git_mode_button = QPushButton("Visit Mizogg Website", self)
        self.miz_git_mode_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Visit Mizogg.co.uk for more information and updates</span>')

        self.miz_git_mode_button.setIconSize(icon_size)
        self.miz_git_mode_button.setIcon(iconred)
        self.miz_git_mode_button.clicked.connect(open_website)
        self.miz_git_mode_button.enterEvent = lambda e: Speaker.play_death()
        main_layout.addWidget(self.miz_git_mode_button)

        self.setLayout(main_layout)