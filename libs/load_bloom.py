"""

@author: Team Mizogg
"""
from bloomfilter import BloomFilter
import sys
sys.path.append('config')
from config import *
def load_bloom_filter():
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