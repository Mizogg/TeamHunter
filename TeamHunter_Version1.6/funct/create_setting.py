"""
Compatibility module for create_setting

This module provides backward compatibility with code that imports from funct.create_setting
All functionality has been moved to config_manager.py

@author: Team Mizogg
"""
from config.config_manager import config

# For backward compatibility
def create_settings_file_if_not_exists():
    """
    This function is maintained for backward compatibility.
    The ConfigManager now handles this automatically.
    """
    # This will trigger the ConfigManager to create the file if it doesn't exist
    config.initialize()

# Any other functions that might have been in the original create_setting.py
# should be added here as wrappers around the ConfigManager functionality 