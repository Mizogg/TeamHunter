"""
Settings utility functions for TeamHunter

@author: Team Mizogg
"""
import json
import os
from PyQt6.QtWidgets import QMessageBox
from config.config_manager import config

def get_settings():
    """
    Get settings from the configuration manager.
    This function is maintained for backward compatibility.
    New code should use config.get() directly.
    
    Returns:
        dict: A dictionary of settings
    """
    try:
        # Return a flattened version of the settings for backward compatibility
        settings_dict = {}
        
        # Add paths
        for key in ["INPUT_FOLDER", "IMAGES_FOLDER", "MUSIC_FOLDER", "WINNER_FOLDER"]:
            settings_dict[key] = config.get(f"Paths.{key}", "")
            
        # Add addresses
        settings_dict["START_ADDRESS"] = config.get("Addresses.START_ADDRESS", "")
        settings_dict["END_ADDRESS"] = config.get("Addresses.END_ADDRESS", "")
        
        # Add Telegram settings
        settings_dict["TELEGRAM_TOKEN"] = config.get("Telegram.token", "")
        settings_dict["TELEGRAM_CHAT_ID"] = config.get("Telegram.chatid", "")
        
        # Add Discord settings
        settings_dict["DISCORD_WEBHOOK"] = config.get("Discord.webhook_url", "")
        
        return settings_dict
        
    except Exception as e:
        error_message = f"An error occurred while reading settings: {e}"
        QMessageBox.critical(None, "Error", error_message)
        return {}

# Remove the commented out create_settings_file_if_not_exists function
# as it's now handled by config_manager.py