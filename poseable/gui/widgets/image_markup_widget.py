import sys
import cv2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.backends.backend_qtagg as plt_backend
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog


class ImageMarkupWidget(QWidget):
    clicked = pyqtSignal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frame_number = 0

        self.load_button_label = QLabel("Choose a video to play around with below:")

        self.load_video_button = QPushButton("Load Video")
        self.load_video_button.clicked.connect(self.load_video)

        self.next_frame_button = QPushButton("Next Frame")
        self.next_frame_button.clicked.connect(self.next_frame)
        self.next_frame_button.setEnabled(False)

        self.click_location = ()

        self.figure = plt.figure()

        self.canvas = plt_backend.FigureCanvasQTAgg(self.figure)

        self.toolbar = plt_backend.NavigationToolbar2QT(self.canvas, self)

        mouse_click = self.figure.canvas.mpl_connect("button_press_event", self.click_event)

        self.click_label = QLabel(self)
        self.click_label.setText("Click on the image to draw a circle. It's location will be printed!")
        self.frame_counter = QLabel(self)
        self.frame_counter.setText(f"Load video to display current frame")

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.load_button_label)
        self.layout.addWidget(self.load_video_button)
        self.layout.addWidget(self.next_frame_button)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.click_label)
        self.layout.addWidget(self.frame_counter)

        self.setLayout(self.layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.jpg *.jpeg *.png);;All Files (*)")
        if file_name:
            self.image_path = file_name
            image = cv2.cvtColor(cv2.imread(str(self.image_path), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
            self.image = np.asarray(image)
            self.plot_image()

    def load_video(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Video Files (*.mp4 *.mov)")
        if file_name:
            self.cap = cv2.VideoCapture(str(file_name))
            self.convert_image(self.read_frame())
            self.frame_number = 0
            self.frame_counter.setText(f"Current Frame: {self.frame_number}")
            self.plot_image()
            self.next_frame_button.setEnabled(True)

    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.handle_end_of_video()
        else:
            self.frame_number += 1
            self.frame_counter.setText(f"Current Frame: {self.frame_number}")
            return frame
        
    def convert_image(self, image):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.image = np.asarray(rgb_image)
        
    def handle_end_of_video(self):
        self.cap.release()
        print("end of video")

    def next_frame(self):
        self.convert_image(self.read_frame())
        self.plot_image()

    def plot_image(self):
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)

        self.ax.imshow(self.image)
        self.figure.set_tight_layout(True)

        self.clicked_point_circle = None

        self.canvas.draw()

    def click_event(self, event):
        if event.xdata is not None and event.ydata is not None:
            self.click_location = (int(event.xdata), int(event.ydata))
            print(f"you clicked at {self.click_location}")

            self.click_label.setText(f"you clicked at {self.click_location}")
            self.clicked.emit(self.click_location)
            self.draw_circle_at_click()

    def draw_circle_at_click(self):
        if self.clicked_point_circle:
            self.clicked_point_circle.remove()
        self.clicked_point_circle = self.ax.scatter(self.click_location[0], self.click_location[1], facecolors='none', edgecolors='r')
        self.canvas.draw()


def run_me():
    app = QApplication(sys.argv)
    widget = ImageMarkupWidget()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run_me()
