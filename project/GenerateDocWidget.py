
import os

from docx.shared import Inches
from docx import Document

from PyQt5.QtWidgets import QFileDialog, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal

from project.TaggableImageWidget import TaggableImageWidget
from project.TagWidget import TagWidget

def put_tags_on_image_widget(image_widget: TaggableImageWidget, tags):
    for idx, tag in enumerate(tags, start=1):
        tag_widget = TagWidget(str(idx), "", tag["x"], tag["y"])
        tag_widget.adjust_to_size(image_widget.size(), 0.015)

        image_widget.add_widget(tag_widget)

class GenerateDocWorker(QThread):
    next_image_signal = pyqtSignal(str, int)
    def __init__(self, workspace_path, data_dictionary, parent=None):
        QThread.__init__(self, parent)
        self.running = False
        self.workspace_path = workspace_path
        self.data_dictionary = data_dictionary
        self.document: Document

    def run(self):
        self.running = True

        self.document = Document()

        self.process_data_dictionary(self.document)

        self.save_doc(self.document)

    def process_data_dictionary(self, document):
        idx = 0
        for imagename, tags in self.data_dictionary.items():
            idx += 1
            if (len(tags) == 0):
                continue
            self.next_image_signal.emit(imagename, idx)
            image_path = self.prepare_and_save_image(imagename, tags)
            self.append_to_doc(document, image_path, tags)

    def prepared_image_widget(self, imagename, tags):
        pixmap = QPixmap(os.path.join(self.workspace_path, imagename))

        image_widget = TaggableImageWidget(pixmap)
        image_widget.setMinimumSize(pixmap.size())
        put_tags_on_image_widget(image_widget, tags)
        return image_widget

    def prepared_temp_dir_path(self):
        temp_dir_path = os.path.join(self.workspace_path, "_dane_trenera_temp_")
        if not os.path.exists(temp_dir_path):
            os.mkdir(temp_dir_path)
        return temp_dir_path

    def prepare_and_save_image(self, imagename, tags):
        image_widget = self.prepared_image_widget(imagename, tags)
        temp_dir_path = self.prepared_temp_dir_path()
        image_path = os.path.join(temp_dir_path, imagename)
        image_widget.save(image_path)
        return image_path

    def append_to_doc(self, document, image_path, tags):
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

        document.add_page_break()

    def format_doc(self, document):
        sections = document.sections
        for section in sections:
            section.left_margin = Inches(0.5)
            section.right_margin = Inches(0.5)

    def save_doc(self, document):
        document_path = QFileDialog.getSaveFileName(
            None,
            "Zapisz dokument",
            "oznaczone struktury.docx",
            "docx (*.docx)"
        )
        if document_path[0] != "":
            document.save(document_path[0])

class GenerateDocWidget(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.worker = GenerateDocWorker(app.workspace_path, app.workspace_structures, app)
        self.worker.next_image_signal.connect(self.on_next_image)
        self.worker.finished.connect(self.on_worker_finished)
        self.init_ui()
        self.start()

    def init_ui(self):
        self.setWindowTitle("Generowanie dokumentu w toku...")
        self.edit = QTextEdit()
        self.edit.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        self.setLayout(layout)

    def on_next_image(self, imagename, idx):
        self.edit.append("[{0}/{1}]: {2}".format(
            idx, len(self.app.workspace_structures), imagename)
        )

    def start(self):
        self.worker.start()

    def on_worker_finished(self):
        self.close()
