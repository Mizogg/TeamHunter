"""
Configuration Manager for TeamHunter
Centralizes all configuration settings and provides methods to load/save them
"""
import os
import json
import platform
from pathlib import Path
from PyQt6.QtCore import QSettings

# Define constants
CONFIG_FOLDER = "config"
CONFIG_FILE = f"{CONFIG_FOLDER}/settings.json"
LEGACY_CONFIG_FILE = f"{CONFIG_FOLDER}/config.json"

class ConfigManager:
    """
    Manages configuration settings for TeamHunter application
    """
    def __init__(self):
        self.config_file = CONFIG_FILE
        # Remove QSettings initialization with IniFormat
        # self.qt_settings = QSettings(self.config_file, QSettings.Format.IniFormat)
        
        # Default settings structure
        self.default_settings = {
            "theme": "default",
            "sound_enabled": True,
            "music_volume": 50,
            "last_tab": 0,
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
                "BTC_TXT_FILE": "btc.txt",
                "WINNER_FOUND": "found.txt"
            },
            "bitcrack_settings": {
                "last_directory": "",
                "threads": 256,  # Default to 256 threads
                "blocks": 32,    # Default to 32 blocks
                "points": 256,   # Default to 256 points
                "device": "0"    # Default to device 0
            },
            "keyhunt_settings": {
                "last_directory": "",
                "mode": "address",
                "threads": 1,
                "ram": 512      # Default to 512 RAM (-k 512)
            },
            "vanbit_settings": {
                "grid": 32,     # Default to 32 grid size
                "threads": 4    # Default to 4 threads
            },
            "iceland_settings": {
                "mode": "address",
                "input_file": "",
                "output_file": ""
            },
            "mnemonic_settings": {
                "word_count": 12,
                "language": "english"
            },
            "brain_settings": {
                "mode": "single",
                "threads": 1
            },
            "xpub_settings": {
                "xpub": "",
                "start_index": 0,
                "end_index": 10
            }
        }
        
        self.settings = {}
        self.initialize()
        
    def initialize(self):
        """Initialize configuration system, migrating from old config if needed"""
        # First check if we need to migrate from the old config format
        if os.path.exists(LEGACY_CONFIG_FILE) and not os.path.exists(self.config_file):
            self.migrate_from_legacy()
        
        # Then load or create settings
        self.load_settings()
        
        # Ensure required directories exist
        self.create_required_directories()
    
    def migrate_from_legacy(self):
        """Migrate settings from legacy config.json format"""
        try:
            with open(LEGACY_CONFIG_FILE, 'r') as f:
                legacy_config = json.load(f)
                
            # Start with default settings
            migrated_settings = self.default_settings
            
            # Update with values from legacy config
            if "Telegram" in legacy_config:
                migrated_settings["Telegram"] = legacy_config["Telegram"]
            
            if "Discord" in legacy_config:
                migrated_settings["Discord"] = legacy_config["Discord"]
            
            if "Addresses" in legacy_config:
                migrated_settings["Addresses"] = legacy_config["Addresses"]
            
            if "Paths" in legacy_config:
                migrated_settings["Paths"] = legacy_config["Paths"]
            
            # Save migrated settings
            self.settings = migrated_settings
            self.save_settings()
            
            print("Successfully migrated from legacy configuration")
            
        except Exception as e:
            print(f"Error migrating from legacy config: {e}")
            self.settings = self.default_settings
        
    def load_settings(self):
        """Load settings from file or create with defaults if not exists"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    try:
                        loaded_settings = json.load(f)
                        
                        # Start with default settings to ensure all keys exist
                        self.settings = self.default_settings.copy()
                        
                        # Update with loaded settings using a deep merge
                        self._deep_update(self.settings, loaded_settings)
                    except json.JSONDecodeError:
                        # If the file is not valid JSON (e.g., it's in INI format), recreate it
                        print("Settings file is not in valid JSON format. Creating new settings file.")
                        self.settings = self.default_settings.copy()
                        self.save_settings()
            else:
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
                self.settings = self.default_settings.copy()
                self.save_settings()
            
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.settings = self.default_settings.copy()
            
    def _deep_update(self, target, source):
        """Deep update target dict with source
        For each k,v in source: if k doesn't exist in target, it is deep copied from
        source to target. Otherwise, if v is a dict, recursively update the dict in target.
        """
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
            
    def save_settings(self):
        """Save current settings to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def create_required_directories(self):
        """Create required directories based on configuration"""
        try:
            # Create main directories
            directories = [
                self.get("Paths.INPUT_FOLDER", "input"),
                self.get("Paths.IMAGES_FOLDER", "images"),
                self.get("Paths.MUSIC_FOLDER", "music"),
                self.get("Paths.WINNER_FOLDER", "found")
            ]
            
            for directory in directories:
                if not os.path.exists(directory):
                    os.makedirs(directory, exist_ok=True)
                    
        except Exception as e:
            print(f"Error creating directories: {e}")
            
    def get(self, key, default=None):
        """Get a setting value by key with optional default"""
        keys = key.split('.')
        value = self.settings
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_path(self, key, default=None):
        """Get a path from the Paths section"""
        base_folder = self.get(f"Paths.{key}", default)
        if key in ["BTC_BF_FILE", "BTC_TXT_FILE", "WINNER_FOUND"]:
            # These are files within folders
            parent_folder = "INPUT_FOLDER"
            if key == "WINNER_FOUND":
                parent_folder = "WINNER_FOLDER"
            
            parent_path = self.get(f"Paths.{parent_folder}", "")
            return f"{parent_path}/{base_folder}"
        
        return base_folder
            
    def set(self, key, value):
        """Set a setting value by key"""
        keys = key.split('.')
        settings_ref = self.settings
        
        # Navigate to the nested dictionary
        for k in keys[:-1]:
            if k not in settings_ref:
                settings_ref[k] = {}
            settings_ref = settings_ref[k]
            
        # Set the value
        settings_ref[keys[-1]] = value
        
        # Save settings to file immediately to ensure they persist
        self.save_settings()
        
        # No longer using QSettings
        # self.qt_settings.setValue(key, value)
        
    def get_system_info(self):
        """Get system information"""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
            "processor": platform.processor(),
            "machine": platform.machine()
        }
        
# Create a singleton instance
config = ConfigManager() 