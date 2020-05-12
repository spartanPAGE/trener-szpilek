import os.path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel
)
from project.QtImageViewer import QtImageViewer

class TaggableImageWidget(QWidget):
    on_tag_added = pyqtSignal(x, y)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.image_viewer = QtImageViewer()
        self.image_viewer.leftMouseButtonDoubleClicked.connect(self.on_lmb_double_click)
        layout = QVBoxLayout()
        layout.addWidget(self.image_viewer)
        self.setLayout(layout)

    def on_lmb_double_click(self, x, y):
        on_tag_added.emit(x, y)

    def set_pixmap(self, pixmap):
        self.image_viewer.setImage(pixmap)
