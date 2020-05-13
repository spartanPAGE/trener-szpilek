import os
from os.path import expanduser
from PyQt5.QtWidgets import (
    QLabel, QGridLayout,
    QWidget, QFileDialog,
    QPushButton,
)
from PyQt5.QtGui import QPixmap

class TrainingWidget(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.init_ui()

    def init_ui(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
