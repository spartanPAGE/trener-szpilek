import os
from PyQt5.QtWidgets import (
    QLabel, QGridLayout,
    QWidget, QInputDialog,
    QPushButton, QListWidget,
    QTabWidget, QListWidgetItem
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

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
        self.structures_list = QListWidget()
        self.image_widget = TaggableImageWidget()
        self.init_ui()

    def init_ui(self):
        self.files_list.itemClicked.connect(self.on_files_list_item_clicked)
        self.structures_list.itemChanged.connect(self.on_structure_name_changed)
        self.image_widget.on_tag_added.connect(self.on_tag_added)

        self.grid = QGridLayout()
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 3)

        self.lists_tab = QTabWidget()
        self.lists_tab.addTab(self.files_list, "Zdjęcia")
        self.lists_tab.addTab(self.structures_list, "Struktury")

        self.grid.addWidget(self.lists_tab, 0, 0)

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

        self.structures_list.clear()
        for tagdata in self.app.workspace_structures[self.selected_image_path]:
            label_id += 1
            self.add_tag(label_id, tagdata)

    def on_tag_added(self, x, y):
        text, ok = QInputDialog.getText(self, 'Wprowadź strukturę', 'Pol, Łac, Ang:')
        if ok:
            structures = self.app.workspace_structures[self.selected_image_path]
            tagdata = {'text': text, 'x': x, 'y': y}
            structures.append(tagdata)

            label_id = len(self.app.workspace_structures[self.selected_image_path])
            self.add_tag(label_id, tagdata)

    def on_structure_name_changed(self, item):
        item_id = self.structures_list.indexFromItem(item).row()
        if len(item.text()) > 0:
            self.update_structure_name(item_id, item)
        else:
            self.delete_structure(item_id, item)

    def update_structure_name(self, item_id, item):
        # update tag
        tag = self.image_widget.tag_at(item_id)
        tag.setToolTip(item.text())
        # update structure text
        structures = self.app.workspace_structures[self.selected_image_path]
        structures[item_id]['text'] = item.text()

    def delete_structure(self, item_id, item):
        # delete from structures
        structures = self.app.workspace_structures[self.selected_image_path]
        del structures[item_id]
        # update list and tags, so IDs can be restored
        mocked_item = QListWidgetItem()
        mocked_item.setText(self.selected_image_path)
        self.on_files_list_item_clicked(mocked_item)

    def save_and_go_home(self):
        self.app.save_workspace_structures()
        self.app.go_home()

    def add_tag(self, label_id, tagdata):
        item_widget = QListWidgetItem()
        item_widget.setText(tagdata['text'])
        item_widget.setFlags(item_widget.flags() | Qt.ItemIsEditable)
        self.structures_list.addItem(item_widget)

        self.image_widget.addWidget(
            TagWidget(str(label_id),
            tagdata['text'],
            tagdata['x'],
            tagdata['y'])
        )
