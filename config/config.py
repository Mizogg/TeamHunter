import json
from PyQt6.QtCore import QSettings

CONFIG_FOLDER = "config"

# Define paths and settings
settings = QSettings(f"{CONFIG_FOLDER}/config.json", QSettings.Format.IniFormat)
CONFIG_FILE = f"{CONFIG_FOLDER}/config.json"

INPUT_FOLDER = settings.value("Paths/INPUT_FOLDER", defaultValue="input", type=str)
IMAGES_FOLDER = settings.value("Paths/IMAGES_FOLDER", defaultValue="webfiles/css/images", type=str)
WINNER_FOLDER = settings.value("Paths/WINNER_FOLDER", defaultValue="found", type=str)

BTC_BF_FILE = f"{INPUT_FOLDER}/{settings.value('Paths/BTC_BF_FILE', defaultValue='btc.bf', type=str)}"
BTC_TXT_FILE = f"{INPUT_FOLDER}/{settings.value('Paths/BTC_TXT_FILE', defaultValue='btc.txt', type=str)}"

WINNER_COMPRESSED = f"{WINNER_FOLDER}/{settings.value('Paths/WINNER_COMPRESSED', defaultValue='foundcaddr.txt', type=str)}"
WINNER_UNCOMPRESSED = f"{WINNER_FOLDER}/{settings.value('Paths/WINNER_UNCOMPRESSED', defaultValue='founduaddr.txt', type=str)}"
WINNER_P2SH = f"{WINNER_FOLDER}/{settings.value('Paths/WINNER_P2SH', defaultValue='foundp2sh.txt', type=str)}"
WINNER_BECH32 = f"{WINNER_FOLDER}/{settings.value('Paths/WINNER_BECH32', defaultValue='foundbech32.txt', type=str)}"

START_ADDRESS_KEY = 'Addresses/START_ADDRESS'
END_ADDRESS_KEY = 'Addresses/END_ADDRESS'

START_ADDRESS = settings.value(START_ADDRESS_KEY, defaultValue='', type=str)
END_ADDRESS = settings.value(END_ADDRESS_KEY, defaultValue='', type=str)

SKIPPED_FILE = f"{INPUT_FOLDER}/{settings.value('Paths/SKIPPED_FILE', defaultValue='skipped.txt', type=str)}"
