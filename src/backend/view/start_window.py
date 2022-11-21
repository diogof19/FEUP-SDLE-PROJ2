from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QMainWindow, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QGuiApplication

from .consts import WINDOW_BACKGROUND_COLOR, WINDOW_COLOR, HIGHLIGHT_COLOR

class StartWindow(QMainWindow):
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

        vertical_layout = QVBoxLayout()

        username_field = QLineEdit()
        username_field.setStyleSheet(f'\
            background-color: {WINDOW_BACKGROUND_COLOR};\
            border: 3px solid {HIGHLIGHT_COLOR};\
            border-radius: 5px;\
        ')
        username_field.setPlaceholderText("Username")

        horizontal_layout = QHBoxLayout()
        
        login_button = QPushButton('Login')
        login_button.setToolTip('This s an example login_button')
        login_button.setStyleSheet("\
            background-color: #FFFFFF;\
            color: #000000;\
        ")
        login_button.clicked.connect(self.login)

        register_button = QPushButton('Register')
        register_button.setToolTip('This s an example register_button')
        register_button.setStyleSheet("\
            background-color: #FFFFFF;\
            color: #000000;\
        ")
        register_button.clicked.connect(self.register)

        horizontal_layout.addWidget(register_button)
        horizontal_layout.addWidget(login_button)
        
        vertical_layout.addWidget(username_field)
        vertical_layout.addLayout(horizontal_layout)

        widget = QWidget()
        widget.setLayout(vertical_layout)

        self.setCentralWidget(widget)

        self.show()
        
    @Slot()
    def login(self):
        print('PyQt5 login_button click')

    @Slot()
    def register(self):
        print('PyQt5 register_button click')