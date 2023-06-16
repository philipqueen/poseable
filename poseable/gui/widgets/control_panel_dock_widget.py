import numpy as np
from pathlib import Path
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import (
    QDockWidget,
    QVBoxLayout,
    QWidget,
    QLabel,
    QTableView,
    QFileDialog,
    QPushButton,
    QComboBox
)

from poseable.core_processes.load_pose_estimation_data.load_mediapipe_data import (
    load_mediapipe_data,
)
from poseable.core_processes.pose_estimation_model_info.mediapipe_keypoints import (
    mediapipe_body_keypoints,
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

        self.select_key_point_label = QLabel("Select key point to edit")

        self.active_table_row_index = 0
        self.select_key_point_combo_box = QComboBox()
        for keypoint in mediapipe_body_keypoints:
            self.select_key_point_combo_box.addItem(keypoint)
        self.select_key_point_combo_box.currentIndexChanged.connect(self.set_active_table_row_index)

        self.table_label = QLabel("Below is a table of your data")

        self.table = QTableView()
        self.model = None

        self.save_data_button = QPushButton("This will save data soon")

        self.layout.addWidget(self.choose_data_file_button)
        self.layout.addWidget(self.active_data_path_label)
        self.layout.addWidget(self.load_data_button)
        self.layout.addWidget(self.select_key_point_label)
        self.layout.addWidget(self.select_key_point_combo_box)
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

    def handle_click_data(self, click_location: tuple):
        # Process the data from the Image Markup Widget
        print(f"updating data with click location")
        self.update_data(click_location)

    def update_data(self, click_location: tuple):
        if self.model:
            x_index = self.model.index(self.active_table_row_index, 0)
            self.model.setData(x_index, click_location[0], Qt.ItemDataRole.EditRole)
            y_index = self.model.index(self.active_table_row_index, 1)
            self.model.setData(y_index, click_location[1], Qt.ItemDataRole.EditRole)
            # self.table.setModel(self.model)
        else:
            print("No data loaded to table, cannot process click")

    def set_active_table_row_index(self):
        self.active_table_row_index = self.select_key_point_combo_box.currentIndex()


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
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Vertical:
                return str(mediapipe_body_keypoints[section])

            if orientation == Qt.Orientation.Horizontal:
                return str(["X","Y"][section])

    def flags(self, index):
        return (
            Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsEditable
        )
