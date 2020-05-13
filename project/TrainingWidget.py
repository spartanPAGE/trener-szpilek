import random, os

from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QScrollArea
)

from PyQt5.QtGui import QIntValidator, QPixmap
from PyQt5.QtCore import Qt

from project.TaggableImageWidget import TaggableImageWidget

class TrainingStructure:
    def __init__(self, imagepath, data):
        self.image = imagepath
        self.data = data

class TrainingSummaryWidget(QWidget):
    def __init__(self, app, training_structures, user_answers):
        super().__init__()
        self.app = app
        self.structures_list = training_structures
        self.user_answers = user_answers
        self.arrow_pixmap = QPixmap("./resources/training-arrow.png")
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.scrollarea = QScrollArea(self)
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget()
        self.scrollarea.setWidget(widget)
        self.scrollarea_layout = QVBoxLayout(widget)
        self.layout.addWidget(self.scrollarea)

        images_pixmaps = {}

        idx = 0
        for structure in self.structures_list:
            image_widget = TaggableImageWidget()
            image_widget.setMinimumSize(400, 400)
            image_path = os.path.join(self.app.workspace_path, structure.image)
            image_widget.set_pixmap(images_pixmaps.setdefault(structure.image, QPixmap(image_path)))
            image_widget.set_highlighter_pixmap(self.arrow_pixmap)
            image_widget.set_highlighter_alignment(Qt.AlignLeft)
            image_widget.show_highlighter()
            self.scrollarea_layout.addWidget(image_widget)

            user_answer_label = QLabel()
            user_answer_label.setText("Twoja odpowiedź: {}".format(self.user_answers[idx]))
            self.scrollarea_layout.addWidget(user_answer_label)

            structure_name_label = QLabel()
            structure_name_label.setText("Prawidłowa odpw.: {}".format(structure.data["text"]))
            self.scrollarea_layout.addWidget(structure_name_label)

            idx += 1

        self.setLayout(self.layout)

class TrainingWidget(QWidget):
    def __init__(self, app, training_structures):
        super().__init__()
        self.app = app
        self.structures_list = training_structures
        self.current_structure_idx = -1
        self.user_answers = []
        self.image_widget = TaggableImageWidget()
        self.summary_widget: TrainingSummaryWidget
        self.init_ui()
        self.next_structure_or_finish()

    def init_ui(self):
        self.training: TrainingStructure
        self.grid = QGridLayout()
        self.grid.setRowStretch(0, 10)

        self.image_widget.set_highlighter_pixmap(QPixmap("./resources/training-arrow.png"))
        self.image_widget.set_highlighter_alignment(Qt.AlignLeft)
        self.grid.addWidget(self.image_widget, 0, 0)


        self.user_answer_lineedit = QLineEdit()
        self.user_answer_lineedit.setFixedHeight(30)
        self.user_answer_lineedit.returnPressed.connect(self.on_user_line_finished)
        self.grid.addWidget(self.user_answer_lineedit, 1, 0)

        self.setLayout(self.grid)

    def on_user_line_finished(self):
        self.user_answers.append("{}".format(self.user_answer_lineedit.text()))
        self.user_answer_lineedit.clear()
        self.next_structure_or_finish()

    def current_structure(self):
        return self.structures_list[
            self.current_structure_idx
        ]

    def next_structure_or_finish(self):
        self.current_structure_idx += 1
        if self.current_structure_idx >= len(self.structures_list):
            self.finish()
        else:
            self.next()

    def finish(self):
        self.summary_widget = TrainingSummaryWidget(
            self.app, self.structures_list, self.user_answers
        )
        self.summary_widget.setWindowTitle("Podsumowanie sesji treningowej")
        self.summary_widget.show()
        self.hide()

    def next(self):
        image_path = os.path.join(self.app.workspace_path, self.current_structure().image)
        self.image_widget.set_pixmap(QPixmap(image_path))
        self.image_widget.clear_tags()
        self.image_widget.move_highlighter(
            self.current_structure().data["x"],
            self.current_structure().data["y"]
        )
        self.image_widget.show_highlighter()


class PrepareTrainingWidget(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.max_structures_count: int
        self.training: TrainingWidget
        self.init_ui()

    def init(self):
        self.max_structures_count = sum([len(v) for v in self.app.workspace_structures.values()])
        validator = QIntValidator(0, self.max_structures_count, self)
        self.structures_count_lineedit.setValidator(validator)

        self.structures_count_label.setText(
            "Ile struktur w tym treningu? (max {})".format(self.max_structures_count)
        )

    def init_ui(self):
        self.structures_count_label = QLabel()

        self.structures_count_lineedit = QLineEdit()

        self.structures_count_lineedit.setMaximumWidth(200)

        self.back_btn = QPushButton("powrót")
        self.back_btn.clicked.connect(self.app.go_home)
        self.back_btn.setMaximumWidth(100)

        self.start_btn = QPushButton("Rozpocznij")
        self.start_btn.clicked.connect(self.start_trening)
        self.start_btn.setMaximumWidth(200)

        horizontal_layout = QHBoxLayout()
        vertical_layouts = [QVBoxLayout() for _ in range(4)]
        for vertical in vertical_layouts:
            horizontal_layout.addLayout(vertical)

        vertical_layouts[0].setAlignment(Qt.AlignBottom)
        vertical_layouts[0].addWidget(self.back_btn)

        vertical_layouts[1].setAlignment(Qt.AlignCenter)
        vertical_layouts[1].addWidget(self.structures_count_label)
        vertical_layouts[1].addWidget(self.structures_count_lineedit)
        vertical_layouts[1].addWidget(self.start_btn)
        horizontal_layout.addStretch()
        self.setLayout(horizontal_layout)

    def start_trening(self):
        structures_count = min(
            int(self.structures_count_lineedit.text()),
            self.max_structures_count
        )

        if structures_count <= 0:
            return

        workspace_structures = self.app.workspace_structures
        all_training_structures = []
        for image_path, tags in workspace_structures.items():
            for data in tags:
                all_training_structures.append(TrainingStructure(image_path, data))

        training_structures = random.sample(all_training_structures, structures_count)

        self.training = TrainingWidget(self.app, training_structures)
        self.training.setWindowTitle("Sesja treningowa")
        self.training.show()
