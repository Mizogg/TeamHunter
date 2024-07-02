from PyQt6.QtWidgets import QMessageBox

def TetrisAboutWindow():
    msgBox = QMessageBox(QMessageBox.Icon.Information, "Unavailable", "This feature is currently unavailable", QMessageBox.StandardButton.Ok)

    return msgBox

