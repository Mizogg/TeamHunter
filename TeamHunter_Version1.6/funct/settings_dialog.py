"""
Settings Dialog for TeamHunter
Provides a dialog for configuring application settings
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QComboBox, QCheckBox, QTabWidget, QWidget, QSlider,
    QGroupBox, QFormLayout, QSpinBox, QLineEdit, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config_manager import config
from config.theme_manager import theme_manager
from config.logger import logger

class SettingsDialog(QDialog):
    """
    Dialog for configuring application settings
    """
    settings_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TeamHunter Settings")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        # Set spinbox and combobox style to ensure they work properly
        self.setStyleSheet("""
            QSpinBox {
                padding-right: 15px; /* Make room for the arrows */
            }
            QSpinBox::up-button {
                width: 16px;
                border-width: 1px;
                subcontrol-origin: border;
                subcontrol-position: top right;
            }
            QSpinBox::down-button {
                width: 16px;
                border-width: 1px;
                subcontrol-origin: border;
                subcontrol-position: bottom right;
            }
            QComboBox {
                min-width: 80px;
                padding: 5px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-style: solid;
            }
        """)
        
        # Initialize UI
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components"""
        main_layout = QVBoxLayout()
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create tabs
        self.general_tab = QWidget()
        self.appearance_tab = QWidget()
        self.tools_tab = QWidget()
        self.advanced_tab = QWidget()
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.general_tab, "General")
        self.tab_widget.addTab(self.appearance_tab, "Appearance")
        self.tab_widget.addTab(self.tools_tab, "Tools")
        self.tab_widget.addTab(self.advanced_tab, "Advanced")
        
        # Setup each tab
        self.setup_general_tab()
        self.setup_appearance_tab()
        self.setup_tools_tab()
        self.setup_advanced_tab()
        
        # Add tab widget to main layout
        main_layout.addWidget(self.tab_widget)
        
        # Add buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.apply_button)
        button_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def setup_general_tab(self):
        """Setup the general tab"""
        layout = QVBoxLayout()
        
        # Sound settings group
        sound_group = QGroupBox("Sound Settings")
        sound_layout = QFormLayout()
        
        self.sound_enabled_checkbox = QCheckBox("Enable Sound Effects")
        self.sound_enabled_checkbox.setChecked(config.get("sound_enabled", True))
        
        self.music_volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.music_volume_slider.setMinimum(0)
        self.music_volume_slider.setMaximum(100)
        self.music_volume_slider.setValue(config.get("music_volume", 50))
        
        sound_layout.addRow("Sound Effects:", self.sound_enabled_checkbox)
        sound_layout.addRow("Music Volume:", self.music_volume_slider)
        
        sound_group.setLayout(sound_layout)
        
        # Startup settings group
        startup_group = QGroupBox("Startup Settings")
        startup_layout = QFormLayout()
        
        self.start_tab_combo = QComboBox()
        tabs = ["Welcome", "BitCrack", "VanBit", "KeyHunt", 
                "Iceland2k14 Secp256k1", "Miz Mnemonic", "Brain Hunter", 
                "Miz Poetry", "XPUB Tool", "CAL", "BTC Snake Game"]
        self.start_tab_combo.addItems(tabs)
        self.start_tab_combo.setCurrentIndex(config.get("last_tab", 0))
        
        startup_layout.addRow("Default Tab:", self.start_tab_combo)
        
        startup_group.setLayout(startup_layout)
        
        # Add groups to layout
        layout.addWidget(sound_group)
        layout.addWidget(startup_group)
        layout.addStretch()
        
        self.general_tab.setLayout(layout)
        
    def setup_appearance_tab(self):
        """Setup the appearance tab"""
        layout = QVBoxLayout()
        
        # Theme settings group
        theme_group = QGroupBox("Theme Settings")
        theme_layout = QFormLayout()
        
        self.theme_combo = QComboBox()
        themes = list(theme_manager.themes.keys())
        self.theme_combo.addItems(themes)
        self.theme_combo.setCurrentText(theme_manager.current_theme)
        
        # Add theme preview
        self.theme_preview = QLabel()
        self.theme_preview.setFixedSize(300, 200)
        self.update_theme_preview(theme_manager.current_theme)
        
        self.theme_combo.currentTextChanged.connect(self.update_theme_preview)
        
        theme_layout.addRow("Theme:", self.theme_combo)
        theme_layout.addRow("Preview:", self.theme_preview)
        
        theme_group.setLayout(theme_layout)
        
        # Add groups to layout
        layout.addWidget(theme_group)
        layout.addStretch()
        
        self.appearance_tab.setLayout(layout)
        
    def update_theme_preview(self, theme_name):
        """Update the theme preview to show a realistic representation of the theme"""
        theme = theme_manager.get_theme(theme_name)
        
        # Create a preview widget to demonstrate theme elements
        preview_widget = QWidget()
        preview_widget.setFixedSize(300, 300)
        
        # Create a layout for the preview
        layout = QVBoxLayout(preview_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Add a title bar to simulate window
        title_bar = QWidget()
        title_bar.setFixedHeight(30)
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(8, 0, 8, 0)
        
        title_label = QLabel("Preview Window")
        close_button = QPushButton("×")
        close_button.setFixedSize(20, 20)
        
        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(close_button)
        
        # Create content area
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        
        # Add some common UI elements
        button = QPushButton("Sample Button")
        checkbox = QCheckBox("Enable Option")
        combo = QComboBox()
        combo.addItems(["Option 1", "Option 2", "Option 3"])
        text_input = QLineEdit()
        text_input.setPlaceholderText("Enter text...")
        
        content_layout.addWidget(button)
        content_layout.addWidget(checkbox)
        content_layout.addWidget(combo)
        content_layout.addWidget(text_input)
        content_layout.addStretch()
        
        # Add status bar
        status_bar = QLabel("Status: Ready")
        status_bar.setFixedHeight(25)
        status_bar.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # Add all components to main layout
        layout.addWidget(title_bar)
        layout.addWidget(content_area)
        layout.addWidget(status_bar)
        
        # Apply theme colors
        preview_style = f"""
            QWidget {{
                background-color: {theme['background_color']};
                color: {theme['text_color']};
                border: none;
            }}
            
            QLabel {{
                padding: 2px;
            }}
            
            QPushButton {{
                background-color: {theme['button_color']};
                color: {theme['button_text_color']};
                border: 1px solid {theme['border_color']};
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }}
            
            QPushButton:hover {{
                background-color: {theme['button_hover_color']};
            }}
            
            QLineEdit {{
                background-color: {theme['background_color']};
                color: {theme['text_color']};
                border: 1px solid {theme['border_color']};
                border-radius: 4px;
                padding: 5px;
            }}
            
            QComboBox {{
                background-color: {theme['background_color']};
                color: {theme['text_color']};
                border: 1px solid {theme['border_color']};
                border-radius: 4px;
                padding: 5px;
                min-width: 100px;
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            
            QCheckBox {{
                spacing: 5px;
            }}
            
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {theme['border_color']};
                border-radius: 3px;
                background-color: {theme['background_color']};
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {theme['accent_color']};
            }}
        """
        
        preview_widget.setStyleSheet(preview_style)
        
        # Create a QPixmap from the preview widget
        pixmap = QPixmap(preview_widget.size())
        preview_widget.render(pixmap)
        
        # Set the preview image
        self.theme_preview.setPixmap(pixmap)
        
    def setup_tools_tab(self):
        """Setup the tools tab"""
        layout = QVBoxLayout()
        
        # BitCrack settings group
        bitcrack_group = QGroupBox("BitCrack Settings")
        bitcrack_layout = QFormLayout()
        
        # Create dropdown menus to match BitCrack GUI
        self.bitcrack_threads = QComboBox()
        self.bitcrack_threads.addItems(['32', '64', '96', '128', '256', '512'])
        
        # Get thread count from config or use default (256)
        default_thread_index = 4  # Default to 256
        config_thread_count = config.get("bitcrack_settings.threads", 256)
        for i in range(self.bitcrack_threads.count()):
            if self.bitcrack_threads.itemText(i) == str(config_thread_count):
                default_thread_index = i
                break
        
        self.bitcrack_threads.setCurrentIndex(default_thread_index)
        
        self.bitcrack_blocks = QComboBox()
        for i in range(8, 153, 2):
            self.bitcrack_blocks.addItem(str(i))
        
        # Get block size from config or use default (32)
        default_block_index = 12  # Default to 32
        config_block_size = config.get("bitcrack_settings.blocks", 32)
        for i in range(self.bitcrack_blocks.count()):
            if self.bitcrack_blocks.itemText(i) == str(config_block_size):
                default_block_index = i
                break
        
        self.bitcrack_blocks.setCurrentIndex(default_block_index)
        
        self.bitcrack_points = QComboBox()
        self.bitcrack_points.addItems(['128', '256', '512', '1024', '2048'])
        
        # Get points size from config or use default (256)
        default_points_index = 1  # Default to 256
        config_points_size = config.get("bitcrack_settings.points", 256)
        for i in range(self.bitcrack_points.count()):
            if self.bitcrack_points.itemText(i) == str(config_points_size):
                default_points_index = i
                break
        
        self.bitcrack_points.setCurrentIndex(default_points_index)
        
        # Add a device selection field
        self.bitcrack_device = QLineEdit()
        self.bitcrack_device.setText(config.get("bitcrack_settings.device", "0"))
        
        bitcrack_layout.addRow("Threads:", self.bitcrack_threads)
        bitcrack_layout.addRow("Blocks:", self.bitcrack_blocks)
        bitcrack_layout.addRow("Points:", self.bitcrack_points)
        bitcrack_layout.addRow("Device(s):", self.bitcrack_device)
        
        # Add a button to set recommended values based on RAM
        ram_button_layout = QHBoxLayout()
        
        default_button = QPushButton("Default")
        default_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Sets Blocks=32, Threads=256, Points=256</span>')
        default_button.clicked.connect(lambda: self.set_bitcrack_ram_preset(0))
        
        ram_8gb_button = QPushButton("8GB RAM")
        ram_8gb_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Sets Blocks=104, Threads=512, Points=1024</span>')
        ram_8gb_button.clicked.connect(lambda: self.set_bitcrack_ram_preset(8))
        
        ram_16gb_button = QPushButton("16GB RAM")
        ram_16gb_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Sets Blocks=128, Threads=512, Points=2048</span>')
        ram_16gb_button.clicked.connect(lambda: self.set_bitcrack_ram_preset(16))
        
        ram_32gb_button = QPushButton("32GB RAM")
        ram_32gb_button.setToolTip('<span style="font-size: 10pt; font-weight: bold; color: black;">Sets Blocks=152, Threads=512, Points=2048</span>')
        ram_32gb_button.clicked.connect(lambda: self.set_bitcrack_ram_preset(32))
        
        ram_button_layout.addWidget(default_button)
        ram_button_layout.addWidget(ram_8gb_button)
        ram_button_layout.addWidget(ram_16gb_button)
        ram_button_layout.addWidget(ram_32gb_button)
        
        bitcrack_layout.addRow("Presets:", ram_button_layout)
        
        bitcrack_group.setLayout(bitcrack_layout)
        
        # KeyHunt settings group
        keyhunt_group = QGroupBox("KeyHunt Settings")
        keyhunt_layout = QFormLayout()
        
        # Create dropdown for CPU selection
        self.keyhunt_threads = QComboBox()
        self.keyhunt_threads.addItems(['1', '2', '4', '8', '16', '32', '64'])
        
        # Get CPU count from config or use default (1)
        default_threads_index = 0  # Default to 1
        config_threads_count = config.get("keyhunt_settings.threads", 1)
        for i in range(self.keyhunt_threads.count()):
            if int(self.keyhunt_threads.itemText(i)) == config_threads_count:
                default_threads_index = i
                break
        
        self.keyhunt_threads.setCurrentIndex(default_threads_index)
        
        self.keyhunt_mode = QComboBox()
        self.keyhunt_mode.addItems(["address", "bsgs", "rmd160"])
        self.keyhunt_mode.setCurrentText(config.get("keyhunt_settings.mode", "address"))
        
        # Add a RAM selection field for KeyHunt
        self.keyhunt_ram = QComboBox()
        self.keyhunt_ram.addItems(["128", "256", "512", "1024", "2048"])
        
        # Get the current RAM value or default to 512
        current_ram = config.get("keyhunt_settings.ram", 512)
        ram_index = 2  # Default to 512
        for i, ram in enumerate(["128", "256", "512", "1024", "2048"]):
            if int(ram) == current_ram:
                ram_index = i
                break
        
        self.keyhunt_ram.setCurrentIndex(ram_index)
        
        keyhunt_layout.addRow("CPUs:", self.keyhunt_threads)
        keyhunt_layout.addRow("Mode:", self.keyhunt_mode)
        keyhunt_layout.addRow("RAM (-k):", self.keyhunt_ram)
        
        keyhunt_group.setLayout(keyhunt_layout)
        
        # VanBit settings group
        vanbit_group = QGroupBox("VanBit Settings")
        vanbit_layout = QFormLayout()
        
        # Create dropdown for CPU selection
        self.vanbit_cpu = QComboBox()
        self.vanbit_cpu.addItems(['1', '2', '4', '8', '16', '32', '64'])
        
        # Get CPU count from config or use default (4)
        default_cpu_index = 2  # Default to 4
        config_cpu_count = config.get("vanbit_settings.threads", 4)
        for i in range(self.vanbit_cpu.count()):
            if int(self.vanbit_cpu.itemText(i)) == config_cpu_count:
                default_cpu_index = i
                break
        
        self.vanbit_cpu.setCurrentIndex(default_cpu_index)
        
        # Create grid size input
        self.vanbit_grid_size = QComboBox()
        self.vanbit_grid_size.addItems(['16', '32', '64', '96', '128'])
        
        # Get grid size from config or use default (32)
        default_grid_index = 1  # Default to 32
        config_grid_size = config.get("vanbit_settings.grid", 32)
        for i in range(self.vanbit_grid_size.count()):
            if self.vanbit_grid_size.itemText(i) == str(config_grid_size):
                default_grid_index = i
                break
        
        self.vanbit_grid_size.setCurrentIndex(default_grid_index)
        
        vanbit_layout.addRow("Number of CPUs:", self.vanbit_cpu)
        vanbit_layout.addRow("Grid Size:", self.vanbit_grid_size)
        
        vanbit_group.setLayout(vanbit_layout)
        
        # Add groups to layout
        layout.addWidget(bitcrack_group)
        layout.addWidget(keyhunt_group)
        layout.addWidget(vanbit_group)
        layout.addStretch()
        
        self.tools_tab.setLayout(layout)
        
    def set_bitcrack_ram_preset(self, ram_gb):
        """Set BitCrack settings based on RAM size"""
        if ram_gb == 0:
            # Default settings
            blocks = "32"
            threads = "256"
            points = "256"
        elif ram_gb == 8:
            # Optimal settings for 8GB RAM
            blocks = "104"
            threads = "512"
            points = "1024"
        elif ram_gb == 16:
            # Optimal settings for 16GB RAM
            blocks = "128"
            threads = "512"
            points = "2048"
        elif ram_gb == 32:
            # Optimal settings for 32GB RAM
            blocks = "152"
            threads = "512"
            points = "2048"
        else:
            return
            
        # Find and set blocks
        for i in range(self.bitcrack_blocks.count()):
            if self.bitcrack_blocks.itemText(i) == blocks:
                self.bitcrack_blocks.setCurrentIndex(i)
                break
        
        # Find and set threads
        for i in range(self.bitcrack_threads.count()):
            if self.bitcrack_threads.itemText(i) == threads:
                self.bitcrack_threads.setCurrentIndex(i)
                break
        
        # Find and set points
        for i in range(self.bitcrack_points.count()):
            if self.bitcrack_points.itemText(i) == points:
                self.bitcrack_points.setCurrentIndex(i)
                break
        
    def setup_advanced_tab(self):
        """Setup the advanced tab"""
        layout = QVBoxLayout()
        
        # Logging settings group
        logging_group = QGroupBox("Logging Settings")
        logging_layout = QFormLayout()
        
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.log_level_combo.setCurrentText(config.get("log_level", "INFO"))
        
        self.log_retention = QSpinBox()
        self.log_retention.setMinimum(1)
        self.log_retention.setMaximum(90)
        self.log_retention.setValue(config.get("log_retention_days", 7))
        
        self.clear_logs_button = QPushButton("Clear Old Logs")
        self.clear_logs_button.clicked.connect(self.clear_old_logs)
        
        logging_layout.addRow("Log Level:", self.log_level_combo)
        logging_layout.addRow("Log Retention (days):", self.log_retention)
        logging_layout.addRow("", self.clear_logs_button)
        
        logging_group.setLayout(logging_layout)
        
        # System information group
        system_group = QGroupBox("System Information")
        system_layout = QFormLayout()
        
        system_info = config.get_system_info()
        
        system_layout.addRow("Operating System:", QLabel(f"{system_info['os']} {system_info['os_version']}"))
        system_layout.addRow("Python Version:", QLabel(system_info['python_version']))
        system_layout.addRow("Processor:", QLabel(system_info['processor']))
        system_layout.addRow("Machine:", QLabel(system_info['machine']))
        
        system_group.setLayout(system_layout)
        
        # Add groups to layout
        layout.addWidget(logging_group)
        layout.addWidget(system_group)
        layout.addStretch()
        
        self.advanced_tab.setLayout(layout)
        
    def clear_old_logs(self):
        """Clear old log files"""
        days = self.log_retention.value()
        count = logger.clear_old_logs(days)
        
        if count > 0:
            self.parent().statusBar().showMessage(f"Cleared {count} old log files", 3000)
        else:
            self.parent().statusBar().showMessage("No old log files to clear", 3000)
        
    def save_settings(self):
        """Save settings and close dialog"""
        self.apply_settings()
        self.accept()
        
    def apply_settings(self):
        """Apply settings without closing dialog"""
        # General settings
        config.set("sound_enabled", self.sound_enabled_checkbox.isChecked())
        config.set("music_volume", self.music_volume_slider.value())
        config.set("last_tab", self.start_tab_combo.currentIndex())
        
        # Appearance settings
        theme_name = self.theme_combo.currentText()
        if theme_name != theme_manager.current_theme:
            theme_manager.set_theme(theme_name)
            config.set("theme", theme_name)
        
        # Tools settings
        config.set("bitcrack_settings.threads", int(self.bitcrack_threads.currentText()))
        config.set("bitcrack_settings.blocks", int(self.bitcrack_blocks.currentText()))
        config.set("bitcrack_settings.points", int(self.bitcrack_points.currentText()))
        config.set("bitcrack_settings.device", self.bitcrack_device.text())
        
        config.set("keyhunt_settings.threads", int(self.keyhunt_threads.currentText()))
        config.set("keyhunt_settings.mode", self.keyhunt_mode.currentText())
        config.set("keyhunt_settings.ram", int(self.keyhunt_ram.currentText()))
        
        config.set("vanbit_settings.threads", int(self.vanbit_cpu.currentText()))
        config.set("vanbit_settings.grid", int(self.vanbit_grid_size.currentText()))
        
        # Advanced settings
        config.set("log_level", self.log_level_combo.currentText())
        config.set("log_retention_days", self.log_retention.value())
        
        # Save settings to file
        config.save_settings()
        
        # Emit signal to notify that settings have changed
        self.settings_changed.emit()
        
        # Log the changes
        logger.info("Settings updated")
        
        # Show status message
        if hasattr(self.parent(), 'statusBar'):
            self.parent().statusBar().showMessage("Settings saved", 3000) 