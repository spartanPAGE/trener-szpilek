#!/usr/bin/env python3

import sys
import qdarkstyle
from PyQt5.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QApplication,
    QDesktopWidget,
    QSplashScreen,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QEventLoop

from project.HomeWidget import HomeWidget
from project.TagStructuresWidget import TagStructuresWidget
from project.TrainingWidget import TrainingWidget

from project.StructuresIO import save_structures, load_structures

def merged_structures_dicts(lhs, rhs):
    result = {}
    for imagepath, structures in rhs.items():
        if imagepath in lhs:
            result[imagepath] = lhs[imagepath] + structures
        else:
            result[imagepath] = structures.copy()
    return result

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.workspace_path = ""
        self.workspace_structures = {}
        self.init_ui()
        self.show()
        self.center()

    def init_ui(self):
        self.setWindowTitle("Trener Szpilek by Patryk Wertka")
        self.home_widget = HomeWidget(self)
        self.tag_structure_widget = TagStructuresWidget(self)
        self.training_widget = TrainingWidget(self)

        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        self.stacked.addWidget(self.home_widget)
        self.stacked.addWidget(self.tag_structure_widget)
        self.stacked.addWidget(self.training_widget)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def set_workspace_path(self, directory):
        self.workspace_path = directory

    def launch_tag_structures(self):
        self.tag_structure_widget.load_images_paths()
        self.stacked.setCurrentWidget(self.tag_structure_widget)

    def launch_training(self):
        self.stacked.setCurrentWidget(self.training_widget)

    def go_home(self):
        self.stacked.setCurrentWidget(self.home_widget)

    def load_workspace_structures(self):
        self.workspace_structures = load_structures(self.workspace_path)

    def save_workspace_structures(self):
        save_structures(self.workspace_path, self.workspace_structures)

    def import_structures(self, directory):
        imported_structures = load_structures(data_directory=directory)
        self.workspace_structures = merged_structures_dicts(
            self.workspace_structures,
            imported_structures
        )
        self.save_workspace_structures() 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    pixmap = QPixmap('./resources/splash.png');
    splash = QSplashScreen(pixmap)
    splash.show()

    loop = QEventLoop()
    QTimer.singleShot(2500, loop.quit)
    loop.exec_()

    splash.hide()
    App().show()
    sys.exit(app.exec_())

    
