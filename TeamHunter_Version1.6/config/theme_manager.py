"""
Theme Manager for TeamHunter
Provides theme management and styling for the application
"""
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

class ThemeManager:
    """
    Manages application themes and provides styling
    """
    def __init__(self):
        self.themes = {
            "default": {
                "description": "Defualt Black A sleek and minimalistic black theme with bold red accents",
                "primary_color": "#E7481F",
                "secondary_color": "#A13316",
                "background_color": "#000000",
                "text_color": "#FFFFFF",
                "accent_color": "#FFD700",
                "button_color": "#E7481F",
                "button_text_color": "#FFFFFF",
                "button_hover_color": "#A13316",
                "tab_color": "#3D3D3D",
                "tab_selected_color": "#E7481F",
                "tab_text_color": "#FFFFFF",
                "tab_selected_text_color": "#FFFFFF",
                "border_color": "#555555",
                "success_color": "#28A745",
                "warning_color": "#FFC107",
                "error_color": "#DC3545",
                "info_color": "#17A2B8"
            },
            "bitcoin": {
                "description": "A bright and bold theme inspired by Bitcoin’s signature orange and gold.",
                "primary_color": "#F7931A",
                "secondary_color": "#D68411",
                "background_color": "#FFFFFF",
                "text_color": "#4D4D4D",
                "accent_color": "#FFD700",
                "button_color": "#F7931A",
                "button_text_color": "#FFFFFF",
                "button_hover_color": "#D68411",
                "tab_color": "#F5F5F5",
                "tab_selected_color": "#F7931A",
                "tab_text_color": "#4D4D4D",
                "tab_selected_text_color": "#FFFFFF",
                "border_color": "#CCCCCC",
                "success_color": "#28A745",
                "warning_color": "#FFC107",
                "error_color": "#DC3545",
                "info_color": "#17A2B8"
            },

            "black": {
                "description": "A sleek and minimalistic black theme with bold red accents",
                "primary_color": "#E7481F",
                "secondary_color": "#A13316",
                "background_color": "#000000",
                "text_color": "#FFFFFF",
                "accent_color": "#FFD700",
                "button_color": "#E7481F",
                "button_text_color": "#FFFFFF",
                "button_hover_color": "#A13316",
                "tab_color": "#3D3D3D",
                "tab_selected_color": "#E7481F",
                "tab_text_color": "#FFFFFF",
                "tab_selected_text_color": "#FFFFFF",
                "border_color": "#555555",
                "success_color": "#28A745",
                "warning_color": "#FFC107",
                "error_color": "#DC3545",
                "info_color": "#17A2B8"
            },

            "cyberpunk": {
                "description": "A futuristic neon theme inspired by cyberpunk aesthetics and city lights.",
                "primary_color": "#0FF0FC",
                "secondary_color": "#FF007F",
                "background_color": "#1A1A2E",
                "text_color": "#0FF0FC",
                "accent_color": "#FFD700",
                "button_color": "#FF007F",
                "button_text_color": "#FFFFFF",
                "button_hover_color": "#D4006A",
                "tab_color": "#16213E",
                "tab_selected_color": "#FF007F",
                "tab_text_color": "#0FF0FC",
                "tab_selected_text_color": "#FFFFFF",
                "border_color": "#FF007F",
                "success_color": "#00FF00",
                "warning_color": "#FFC107",
                "error_color": "#FF3131",
                "info_color": "#0FF0FC"
            },

            "dark": {
                "description": "A modern dark theme with deep gray tones and striking red highlights.",
                "primary_color": "#E7481F",
                "secondary_color": "#A13316",
                "background_color": "#2D2D2D",
                "text_color": "#FFFFFF",
                "accent_color": "#FFD700",
                "button_color": "#E7481F",
                "button_text_color": "#FFFFFF",
                "button_hover_color": "#A13316",
                "tab_color": "#3D3D3D",
                "tab_selected_color": "#E7481F",
                "tab_text_color": "#FFFFFF",
                "tab_selected_text_color": "#FFFFFF",
                "border_color": "#555555",
                "success_color": "#28A745",
                "warning_color": "#FFC107",
                "error_color": "#DC3545",
                "info_color": "#17A2B8"
            },

            "devil_flaming": {
                "description": "Fiery reds, dark shadows, and an intense, infernal vibe 🔥😈",
                "primary_color": "#FF0000",
                "secondary_color": "#8B0000",
                "background_color": "#1E0000",
                "text_color": "#FF4500",
                "accent_color": "#FFD700",
                "button_color": "#B22222",
                "button_text_color": "#FFFFFF",
                "button_hover_color": "#FF4500",
                "tab_color": "#300000",
                "tab_selected_color": "#FF0000",
                "tab_text_color": "#FF6347",
                "tab_selected_text_color": "#FFFFFF",
                "border_color": "#8B0000",
                "success_color": "#FF4500",
                "warning_color": "#FFA500",
                "error_color": "#8B0000",
                "info_color": "#FF6347"
            },

            "ice_blue": {
                "description": "Frozen whites, icy blues, and chilling cold vibes ❄️💙",
                "primary_color": "#00BFFF",
                "secondary_color": "#1E90FF",
                "background_color": "#E0F7FA",
                "text_color": "#005F8F",
                "accent_color": "#FFFFFF",
                "button_color": "#00CED1",
                "button_text_color": "#FFFFFF",
                "button_hover_color": "#4682B4",
                "tab_color": "#B0E0E6",
                "tab_selected_color": "#00BFFF",
                "tab_text_color": "#005F8F",
                "tab_selected_text_color": "#FFFFFF",
                "border_color": "#A0C4FF",
                "success_color": "#00FA9A",
                "warning_color": "#87CEFA",
                "error_color": "#4682B4",
                "info_color": "#00FFFF"
            },

            "light": {
                "description": "A bright and clean theme with soft gray and warm red elements.",
                "primary_color": "#E7481F",
                "secondary_color": "#A13316",
                "background_color": "#F8F9FA",
                "text_color": "#212529",
                "accent_color": "#FFD700",
                "button_color": "#E7481F",
                "button_text_color": "#FFFFFF",
                "button_hover_color": "#A13316",
                "tab_color": "#E9ECEF",
                "tab_selected_color": "#E7481F",
                "tab_text_color": "#212529",
                "tab_selected_text_color": "#FFFFFF",
                "border_color": "#DEE2E6",
                "success_color": "#28A745",
                "warning_color": "#FFC107",
                "error_color": "#DC3545",
                "info_color": "#17A2B8"
            },

            "matrix": {
                "description": "A hacker-inspired green-on-black theme straight out of The Matrix.",
                "primary_color": "#00FF00",
                "secondary_color": "#008800",
                "background_color": "#000000",
                "text_color": "#00FF00",
                "accent_color": "#FFFFFF",
                "button_color": "#008800",
                "button_text_color": "#00FF00",
                "button_hover_color": "#00AA00",
                "tab_color": "#001100",
                "tab_selected_color": "#00FF00",
                "tab_text_color": "#00FF00",
                "tab_selected_text_color": "#000000",
                "border_color": "#00FF00",
                "success_color": "#00FF00",
                "warning_color": "#FFFF00",
                "error_color": "#FF0000",
                "info_color": "#00FFFF"
            },

            "unicorn": {
                "description": "A playful and magical pastel theme with pinks, purples, and dreamy colors.",
                "primary_color": "#FF69B4",
                "secondary_color": "#9370DB",
                "background_color": "#F0F8FF",
                "text_color": "#4B0082",
                "accent_color": "#FFD700",
                "button_color": "#FF69B4",
                "button_text_color": "#FFFFFF",
                "button_hover_color": "#9370DB",
                "tab_color": "#E6E6FA",
                "tab_selected_color": "#FF69B4",
                "tab_text_color": "#4B0082",
                "tab_selected_text_color": "#FFFFFF",
                "border_color": "#D8BFD8",
                "success_color": "#00FF00",
                "warning_color": "#FFFF00",
                "error_color": "#FF0000",
                "info_color": "#00FFFF"
            }
        }
        self.current_theme = "black"
        
    def get_theme(self, theme_name=None):
        """Get a theme by name or the current theme if none specified"""
        if theme_name is None:
            theme_name = self.current_theme
            
        return self.themes.get(theme_name, self.themes["default"])
        
    def set_theme(self, theme_name):
        """Set the current theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False
        
    def apply_theme(self, app):
        """Apply the current theme to the application"""
        if not isinstance(app, QApplication):
            raise TypeError("Expected QApplication instance")
            
        theme = self.get_theme()
        
        # Create a palette for the application
        palette = QPalette()
        
        # Set colors based on theme
        palette.setColor(QPalette.ColorRole.Window, QColor(theme["background_color"]))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(theme["text_color"]))
        palette.setColor(QPalette.ColorRole.Base, QColor(theme["background_color"]))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(theme["tab_color"]))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(theme["background_color"]))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(theme["text_color"]))
        palette.setColor(QPalette.ColorRole.Text, QColor(theme["text_color"]))
        palette.setColor(QPalette.ColorRole.Button, QColor(theme["button_color"]))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(theme["button_text_color"]))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(theme["accent_color"]))
        palette.setColor(QPalette.ColorRole.Link, QColor(theme["primary_color"]))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(theme["primary_color"]))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(theme["button_text_color"]))
        
        # Apply the palette to the application
        app.setPalette(palette)

        return self.get_stylesheet()

        
    def get_stylesheet(self):
        """Get the stylesheet for the current theme"""
        theme = self.get_theme()
        
        return f"""
        QMainWindow, QDialog {{
            background-color: {theme["background_color"]};
            color: {theme["text_color"]};
        }}
        
        QPushButton {{
            background-color: {theme["button_color"]};
            color: {theme["button_text_color"]};
            border: 1px solid {theme["border_color"]};
            border-radius: 4px;
            padding: 5px 10px;
        }}
        
        QPushButton:hover {{
            background-color: {theme["button_hover_color"]};
        }}
        
        QPushButton:pressed {{
            background-color: {theme["secondary_color"]};
        }}
        
        QTabWidget::pane {{
            border: 1px solid {theme["border_color"]};
            background-color: {theme["background_color"]};
        }}
        
        QTabBar::tab {{
            background-color: {theme["tab_color"]};
            color: {theme["tab_text_color"]};
            border: 1px solid {theme["border_color"]};
            border-bottom: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            padding: 5px 10px;
            margin-right: 2px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {theme["tab_selected_color"]};
            color: {theme["tab_selected_text_color"]};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {theme["button_hover_color"]};
        }}
        
        QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox {{
            border: 1px solid {theme["border_color"]};
            border-radius: 4px;
            padding: 3px;
            background-color: {theme["background_color"]};
            color: {theme["text_color"]};
        }}
        
        QLabel {{
            color: {theme["text_color"]};
        }}
        
        QCheckBox {{
            color: {theme["text_color"]};
        }}
        
        QRadioButton {{
            color: {theme["text_color"]};
        }}
        
        QGroupBox {{
            border: 1px solid {theme["border_color"]};
            border-radius: 4px;
            margin-top: 10px;
            color: {theme["text_color"]};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
        }}
        
        QMenuBar {{
            background-color: {theme["background_color"]};
            color: {theme["text_color"]};
        }}
        
        QMenuBar::item:selected {{
            background-color: {theme["primary_color"]};
            color: {theme["button_text_color"]};
        }}
        
        QMenu {{
            background-color: {theme["background_color"]};
            color: {theme["text_color"]};
            border: 1px solid {theme["border_color"]};
        }}
        
        QMenu::item:selected {{
            background-color: {theme["primary_color"]};
            color: {theme["button_text_color"]};
        }}
        
        QProgressBar {{
            border: 1px solid {theme["border_color"]};
            border-radius: 4px;
            text-align: center;
        }}
        
        QProgressBar::chunk {{
            background-color: {theme["primary_color"]};
        }}
        
        QScrollBar:vertical {{
            border: 1px solid {theme["border_color"]};
            background: {theme["background_color"]};
            width: 15px;
            margin: 15px 0 15px 0;
        }}
        
        QScrollBar::handle:vertical {{
            background: {theme["button_color"]};
            min-height: 20px;
        }}
        
        QScrollBar:horizontal {{
            border: 1px solid {theme["border_color"]};
            background: {theme["background_color"]};
            height: 15px;
            margin: 0 15px 0 15px;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {theme["button_color"]};
            min-width: 20px;
        }}
        """
        
    def add_theme(self, name, theme_dict):
        """Add a new theme to the theme manager"""
        # Validate theme dict has all required keys
        required_keys = set(self.themes["default"].keys())
        if not required_keys.issubset(set(theme_dict.keys())):
            missing_keys = required_keys - set(theme_dict.keys())
            raise ValueError(f"Theme is missing required keys: {missing_keys}")
            
        self.themes[name] = theme_dict
        return True
        
# Create a singleton instance
theme_manager = ThemeManager() 