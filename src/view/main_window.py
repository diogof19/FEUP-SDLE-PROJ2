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
    """
    Worker thread to update the timeline and followers list periodically
    """
    signals = ReloadSignal()

    def __init__(self):
        super().__init__()
        
    def run(self):
        while True:
            self.signals.signal.emit(1)
            time.sleep(0.1)

class MainWindow(QMainWindow):
    """
    GUI main window
    """
    def __init__(self, controller):
        super().__init__()
        self.title = 'Singer'        
        self.logged_in = False
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.controller = controller
        self.timeline_layout = None
        self.setup()

        # Start the background thread to update the timeline, followers list, etc.
        self.threadpool = QThreadPool()
        self.updater = Updater()
        self.updater.signals.signal.connect(self.update)
        self.threadpool.start(self.updater)
        
    def setup(self):
        """
        Start page layout
        """
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
        """
        Login to the system
        """
        print("Logging in as", username)
        self.controller.user.username = username
        self.controller.login()
        self.logged_in = True
        
        self.timeline_layout = TimelineLayout(self)
        self.timeline_layout.setAlignment(Qt.AlignTop)
        
        widget = QWidget()
        widget.width = 400
        widget.setLayout(self.timeline_layout)

        self.setCentralWidget(widget)

        self.show()
        
    def register(self, username):
        """
        Register to the system
        """
        print("Registering as", username)
        self.controller.user.username = username
        self.controller.register()
        self.logged_in = True

        self.timeline_layout = TimelineLayout(self)
        self.timeline_layout.setAlignment(Qt.AlignTop)
        
        widget = QWidget()
        widget.width = 400
        widget.setLayout(self.timeline_layout)

        self.setCentralWidget(widget)

        self.show()
        
    def reload(self):
        """
        Reload the timeline layout
        """
        if not self.logged_in: 
            return
        
        self.timeline_layout = TimelineLayout(self)
        self.timeline_layout.setAlignment(Qt.AlignTop)
        
        widget = QWidget()
        widget.width = 400
        widget.setLayout(self.timeline_layout)

        self.setCentralWidget(widget)

        self.show()
        
    def logout(self):
        """
        Logout from the system
        """
        print("Logout")
        
        self.logged_in = False
        self.timeline_layout = None
        self.controller.logout()
        layout = StartLayout(self)

        widget = QWidget()
        widget.width = 400
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        
    def update(self):
        """
        Update the posts, followers and following lists
        """
        if self.timeline_layout != None:
            self.timeline_layout.update_posts()
            self.timeline_layout.update_followers()
            self.timeline_layout.update_following()