"""
Configuration module for TeamHunter
This file provides backward compatibility with older code that imports from config.py
All new code should use config_manager.py directly.

@author: Team Mizogg
"""
from config.config_manager import config, CONFIG_FOLDER

# For backward compatibility
# The qt_settings attribute has been removed from ConfigManager
# Create a simple class to mimic QSettings for backward compatibility
class SettingsProxy:
    def value(self, key, default=None):
        return config.get(key, default)
    
    def setValue(self, key, value):
        config.set(key, value)
        
    def sync(self):
        config.save_settings()

# Create a proxy object for backward compatibility
settings = SettingsProxy()
CONFIG_FILE = config.config_file

# Define paths for backward compatibility
INPUT_FOLDER = config.get("Paths.INPUT_FOLDER", "input")
IMAGES_FOLDER = config.get("Paths.IMAGES_FOLDER", "images")
MUSIC_FOLDER = config.get("Paths.MUSIC_FOLDER", "music")
WINNER_FOLDER = config.get("Paths.WINNER_FOLDER", "found")

BTC_BF_FILE = config.get_path("BTC_BF_FILE", "btc.bf")
BTC_TXT_FILE = config.get_path("BTC_TXT_FILE", "btc.txt")
WINNER_FOUND = config.get_path("WINNER_FOUND", "found.txt")

START_ADDRESS_KEY = 'Addresses.START_ADDRESS'
END_ADDRESS_KEY = 'Addresses.END_ADDRESS'

START_ADDRESS = config.get(START_ADDRESS_KEY, '')
END_ADDRESS = config.get(END_ADDRESS_KEY, '')

# Function to create settings file (for backward compatibility)
def create_settings_file_if_not_exists():
    """
    This function is maintained for backward compatibility.
    The ConfigManager now handles this automatically.
    """
    # This will trigger the ConfigManager to create the file if it doesn't exist
    config.initialize()
