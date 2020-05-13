from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout
)
from PyQt5.QtCore import pyqtSignal, Qt
from project.QtImageViewer import QtImageViewer

class TaggableImageWidget(QWidget):
    on_tag_added = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self.tags = []
        self.init_ui()

    def init_ui(self):
        self.image_viewer = QtImageViewer()
        self.image_viewer.leftMouseButtonDoubleClicked.connect(self.on_lmb_double_click)
        layout = QVBoxLayout()
        layout.addWidget(self.image_viewer)
        self.setLayout(layout)

    def on_lmb_double_click(self, x, y):
        self.on_tag_added.emit(x, y)

    def set_pixmap(self, pixmap):
        self.image_viewer.setImage(pixmap)

    def addWidget(self, widget):
        self.tags.append(self.image_viewer.scene.addWidget(widget))

    def clear_tags(self):
        for tag in self.tags:
            self.image_viewer.scene.removeItem(tag)
        self.tags.clear()

    def tag_at(self, idx):
        return self._tag_at_wrapped(idx).widget()

    def remove_tag_at(self, idx):
        self.image_viewer.scene.removeItem(self._tag_at_wrapped(idx))

    def _tag_at_wrapped(self, idx):
        return self.image_viewer.scene.items(Qt.AscendingOrder)[idx+1]