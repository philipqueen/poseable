import sys
from pathlib import Path
from typing import Union

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout

from poseable.gui.widgets.control_panel_dock_widget import ControlPanelDockWidget
from poseable.gui.widgets.image_markup_widget import ImageMarkupWidget

class PoseableMainWindow(QMainWindow):
    def __init__(self, parent: None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Poseable")
        self.setGeometry(100, 100, 1600, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QHBoxLayout(central_widget)

        self.image_markup_widget = ImageMarkupWidget()
        self.layout.addWidget(self.image_markup_widget)

        self.control_panel_dock_widget = ControlPanelDockWidget(parent=self)
        self.control_panel_dock_widget.setMinimumWidth(500)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.control_panel_dock_widget)
        
        self.image_markup_widget.clicked.connect(self.control_panel_dock_widget.control_panel_widget.handle_click_data)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PoseableMainWindow()
    window.show()
    app.exec()
