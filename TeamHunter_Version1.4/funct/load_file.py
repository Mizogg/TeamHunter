"""

@author: Team Mizogg
"""
from bloomfilter import BloomFilter

BTC_BF_FILE = "input/btc.bf"
BTC_TXT_FILE = "input/btc.txt"
def load_addresses():
    global addfind
    try:
        with open(BTC_BF_FILE, "rb") as fp:
            addfind = BloomFilter.load(fp)
    except FileNotFoundError:
        try:
            with open(BTC_TXT_FILE) as file:
                addfind = file.read().split()
        except FileNotFoundError:
            addfind = []

    return addfind