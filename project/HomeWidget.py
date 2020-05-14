import os
from os.path import expanduser
from PyQt5.QtWidgets import (
    QGridLayout,
    QWidget,
    QFileDialog,
    QPushButton,
)

class HomeWidget(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.requireing_workspace_buttons = []

        self.init_ui()

    def init_ui(self):
        self.grid = QGridLayout()
        self.grid.setColumnStretch(0, 2)
        self.grid.setColumnStretch(3, 2)

        self.grid.addLayout(self.buttons_layout(), 2, 1)

        self.setLayout(self.grid)

    def buttons_layout(self):
        workspace_btn = QPushButton("Wybierz folder roboczy")
        workspace_btn.clicked.connect(self.select_workspace)

        import_structures_btn = QPushButton("Importuj struktury")
        import_structures_btn.clicked.connect(self.import_structures)

        tag_structures_btn = QPushButton("Oznacz struktury")
        tag_structures_btn.clicked.connect(self.app.launch_tag_structures)

        train_structures_btn = QPushButton("Trenuj szpilki")
        train_structures_btn.clicked.connect(self.app.launch_training)

        self.requireing_workspace_buttons = [
            import_structures_btn,
            tag_structures_btn,
            train_structures_btn,
        ]
        self.set_requireing_workspace_buttons_enabled(False)

        buttons_grid = QGridLayout()
        buttons_grid.addWidget(workspace_btn, 1, 1)
        buttons_grid.addWidget(import_structures_btn, 1, 2)
        buttons_grid.addWidget(tag_structures_btn, 1, 3)
        buttons_grid.addWidget(train_structures_btn, 1, 4)
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
            self.app.set_workspace_path(selected_directory)
            self.app.load_workspace_structures()
            self.set_requireing_workspace_buttons_enabled(True)

    def import_structures(self):
        selected_directory = QFileDialog.getExistingDirectory(
            self,
            "Wybierz obszar (folder) roboczy do zaimportowania",
            expanduser("~"),
            QFileDialog.ShowDirsOnly
        )

        if os.path.isdir(selected_directory):
            self.app.import_structures(selected_directory)
