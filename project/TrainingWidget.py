from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QLabel,
)

from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt

class TrainingWidget(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.max_structures_count: int
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
        pass
