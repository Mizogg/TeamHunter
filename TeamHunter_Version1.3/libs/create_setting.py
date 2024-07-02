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
    else:
        # Load existing configuration data
        with open(CONFIG_FILE, "r") as file:
            config_data = json.load(file)

    # Check and create the "found" folder
    found_folder = config_data["Paths"]["WINNER_FOLDER"]
    if not os.path.exists(found_folder):
        os.makedirs(found_folder)
