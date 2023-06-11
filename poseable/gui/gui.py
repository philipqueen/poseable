import sys
import cv2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.backends.backend_qtagg as plt_backend
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog


class ImageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.load_button_label = QLabel("Choose an image to play around with below:")

        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)

        self.click_location = ()

        self.figure = plt.figure()

        self.canvas = plt_backend.FigureCanvasQTAgg(self.figure)

        self.toolbar = plt_backend.NavigationToolbar2QT(self.canvas, self)

        mouse_click = self.figure.canvas.mpl_connect("button_press_event", self.click_event)

        self.click_label = QLabel(self)
        self.click_label.setText("Click on the image to draw a circle. It's location will be printed!")

        layout = QVBoxLayout()

        layout.addWidget(self.load_button_label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.click_label)

        self.setLayout(layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "All Files (*);;Image Files (*.jpg *.jpeg *.png)")
        if file_name:
            self.image_path = file_name
            image = cv2.cvtColor(cv2.imread(str(self.image_path), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
            self.image = np.asarray(image)
            self.plot_image()

    def plot_image(self):
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)

        self.ax.imshow(self.image)
        self.figure.set_tight_layout(True)

        self.clicked_point_circle = None

        self.canvas.draw()

    def click_event(self, event):
        self.click_location = (int(event.xdata), int(event.ydata))

        print(f"you clicked at {self.click_location}")

        self.click_label.setText(f"you clicked at {self.click_location}")
        self.draw_circle_at_click()

    def draw_circle_at_click(self):
        if self.clicked_point_circle:
            self.clicked_point_circle.remove()
        self.clicked_point_circle = self.ax.scatter(self.click_location[0], self.click_location[1], facecolors='none', edgecolors='r')
        self.canvas.draw()


def run_me():
    app = QApplication(sys.argv)
    widget = ImageWidget()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_me()
