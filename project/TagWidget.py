from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QSize
class TagWidget(QLabel):
    def __init__(self, text, tooltip, x, y):
        super().__init__()
        self.setText(text)
        if (x is not None and y is not None):
            self.move(x, y)
        if (tooltip):
            self.setToolTip(tooltip)

    def adjust_to_size(self, size: QSize, ratio: float):
        pixels = min(size.width(), size.height()) * ratio
        self.setStyleSheet("font: {0}pt".format(pixels))