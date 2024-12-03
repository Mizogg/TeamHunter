# scanner_thread.py
import os
import random
from PyQt6.QtCore import QThread, pyqtSignal
from funct.iceland import secp256k1 as ice
from funct import (team_balance, load_file)
import numpy as np

addfind = load_file.load_addresses()
FOUND_FILE = "found/found.txt"

class KeyspaceScannerThread(QThread):
    btc_hunter_finished = pyqtSignal(str, str)
    grid_data_ready = pyqtSignal(list)

    def __init__(self, start_value, end_value):
        super().__init__()
        self.start_value = start_value
        self.end_value = end_value
        self.is_active = True

    def stop(self):
        self.is_active = False

    def run(self):
        counter = 0
        while self.is_active:
            int_value = random.randint(self.start_value, self.end_value)
            dec = int(int_value)
            caddr = ice.privatekey_to_address(0, True, dec)
            uaddr = ice.privatekey_to_address(0, False, dec)
            p2sh = ice.privatekey_to_address(1, True, dec)
            bech32 = ice.privatekey_to_address(2, True, dec)
            HEX = "%064x" % dec
            wifc = ice.btc_pvk_to_wif(HEX)
            wifu = ice.btc_pvk_to_wif(HEX, False)
            data = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Compressed: {caddr} \nWIF Compressed: {wifc} \nBTC Address Uncompressed: {uaddr} \nWIF Uncompressed: {wifu} \nBTC Address p2sh: {p2sh} \nBTC Address Bc1: {bech32} \n")
            self.btc_hunter_finished.emit(data, 'scanning')
            counter += 1
            if caddr in addfind:
                WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Compressed: {caddr} \nWIF Compressed: {wifc} \n")
                self.btc_hunter_finished.emit(data, 'winner')
                try:
                    with open(FOUND_FILE, "a") as f:
                        f.write(WINTEXT)
                except FileNotFoundError:
                    os.makedirs(os.path.dirname(FOUND_FILE), exist_ok=True)

                    with open(FOUND_FILE, "w") as f:
                        f.write(WINTEXT)
            if uaddr in addfind:
                WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Uncompressed: {uaddr} \nWIF Uncompressed: {wifu} \n")
                self.btc_hunter_finished.emit(data, 'winner')
                try:
                    with open(FOUND_FILE, "a") as f:
                        f.write(WINTEXT)
                except FileNotFoundError:
                    os.makedirs(os.path.dirname(FOUND_FILE), exist_ok=True)

                    with open(FOUND_FILE, "w") as f:
                        f.write(WINTEXT)
            if p2sh in addfind:
                self.WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address p2sh: {p2sh} \n")
                self.btc_hunter_finished.emit(data, 'winner')
                try:
                    with open(FOUND_FILE, "a") as f:
                        f.write(WINTEXT)
                except FileNotFoundError:
                    os.makedirs(os.path.dirname(FOUND_FILE), exist_ok=True)

                    with open(FOUND_FILE, "w") as f:
                        f.write(WINTEXT)
            if bech32 in addfind:
                WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Bc1: {bech32} \n")
                self.btc_hunter_finished.emit(data, 'winner')
                try:
                    with open(FOUND_FILE, "a") as f:
                        f.write(WINTEXT)
                except FileNotFoundError:
                    os.makedirs(os.path.dirname(FOUND_FILE), exist_ok=True)

                    with open(FOUND_FILE, "w") as f:
                        f.write(WINTEXT)
            if counter >= 1000:
                binstring = "{0:b}".format(int_value)
                binstring = binstring.rjust(16 * 16, "0")
                self.grid_data_ready.emit(self.grid_data(binstring))
                counter = 0

    def grid_data(self, binstring):
        grid = [[int(binstring[j]) for j in range(i * 16, (i + 1) * 16)] for i in range(16)]
        return grid

class BtcHunterThread(QThread):
    btc_hunter_finished = pyqtSignal(str, str)

    def __init__(self, grid):
        super().__init__()
        self.grid = grid

    def run(self):
        arr = np.array(self.grid)
        binstring = ''.join(''.join(map(str, l)) for l in arr)
        dec = int(binstring, 2)
        caddr = ice.privatekey_to_address(0, True, dec)
        uaddr = ice.privatekey_to_address(0, False, dec)
        p2sh = ice.privatekey_to_address(1, True, dec)
        bech32 = ice.privatekey_to_address(2, True, dec)
        HEX = "%064x" % dec
        wifc = ice.btc_pvk_to_wif(HEX)
        wifu = ice.btc_pvk_to_wif(HEX, False)
        data = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Compressed: {caddr} \nWIF Compressed: {wifc} \nBTC Address Uncompressed: {uaddr} \nWIF Uncompressed: {wifu} \nBTC Address p2sh: {p2sh} \nBTC Address Bc1: {bech32} \n")
        self.btc_hunter_finished.emit(data, 'scanning')
        if caddr in addfind:
            WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Compressed: {caddr} \nWIF Compressed: {wifc} \n")
            self.btc_hunter_finished.emit(data, 'winner')
            try:
                with open(FOUND_FILE, "a") as f:
                    f.write(WINTEXT)
            except FileNotFoundError:
                os.makedirs(os.path.dirname(FOUND_FILE), exist_ok=True)

                with open(FOUND_FILE, "w") as f:
                    f.write(WINTEXT)
            pass
        if uaddr in addfind:
            WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Uncompressed: {uaddr} \nWIF Uncompressed: {wifu} \n")
            self.btc_hunter_finished.emit(data, 'winner')
            try:
                with open(FOUND_FILE, "a") as f:
                    f.write(WINTEXT)
            except FileNotFoundError:
                os.makedirs(os.path.dirname(FOUND_FILE), exist_ok=True)

                with open(FOUND_FILE, "w") as f:
                    f.write(WINTEXT)
            pass
        if p2sh in addfind:
            self.WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address p2sh: {p2sh} \n")
            self.btc_hunter_finished.emit(data, 'winner')
            try:
                with open(FOUND_FILE, "a") as f:
                    f.write(WINTEXT)
            except FileNotFoundError:
                os.makedirs(os.path.dirname(FOUND_FILE), exist_ok=True)

                with open(FOUND_FILE, "w") as f:
                    f.write(WINTEXT)
            pass
        if bech32 in addfind:
            WINTEXT = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Bc1: {bech32} \n")
            self.btc_hunter_finished.emit(data, 'winner')
            try:
                with open(FOUND_FILE, "a") as f:
                    f.write(WINTEXT)
            except FileNotFoundError:
                os.makedirs(os.path.dirname(FOUND_FILE), exist_ok=True)

                with open(FOUND_FILE, "w") as f:
                    f.write(WINTEXT)
            pass
    def stop(self):
        self.terminate()

    def finish(self):
        self.quit()
        self.wait()

class BtcHunterThread_online(QThread):
    btc_hunter_finished_online = pyqtSignal(str, str)

    def __init__(self, grid):
        super().__init__()
        self.grid = grid

    def run(self):
        arr = np.array(self.grid)
        binstring = ''.join(''.join(map(str, l)) for l in arr)
        dec = int(binstring, 2)
        caddr = ice.privatekey_to_address(0, True, dec)
        uaddr = ice.privatekey_to_address(0, False, dec)
        HEX = "%064x" % dec
        wifc = ice.btc_pvk_to_wif(HEX)
        wifu = ice.btc_pvk_to_wif(HEX, False)
        balance, totalReceived, totalSent, txs = team_balance.check_balance(caddr)
        balanceu, totalReceivedu, totalSentu, txsu = team_balance.check_balance(uaddr)
        data = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Compressed: {caddr} \nWIF Compressed: {wifc} \nBalance: {balance} \nTotalReceived: {totalReceived} \nTotalSent: {totalSent} \nTransactions: {txs}\n")
        data1 = (f"DEC Key: {dec}\nHEX Key: {HEX} \nBTC Address Uncompressed: {uaddr} \nWIF Uncompressed: {wifu} \nBalance: {balanceu} \nTotalReceived: {totalReceivedu} \nTotalSent: {totalSentu} \nTransactions: {txsu}\n")
        self.btc_hunter_finished_online.emit(data, 'scanning')
        self.btc_hunter_finished_online.emit(data1, 'scanningu')
        if int(txs) > 1:
            self.btc_hunter_finished_online.emit(data, 'winner')
            try:
                with open(FOUND_FILE, "a") as f:
                    f.write(data)
            except FileNotFoundError:
                os.makedirs(os.path.dirname(FOUND_FILE), exist_ok=True)

                with open(FOUND_FILE, "w") as f:
                    f.write(data)
        if int(txsu) > 1:
            self.btc_hunter_finished_online.emit(data1, 'winner')
            try:
                with open(FOUND_FILE, "a") as f:
                    f.write(data1)
            except FileNotFoundError:
                os.makedirs(os.path.dirname(FOUND_FILE), exist_ok=True)

                with open(FOUND_FILE, "w") as f:
                    f.write(data1)

    def stop(self):
        self.terminate()

    def finish(self):
        self.quit()
        self.wait()