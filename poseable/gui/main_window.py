import sys
from pathlib import Path
from typing import Union

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout

from poseable.gui.widgets.image_markup_widget import ImageMarkupWidget

class PoseableMainWindow(QMainWindow):
    def __init__(self, parent: None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Poseable")
        self.setGeometry(100, 100, 1600, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)

        self.image_markup_widget = ImageMarkupWidget()
        self.layout.addWidget(self.image_markup_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PoseableMainWindow()
    window.show()
    app.exec()
