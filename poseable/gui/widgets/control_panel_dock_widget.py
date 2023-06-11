from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDockWidget,
    QVBoxLayout,
    QWidget,
    QLabel
)


class ControlPanelDockWidget(QDockWidget):
    def __init__(self, **kwargs):
        super().__init__("Control", parent=kwargs.get("parent"))

        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable)

        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)

        self.control_panel_widget = ControlPanelWidget(**kwargs)
        self.setWidget(self.control_panel_widget)


class ControlPanelWidget(QWidget):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(parent=parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.dummy_label = QLabel("Controls Here NOW! - Ram Dass")
        self.layout.addWidget(self.dummy_label)
