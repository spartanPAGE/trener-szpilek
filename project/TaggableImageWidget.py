from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGraphicsProxyWidget,
    QGraphicsPixmapItem
)
from PyQt5.QtCore import pyqtSignal, Qt
from project.QtImageViewer import QtImageViewer
from project.TagWidget import TagWidget

class PixmapNotSetError(Exception):
    pass

HIGHLIGHTER_ZORDER = 1000
class TaggableImageWidget(QWidget):
    on_tag_added = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self.tags = []
        self.highlighter: QGraphicsPixmapItem = None
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
        
    def set_highlighter_pixmap(self, pixmap):
        self.highlighter = self.image_viewer.scene.addPixmap(pixmap)
        self.highlighter.setZValue(HIGHLIGHTER_ZORDER)

    def addWidget(self, widget):
        self.tags.append(self.image_viewer.scene.addWidget(widget))

    def clear_tags(self):
        for tag in self.tags:
            self.image_viewer.scene.removeItem(tag)
        self.tags.clear()

    def show_highlighter(self):
        self.set_hightlighter_visibility_state(True)

    def hide_highlighter(self):
        self.set_hightlighter_visibility_state(False)

    def set_hightlighter_visibility_state(self, state):
        self.highlighter.setVisible(state)

    def highlight_tag_at(self, idx):
        if not self.highlighter:
            raise PixmapNotSetError

        tag_geometry = self.tag_at(idx).geometry()
        self.highlighter.setPos(tag_geometry.left()-self.highlighter.boundingRect().width()/2, tag_geometry.bottom())

    def tag_at(self, idx):
        return self._wrapped_tag_at(idx).widget()

    def remove_tag_at(self, idx):
        self.image_viewer.scene.removeItem(self._wrapped_tag_at(idx))

    def _wrapped_tag_at(self, idx):
        items = self.image_viewer.scene.items(Qt.AscendingOrder)

        offset = 1
        while not (
            isinstance(items[offset], QGraphicsProxyWidget) and
            isinstance(items[offset].widget(), TagWidget)
        ): offset += 1

        return self.image_viewer.scene.items(Qt.AscendingOrder)[idx+offset]
