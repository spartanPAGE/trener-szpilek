#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QApplication,
    QDesktopWidget
)

from project.HomeWidget import HomeWidget
from project.TagStructuresWidget import TagStructuresWidget

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.workspace_directory = ""
        self.init_ui()
        self.show()
        self.center()

    def init_ui(self):
        self.homeWidget = HomeWidget(self)
        self.tagStructuresWidget = TagStructuresWidget(self)

        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        self.stacked.addWidget(self.homeWidget)
        self.stacked.addWidget(self.tagStructuresWidget)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_workspace_directory(self, directory):
        self.workspace_directory = directory

    def launch_tag_structures(self):
        self.tagStructuresWidget.load_images_paths()
        self.stacked.setCurrentWidget(self.tagStructuresWidget)

    def go_home(self):
        self.stacked.setCurrentWidget(self.homeWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    App().show()
    sys.exit(app.exec_())
