from PyQt5.QtWidgets import QLabel

class TagWidget(QLabel):
    def __init__(self, text, tooltip, x, y):
        super().__init__()
        self.setText(text)
        self.move(x, y)
        self.setToolTip(tooltip)
