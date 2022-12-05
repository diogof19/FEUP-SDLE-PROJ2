from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QMainWindow, QVBoxLayout, QHBoxLayout, QWidgetAction
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QGuiApplication

from .consts import WINDOW_BACKGROUND_COLOR, WINDOW_COLOR, HIGHLIGHT_COLOR
from .layouts.start_layout import StartLayout
from .layouts.timeline_layout import TimelineLayout

from model.user import User

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.title = 'Singer'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.controller = controller
        self.setup()
        
    def setup(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet(f'\
            background-color: {WINDOW_BACKGROUND_COLOR};\
            color: {WINDOW_COLOR};\
        ')
        
        layout = StartLayout(self)

        widget = QWidget()
        widget.width = 400
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()
        
    def login(self, username):
        print("Logging in as", username)
        self.controller.user.username = username
        self.controller.login()
        
        layout = TimelineLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        widget = QWidget()
        widget.width = 400
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()
        
    def register(self, username):
        print("Registering as", username)
        self.controller.user.username = username
        self.controller.register()
        
        layout = TimelineLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        widget = QWidget()
        widget.width = 400
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()
        
    def reload(self):
        print("Reloading")
        
        layout = TimelineLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        widget = QWidget()
        widget.width = 400
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()
        
    def do_search(self, text):
        print('Searching', text)
        
        #GET SEARCH RESULTS
        search_results = ['User1', 'User2', 'User3']
        
        layout = TimelineLayout(self, search_results=search_results)
        layout.setAlignment(Qt.AlignTop)
        
        widget = QWidget()
        widget.width = 400
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()