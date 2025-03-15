# TeamHunter Configuration System

This directory contains the configuration system for TeamHunter.

## Overview

The configuration system has been consolidated to provide a more unified approach to managing settings:

- `config_manager.py`: The main configuration manager that handles loading, saving, and accessing settings
- `config.py`: A backward compatibility layer that imports from config_manager.py
- `settings.json`: The main configuration file (replaces the older config.json)

## Usage

### For New Code

Always use the ConfigManager from config_manager.py:

```python
from config.config_manager import config

# Get a setting
theme = config.get("theme", "default")
input_folder = config.get("Paths.INPUT_FOLDER", "input")

# Set a setting
config.set("theme", "dark")
config.set("Paths.INPUT_FOLDER", "custom_input")

# Get a path (handles nested paths automatically)
btc_file = config.get_path("BTC_BF_FILE")

# Get system info
system_info = config.get_system_info()
```

### For Backward Compatibility

Older code that imports from config.py will continue to work:

```python
from config.config import INPUT_FOLDER, BTC_BF_FILE, create_settings_file_if_not_exists

# These variables are now derived from the ConfigManager
```

## Configuration Structure

The configuration is stored in a JSON file with the following structure:

```json
{
    "theme": "default",
    "sound_enabled": true,
    "music_enabled": true,
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
        "threads": 1,
        "blocks": 1,
        "points": 1,
        "device": 0
    },
    "keyhunt_settings": {
        "last_directory": "",
        "mode": "address",
        "threads": 1
    },
    // Additional tool settings...
}
```

## Migration

The system automatically migrates settings from the old config.json format to the new settings.json format when first run. 