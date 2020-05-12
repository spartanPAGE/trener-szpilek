import os
from PyQt5.QtWidgets import (
    QLabel, QGridLayout,
    QWidget, QInputDialog,
    QPushButton, QListWidget,
)
from PyQt5.QtGui import QPixmap

from project.TaggableImageWidget import TaggableImageWidget

def load_files_paths(directory, valid_extensions):
    paths = []
    for path in os.listdir(directory):
        if path.lower().endswith(valid_extensions):
            paths.append(path)
    return paths

class TagWidget(QLabel):
    def __init__(self, text, tooltip, x, y):
        super().__init__()
        self.setText(text)
        self.move(x, y)
        self.setToolTip(tooltip)

class TagStructuresWidget(QWidget):
    def __init__(self, app):
        super().__init__()
        self.images_paths = []
        self.selected_image_path = ""
        self.app = app

        self.files_list = QListWidget()
        self.image_widget = TaggableImageWidget()
        self.image_widget.on_tag_added.connect(self.on_tag_added)
        self.init_ui()

    def init_ui(self):
        self.files_list.itemClicked.connect(self.on_files_list_item_clicked)

        self.grid = QGridLayout()
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 3)
        self.grid.addWidget(self.files_list, 0, 0)

        self.grid.addWidget(self.image_widget, 0, 1)

        back_btn = QPushButton("Zapisz i powróć")
        back_btn.clicked.connect(self.save_and_go_home)

        self.grid.addWidget(back_btn, 1, 0)

        self.setLayout(self.grid)

    def load_images_paths(self):
        self.images_paths = load_files_paths(self.app.workspace_path, ("jpeg", "jpg", "png"))
        self.files_list.clear()

        for path in self.images_paths:
            self.files_list.addItem(path)

    def on_files_list_item_clicked(self, item):
        self.selected_image_path = item.text()
        image_path = os.path.join(self.app.workspace_path, self.selected_image_path)
        self.image_widget.set_pixmap(QPixmap(image_path))
        self.image_widget.clear_tags()
        label_id = 0

        for tagdata in self.app.workspace_structures[self.selected_image_path]:
            label_id += 1
            self.image_widget.addWidget(TagWidget(str(label_id), tagdata['text'], tagdata['x'], tagdata['y']))

    def on_tag_added(self, x, y):
        text, ok = QInputDialog.getText(self, 'Wprowadź strukturę', 'Pol, Łac, Ang:')
        if ok:
            self.app.workspace_structures[self.selected_image_path].append({'text': text, 'x': x, 'y': y})
            label_id = str(len(self.app.workspace_structures[self.selected_image_path]))
            self.image_widget.addWidget(TagWidget(label_id, text, x, y))

    def save_and_go_home(self):
        self.app.save_workspace_structures()
        self.app.go_home()
