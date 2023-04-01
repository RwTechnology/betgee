from PyQt5.QtWidgets import QHBoxLayout, QLabel,QLineEdit,QPushButton, QDialog,QVBoxLayout,QGroupBox,QTimeEdit,QDateEdit, QDialog
from PyQt5.QtCore import Qt, QSize,QDate
from models.Match import Match


class PariageDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(300, 350)
