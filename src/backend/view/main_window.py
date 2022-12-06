from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QMainWindow, QVBoxLayout, QHBoxLayout, QWidgetAction
from PySide6.QtCore import Slot, Qt, QRunnable, QThreadPool, Signal, QObject
from PySide6.QtGui import QGuiApplication
import time

from .consts import WINDOW_BACKGROUND_COLOR, WINDOW_COLOR, HIGHLIGHT_COLOR
from .layouts.start_layout import StartLayout
from .layouts.timeline_layout import TimelineLayout

from model.user import User

class ReloadSignal(QObject):
    signal = Signal(int)

class Updater(QRunnable):
    signals = ReloadSignal()

    def __init__(self):
        super().__init__()
        
    def run(self):
        while True:
            self.signals.signal.emit(1)
            time.sleep(0.1)

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.title = 'Singer'        
        self.logged_in = False
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.controller = controller
        self.setup()

        self.threadpool = QThreadPool()
        self.updater = Updater()
        self.updater.signals.signal.connect(self.reload)
        self.threadpool.start(self.updater)
        
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
        self.logged_in = True
        
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
        self.logged_in = True

        layout = TimelineLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        widget = QWidget()
        widget.width = 400
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()
        
    def reload(self):
        if not self.logged_in: 
            return
        
        layout = TimelineLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        widget = QWidget()
        widget.width = 400
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()
        
    def logout(self):
        print("Logout")
        self.logged_in = False
        layout = StartLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        widget = QWidget()
        widget.width = 400
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()