"""

@author: Team Mizogg
"""
import json
import os
CONFIG_FILE = "config/config.json"
def create_settings_file_if_not_exists():
    if not os.path.exists(CONFIG_FILE):
        config_data = {
            "Theme": {
                "theme": "dark"
            },
            "Telegram": {
                "token": "",
                "chatid": ""
            },
            "Discord": {
                "webhook_url": ""
            },
            "Addresses": {
                "START_ADDRESS": "",
                "END_ADDRESS": ""
            },
            "Paths": {
                "INPUT_FOLDER": "input",
                "IMAGES_FOLDER": "images",
                "MUSIC_FOLDER": "music",
                "WINNER_FOLDER": "found",
                "BTC_BF_FILE": "btc.bf",
                "BTC_TXT_FILE": "btc.txt"
            }
        }
        
        with open(CONFIG_FILE, "w") as file:
            json.dump(config_data, file, indent=4)
