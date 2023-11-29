"""

@author: Team Mizogg
"""
import sys
from PyQt6.QtWidgets import QMessageBox
sys.path.append('config')
from config import *

def get_settings():
    settings_dict = {}
    try:
        with open(CONFIG_FILE, "r") as settings_file:
            for line in settings_file:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    settings_dict[key] = value
    except FileNotFoundError:
        setting_message = "Settings file not found."
        QMessageBox.information(None, "File not found", setting_message)
    except Exception as e:
        error_message = f"An error occurred while reading settings: {e}"
        QMessageBox.critical(None, "Error", error_message)
    return settings_dict
