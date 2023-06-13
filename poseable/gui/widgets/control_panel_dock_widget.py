import numpy as np
from pathlib import Path
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import (
    QDockWidget,
    QVBoxLayout,
    QWidget,
    QLabel,
    QTableView,
    QFileDialog,
    QPushButton,
)

from poseable.core_processes.load_pose_estimation_data.load_mediapipe_data import (
    load_mediapipe_data,
)


class ControlPanelDockWidget(QDockWidget):
    def __init__(self, **kwargs):
        super().__init__("Control", parent=kwargs.get("parent"))

        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable)

        self.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )

        self.control_panel_widget = ControlPanelWidget()
        self.setWidget(self.control_panel_widget)


class ControlPanelWidget(QWidget):
    def __init__(
        self,
        parent=None,
    ):
        super().__init__(parent=parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.choose_data_file_button = QPushButton("choose npy file")
        self.choose_data_file_button.clicked.connect(self.select_file)

        self.active_data_path_label = QLabel("No data selected")

        self.load_data_button = QPushButton("load data")
        self.load_data_button.clicked.connect(self.load_data)
        self.load_data_button.setEnabled(False)

        # TODO: drop downs for camera, frame, num_tracked_points based on data model
        self.camera = 0
        self.frame = 500
        self.num_tracked_points = 33

        self.table_label = QLabel("Below is a table of your data")

        self.table = QTableView()

        self.save_data_button = QPushButton("This will save data soon")

        self.layout.addWidget(self.choose_data_file_button)
        self.layout.addWidget(self.active_data_path_label)
        self.layout.addWidget(self.load_data_button)
        self.layout.addWidget(self.table_label)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.save_data_button)

    def select_file(self):
        self.file_path, _ = QFileDialog.getOpenFileName(
            self, "Select npy file", "", "NumPy Files (*.npy);;All Files (*)"
        )
        if self.file_path:
            font_metrics = QFontMetrics(self.active_data_path_label.font())
            shortened_path = font_metrics.elidedText(
                str(self.file_path), Qt.TextElideMode.ElideMiddle, 450
            )
            self.active_data_path_label.setText(shortened_path)
            self.load_data_button.setEnabled(True)

    def load_data(self):
        if self.file_path:
            self.data = load_mediapipe_data(
                self.file_path,
                camera=self.camera,
                frame=self.frame,
                num_tracked_points=self.num_tracked_points,
            )
            self.load_data_to_table()
        else:
            raise Exception("No data selected")

    def load_data_to_table(self):
        self.model = TableModel(self.data)
        self.table.setModel(self.model)


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data[index.row(), index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self._data[index.row(), index.column()] = value
            return True
        return False

    # def headerData(self, col, orientation, role):
    #     if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
    #         return self._data.columns[col]

    def flags(self, index):
        return (
            Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsEditable
        )
