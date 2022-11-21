import threading
import asyncio

from node import Node
from .user_info import UserInfo
from .event_thread import EventThread
from database.database import PostsDatabase
from comms.listener import Listener


class User(Node):
    def __init__(self, ip  : str, port : int, username : str) -> None:
        super().__init__(ip, port)

        self.username = username

        self.database = None

        self.info = UserInfo()

        self.stop_ntp = threading.Event()
        self.ntp_thread = EventThread(self.stop_ntp)
        self.ntp_thread.start()

    def init_database(self):
        """
        Initialize the database for the user
        """
        self.database = PostsDatabase(self.username)

    def start_listening(self):
        """
        Start listening for incoming messages
        """
        listener = Listener(self.info.ip, self.info.port, self)
        listener.daemon = True
        listener.start()

    def stop(self) -> None:
        """
        Stop the node
        """
        self.stop_ntp.set()
        super().stop()
