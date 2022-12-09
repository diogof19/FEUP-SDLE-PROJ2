from .node import Node
from .user_info import UserInfo
from .message import Message
from database.database import PostsDatabase
from comms.listener import Listener

from os.path import exists, join
from os import getcwd

class User(Node):
    def __init__(self, ip  : str, port : int, username : str, bootstrap_file : str) -> None:
        super().__init__(ip, port, bootstrap_file)

        self.username = username
        self.logged_in = False
        self.database = None

        self.info = UserInfo(ip, port, [], [])
        self.listener = Listener(self.info.ip, self.info.port, self)
        self.listener.daemon = True
        self.start_listening()

    def init_database(self):
        """
        Initialize the database for the user
        """
        self.database = PostsDatabase(self.username)

    def start_listening(self):
        """
        Start listening for incoming messages
        """
        self.listener.start()

    async def follow(self, username : str) -> None:
        """
        Follow a user
        TODO: What happens when user is offline?
        """
        new_follow_info = await self.get_kademlia_info(username)
        
        if new_follow_info is None:
            return None
        
        self.info.following.append(username)
        await self.set_kademlia_info(self.username, self.info)
        
        self.database.add_following(username)

        await self.send_message(new_follow_info.ip, new_follow_info.port, Message.follow_message(self.username))
        
        return True

    async def unfollow(self, username : str) -> None:
        """
        Unfollow a user
        DONE: What happens when user is offline?
        unfollow is persisted in db and when another post is received 
        """
        unfollow_info = await self.get_kademlia_info(username)

        if unfollow_info is None:
            raise Exception(f'User {username} not found')
        
        self.info.following.remove(username)
        await self.set_kademlia_info(self.username, self.info)
        self.database.del_following(username)

        await self.send_message(unfollow_info.ip, unfollow_info.port, Message.unfollow_message(self.username))


    async def post(self, body : str) -> None:
        """
        Post a message
        """

        if(body.strip() == "" or body == None):
            return False

        self.info.increment_post_id()
        self.database.insert_post(self.info.last_post_id, self.username, body)
        
        await self.set_kademlia_info(self.username, self.info)

        print('followers:', self.info.followers)
        all_posts_sent = True

        for follower in self.info.followers:
            follower_info = await self.get_kademlia_info(follower)
            all_posts_sent = all_posts_sent and await self.send_message(follower_info.ip, follower_info.port, Message.post_message(self.username, self.info.last_post_id, body, self.database.get_date(self.info.last_post_id)))

        print('all posts sent:', all_posts_sent)

        return True

    async def register(self) -> None:
        """
        Register the user
        """
        print(f'Registering user {self.username}')

        if await self.get_kademlia_info(self.username) is not None:
            raise Exception(f'User {self.username} already exists')
        
        await self.set_kademlia_info(self.username, self.info)
        print(f'User {self.username} registered')
        self.init_database()
        self.logged_in = True
        return True

    async def login(self) -> None:
        """
        Login the user
        """
        print(f'Logging in user {self.username}')

        own_kademlia_info = await self.get_kademlia_info(self.username)
        
        if own_kademlia_info is not None:
            info = own_kademlia_info
            self.info = UserInfo(self.ip, self.port, info.followers, info.following, info.last_post_id)
            await self.set_kademlia_info(self.username, self.info)
            self.init_database()
            self.logged_in = True
            return True
        elif exists(join(getcwd(), 'database', 'db', f'{self.username}.db')):
            self.init_database()
            info = self.database.get_info()
            self.info = UserInfo(self.ip, self.port, info['followers'], info['following'], info['last_post_id'])
            await self.set_kademlia_info(self.username, self.info)
            self.logged_in = True
            return True

        print(f'User {self.username} not found')

        return False
    
    def get_followers(self):
        """
        Get the followers of the user
        """
        return self.info.followers
    
    def get_following(self):
        """
        Get the users the user is following
        """
        return self.info.following

    async def set_own_info(self):
        """
        Reset the user's own info
        """
        print("Setting own info")
        has_set_info = False
        while True:
            if has_set_info:
                break
            elif self.logged_in:
                has_set_info = await self.set_kademlia_info(self.username, self.info)
            continue
        print("Set own info")

    async def ping(self, username : str) -> bool:
        """
        Ping a user
        """
        print(f'Pinging user {username}')
        info = await self.get_kademlia_info(username)
        if info is None:
            return False
        print('info:', info)
        return await self.send_message(info.ip, info.port, Message.ping_message())