import threading

from .node import Node
from .user_info import UserInfo
from .event_thread import EventThread
from .message import Message
from database.database import PostsDatabase
from comms.listener import Listener
from comms.sender import Sender


class User(Node):
    def __init__(self, ip  : str, port : int, username : str, bootstrap_file : str) -> None:
        super().__init__(ip, port, bootstrap_file)

        self.username = username

        self.database = None

        self.info = UserInfo(ip, port, [], [])

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

    async def follow(self, username : str) -> None:
        """
        Follow a user
        TODO: What happens when user is offline?
        """
        new_follow_info = await self.get_kademlia_info(username)

        if new_follow_info is None:
            raise Exception(f'User {username} not found')
        
        self.info.following.append(username)
        await self.set_kademlia_info(self.username, self.info)

        new_follow_info.followers.append(self.username)
        await self.set_kademlia_info(username, new_follow_info)

        await self.send_message(new_follow_info.ip, new_follow_info.port, Message.follow_message(self.username))

    async def unfollow(self, username : str) -> None:
        """
        Unfollow a user
        TODO: What happens when user is offline?
        """
        new_follow_info = await self.get_kademlia_info(username)

        if new_follow_info is None:
            raise Exception(f'User {username} not found')
        
        self.info.following.remove(username)
        self.set_kademlia_info(self.username, self.info)

        new_follow_info.followers.remove(self.username)
        self.set_kademlia_info(username, new_follow_info)

    async def post(self, body : str) -> None:
        """
        Post a message
        """
        self.info.increment_post_id()
        self.database.insert_post(self.info.last_post_id, self.username, body)
        
        await self.set_kademlia_info(self.username, self.info)

        for follower in self.info.followers:
            follower_info = await self.get_kademlia_info(follower)
            self.send_message(follower_info.ip, follower_info.port, Message.post_message(self.username, self.info.last_post_id, body))

        return True

    async def register(self) -> None:
        """
        Register the user
        """
        print(f'Registering user {self.username}')
        await self.set_kademlia_info(self.username, self.info)
        print(f'User {self.username} registered')
        self.init_database()

        return True