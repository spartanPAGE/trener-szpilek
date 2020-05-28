from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGraphicsProxyWidget,
    QGraphicsPixmapItem
)
from PyQt5.QtCore import QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPainter

from project.QtImageViewer import QtImageViewer
from project.TagWidget import TagWidget

class PixmapNotSetError(Exception):
    pass

class BadAlignmentSetError(Exception):
    pass

HIGHLIGHTER_ZORDER = 1000
class TaggableImageWidget(QWidget):
    on_tag_added = pyqtSignal(float, float)

    def __init__(self, pixmap = None):
        super().__init__()
        self.tags = []
        self.highlighter: QGraphicsPixmapItem = None
        self.highlighter_alignment = Qt.AlignCenter
        self.init_ui()
        if (pixmap):
            self.set_pixmap(pixmap)

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

    def add_widget(self, widget): self.addWidget(widget)

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

    def set_highlighter_alignment(self, alignment):
        self.highlighter_alignment = alignment

    def move_highlighter(self, x, y):
        if self.highlighter_alignment == Qt.AlignCenter:
            self.highlighter.setPos(
                x-self.highlighter.boundingRect().width()/2,
                y
            )
        elif self.highlighter_alignment == Qt.AlignLeft:
            self.highlighter.setPos(
                x,
                y
            )
        else:
            raise BadAlignmentSetError

    def highlight_tag_at(self, idx):
        if not self.highlighter:
            raise PixmapNotSetError

        tag_geometry = self.tag_at(idx).geometry()
        self.move_highlighter(tag_geometry.left(), tag_geometry.bottom())

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

    def image(self) -> QImage:
        return self.image_viewer.image()

    def save(self, path):
        size = self.image().size()
        image = QImage(size.width(), size.height(), QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(image)

        self.image_viewer.scene.render(painter, QRectF(image.rect()), QRectF(self.image().rect()))
        painter.end()
        image.save(path)
