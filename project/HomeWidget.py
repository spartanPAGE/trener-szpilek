import os
from os.path import expanduser
from PyQt5.QtWidgets import (
    QLabel, QGridLayout,
    QWidget, QFileDialog,
    QPushButton,
)
from PyQt5.QtGui import QPixmap

class HomeWidget(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.requireing_workspace_buttons = []

        self.splash_screen()
        self.init_ui()
        self.show()

    def splash_screen(self):
        self.im = QPixmap("./resources/splash.png")
        self.label = QLabel()
        self.label.setPixmap(self.im)

    def init_ui(self):
        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 1, 1)

        self.grid.addLayout(self.buttons_layout(), 2, 1)

        self.setLayout(self.grid)

    def buttons_layout(self):
        workspace_btn = QPushButton("Wybierz folder roboczy")
        workspace_btn.clicked.connect(self.select_workspace)

        tag_structures_btn = QPushButton("Oznacz struktury")
        tag_structures_btn.clicked.connect(self.app.launch_tag_structures)

        train_structures_btn = QPushButton("trenuj szpilki")
        self.requireing_workspace_buttons = [tag_structures_btn, train_structures_btn]
        self.set_requireing_workspace_buttons_enabled(False)

        buttons_grid = QGridLayout()
        buttons_grid.addWidget(workspace_btn, 1, 1)
        buttons_grid.addWidget(tag_structures_btn, 1, 2)
        buttons_grid.addWidget(train_structures_btn, 1, 3)
        return buttons_grid

    def set_requireing_workspace_buttons_enabled(self, state):
        for btn in self.requireing_workspace_buttons:
            btn.setEnabled(state)

    def select_workspace(self):
        selected_directory = QFileDialog.getExistingDirectory(
            self,
            "Wybierz obszar (folder) roboczy",
            expanduser("~"),
            QFileDialog.ShowDirsOnly
        )

        if os.path.isdir(selected_directory):
            self.app.set_workspace_directory(selected_directory)
            self.set_requireing_workspace_buttons_enabled(True)