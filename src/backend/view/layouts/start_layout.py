from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QFrame
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QGuiApplication

from ..consts import WINDOW_BACKGROUND_COLOR, WINDOW_COLOR, HIGHLIGHT_COLOR

class StartLayout(QHBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.username = ""
        self.setup()

    def setup(self):
        # Left side
        left_side = QVBoxLayout()
        left_side.addWidget(QWidget())

        # Center
        vertical_layout = QVBoxLayout()
        vertical_layout.setObjectName('vertical_layout')
        vertical_layout.setSpacing(0)
        
        title = QLabel('Singer')
        title.setObjectName('start_title')
        
        card_layout = QVBoxLayout()
        
        card = QGroupBox()
        card.setObjectName('auth_card')
        
        username_field = QLineEdit()
        username_field.setObjectName('username_field')
        username_field.setPlaceholderText("Username")
        username_field.textChanged.connect(self.username_changed)

        horizontal_layout = QHBoxLayout()
        
        login_button = QPushButton('Login')
        login_button.setObjectName('login_button')
        login_button.clicked.connect(self.login)

        register_button = QPushButton('Register')
        register_button.setObjectName('register_button')
        register_button.clicked.connect(self.register)
        
        horizontal_layout.addWidget(register_button)
        horizontal_layout.addWidget(login_button)
        
        card_layout.addWidget(username_field)
        card_layout.addLayout(horizontal_layout)

        card.setLayout(card_layout)
        
        vertical_layout.addWidget(title)
        vertical_layout.addWidget(card)
        
        # Right side
        right_side = QVBoxLayout()
        right_side.addWidget(QWidget())

        vertical_layout.addLayout(right_side)
        self.addLayout(vertical_layout)
    
    def login(self):
        self.parent.login(self.username)

    def register(self):
        self.parent.register(self.username)
        
    def username_changed(self, text):
        self.username = text