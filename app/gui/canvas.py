from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Canvas(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)

    def paintEvent(self, event: QPaintEvent):
        pass
