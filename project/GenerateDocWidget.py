
import os

from docx.shared import Inches
from docx import Document

from PyQt5.QtWidgets import QFileDialog, QLabel, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QEventLoop, QThread, QTimer, pyqtSignal

from project.TaggableImageWidget import TaggableImageWidget
from project.TagWidget import TagWidget

def put_tags_on_image_widget(image_widget: TaggableImageWidget, tags):
    for idx, tag in enumerate(tags, start=1):
        tag_widget = TagWidget(str(idx), "", tag["x"], tag["y"])
        tag_widget.adjust_to_size(image_widget.size(), 0.015)

        image_widget.add_widget(tag_widget)

def generate_doc(workspace_path, data_dictionary):
    document = Document()

    for imagename, tags in data_dictionary.items():
        if (len(tags) == 0):
            continue

        pixmap = QPixmap(os.path.join(workspace_path, imagename))

        image_widget = TaggableImageWidget(pixmap)
        image_widget.setMinimumSize(pixmap.size())
        put_tags_on_image_widget(image_widget, tags)

        temp_dir_path = os.path.join(workspace_path, "_dane_trenera_temp_")
        if not os.path.exists(temp_dir_path):
            os.mkdir(temp_dir_path)

        image_path = os.path.join(temp_dir_path, imagename)

        image_widget.save(image_path)
        document.add_picture(image_path, Inches(7.5))
        table = document.add_table(len(tags), cols=2)
        table.style = 'TableGrid'
        table.allow_autofit = False
        table.columns[0].width = Inches(0.5)
        table.columns[1].width = Inches(7)
        for idx, tag in enumerate(tags):
            table.rows[idx].cells[0].text = str(idx+1)
            table.rows[idx].cells[0].width = Inches(0.5)
            table.rows[idx].cells[1].text = tag["text"]
            table.rows[idx].cells[1].width = Inches(7)
            print(str(idx+1), tag["text"])

        document.add_page_break()

    sections = document.sections
    for section in sections:
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    return document

class GenerateDocWidget(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Generowanie dokumentu w toku...")

        layout = QVBoxLayout()
        label = QLabel()
        label.setText("Poczekaj, generuję dokument. Nic nie klikaj (w przyszłości będziesz mógł)")
        layout.addWidget(label)
        self.setLayout(layout)

    def start(self):
        loop = QEventLoop()
        QTimer.singleShot(1, self._on_timer)
        loop.exec_()

    def _on_timer(self):
        document = generate_doc(self.app.workspace_path, self.app.workspace_structures)
        self.hide()
        document_path = QFileDialog.getSaveFileName(None, "Zapisz dokument", "oznaczone struktury.docx", "docx (*.docx)")
        if document_path[0] != "":
            document.save(document_path[0])
        self.close()

