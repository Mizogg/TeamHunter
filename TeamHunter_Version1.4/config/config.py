"""

@author: Team Mizogg
"""
from PyQt6.QtCore import QSettings

CONFIG_FOLDER = "config"

# Define paths and settings
settings = QSettings(f"{CONFIG_FOLDER}/config.json", QSettings.Format.IniFormat)
CONFIG_FILE = f"{CONFIG_FOLDER}/config.json"

INPUT_FOLDER = settings.value("Paths/INPUT_FOLDER", defaultValue="input", type=str)
IMAGES_FOLDER = settings.value("Paths/IMAGES_FOLDER", defaultValue="images", type=str)
MUSIC_FOLDER = settings.value("Paths/MUSIC_FOLDER", defaultValue="music", type=str)
WINNER_FOLDER = settings.value("Paths/WINNER_FOLDER", defaultValue="found", type=str)

BTC_TXT_FILE = f"{INPUT_FOLDER}/{settings.value('Paths/BTC_TXT_FILE', defaultValue='btc.txt', type=str)}"

WINNER_FOUND = f"{WINNER_FOLDER}/{settings.value('Paths/WINNER_FOUND', defaultValue='found.txt', type=str)}"

START_ADDRESS_KEY = 'Addresses_start/START_ADDRESS'
END_ADDRESS_KEY = 'Addresses_stop/END_ADDRESS'

START_ADDRESS = settings.value(START_ADDRESS_KEY, defaultValue='', type=str)
END_ADDRESS = settings.value(END_ADDRESS_KEY, defaultValue='', type=str)
