import os
from PyQt5.QtWidgets import (
    QLabel, QGridLayout,
    QWidget, QScrollArea,
    QPushButton, QListWidget,
    QInputDialog,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect

def load_files_paths(directory, valid_extensions):
    paths = []
    for path in os.listdir(directory):
        if path.lower().endswith(valid_extensions):
            paths.append(path)
    return paths

class TagStructuresWidget(QWidget):
    def __init__(self, app):
        super().__init__()
        self.images_paths = []
        self.app = app
        self.init_ui()

    def init_ui(self):
        self.files_list = QListWidget()
        self.files_list.itemClicked.connect(self.on_files_list_item_clicked)

        self.image_label = QLabel()
        self.image_label.mouseReleaseEvent = self.on_image_mouse_release
        self.image_label.setScaledContents(True)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setGeometry(QRect(0, 0, 400, 400))

        self.grid = QGridLayout()
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 3)
        self.grid.addWidget(self.files_list, 0, 0)
        self.grid.addWidget(self.scroll_area, 0, 1)

        back_btn = QPushButton("Powrót")
        back_btn.clicked.connect(self.app.go_home)

        self.grid.addWidget(back_btn, 1, 0)

        self.setLayout(self.grid)

    def on_image_mouse_release(self, event):
        # coś niezbyt się ustawia tam gdzie ma być
        label = QLabel(self.image_label)
        label.setText("1")
        label.move(event.pos().x(), event.pos().y())
        QInputDialog.getText(self, 'Nazywanie oznaczenia', 'Nazwij strukturę (pol, łac, ang):')


    def load_images_paths(self):
        self.images_paths = load_files_paths(self.app.workspace_directory, ("jpeg", "jpg", "png"))
        self.files_list.clear()
        for path in self.images_paths:
            self.files_list.addItem(path)

    def on_files_list_item_clicked(self, item):
        image_path = os.path.join(self.app.workspace_directory, item.text())
        self.image_label.setPixmap(QPixmap(image_path))