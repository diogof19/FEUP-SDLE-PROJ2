from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QMainWindow, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QGuiApplication

from .consts import WINDOW_BACKGROUND_COLOR, WINDOW_COLOR, HIGHLIGHT_COLOR
from .layouts.start_layout import StartLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Singer'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.setup()
        
    def setup(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet(f'\
            background-color: {WINDOW_BACKGROUND_COLOR};\
            color: {WINDOW_COLOR};\
        ')

        layout = StartLayout()

        widget = QWidget()
        widget.width = 400
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()
        