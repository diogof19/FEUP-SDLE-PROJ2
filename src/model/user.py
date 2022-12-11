from .node import Node
from .user_info import UserInfo
from .message import Message
from database.database import PostsDatabase
from comms.listener import Listener
import asyncio
import json
from utils.node_utils import run_in_loop

from os.path import exists, join
from os import getcwd

class User(Node):
    def __init__(self, ip  : str, port : int, username : str, bootstrap_file : str) -> None:
        super().__init__(ip, port, bootstrap_file)

        self.username = username
        self.database = None

        self.info = UserInfo(ip, port, [], [], False)
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
        Works even if the user is offline
        """
        if(username == self.username):
            return False


        if self.database.is_following(username):
            return
        
        
    
        
        self.info.following.append(username)
        await self.set_kademlia_info(self.username, self.info)

        print(str(self.info.following))

        """
        If username is not running the program (is not in the hash table), its registered has an unotified following
        If username is running the program, his kademlia info is updated. Additionally, if he is currently online, a follow message is sent
        """
        if await self.ping(username):
            new_follow_info = await self.get_kademlia_info(username)
            new_follow_info.followers.append(self.username)
            await self.set_kademlia_info(username, new_follow_info)
            if new_follow_info.online:
                await self.send_message(new_follow_info.ip, new_follow_info.port, Message.follow_message(self.username))
                
            self.database.add_following(username, True)
        else:

            self.database.add_following(username, False)
        
        return True

    async def unfollow(self, username : str) -> None:
        """
        Unfollow a user
        Works even if the user is offline 
        """

        if(username == self.username):
            return False


        if not self.database.is_following(username):
            return

        
        
        self.info.following.remove(username)
        await self.set_kademlia_info(self.username, self.info)
        self.database.del_following(username)

        """
        if username is not running the program (is not in the hash table), we cant modify his entry or send an unfollow message
        """
        if await self.ping(username):
            unfollow_info = await self.get_kademlia_info(username)
            unfollow_info.followers.remove(self.username)
            await self.set_kademlia_info(username, unfollow_info)
            if unfollow_info.online:
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

        for follower in self.info.followers:
            follower_info = await self.get_kademlia_info(follower)
            if follower_info != None:
                await self.send_message(follower_info.ip, follower_info.port, Message.post_message(self.username, self.info.last_post_id, body, self.database.get_date(self.username, self.info.last_post_id)))

        return True

    async def register(self) -> None:
        """
        Register the user
        """
        print(f'Registering user {self.username}')

        if await self.get_kademlia_info(self.username) is not None:
            raise Exception(f'User {self.username} already exists')
        
        for node in self.connected_nodes:
            await self.send_message(node[0], node[1], Message.set_own_kademlia_info_message())
        
        self.info.online = True

        await self.set_kademlia_info(self.username, self.info)
        print(f'User {self.username} registered')
        self.init_database()
        return True

    async def logout(self) -> None:
        """
        Logout the user
        """
        self.info.online = False
        await self.set_kademlia_info(self.username, self.info)
        self.database = None
        return True

    async def login(self) -> None:
        """
        Login the user
        """
        print(f'Logging in user {self.username}')

        own_kademlia_info = await self.get_kademlia_info(self.username)
        
        if own_kademlia_info is not None:
            info = own_kademlia_info
            self.info = UserInfo(self.ip, self.port, info.followers, info.following, True, info.last_post_id)
            await self.set_kademlia_info(self.username, self.info)
            self.init_database()
            for node in self.connected_nodes:
                await self.send_message(node[0], node[1], Message.set_own_kademlia_info_message())
            await self.get_missing_posts()
            self.logged_in = True
            self.sync_followers()
            await self.sync_following()
            return True
        elif exists(join(getcwd(), 'database', 'db', f'{self.username}.db')):
            self.init_database()
            info = self.database.get_info()
            self.info = UserInfo(self.ip, self.port, info['followers'], info['following'], True, info['last_post_id'])
            await self.set_kademlia_info(self.username, self.info)
            for node in self.connected_nodes:
                await self.send_message(node[0], node[1], Message.set_own_kademlia_info_message())
            await self.get_missing_posts()

            self.logged_in = True
            return True

        print(f'User {self.username} not found')

        return False

    def sync_followers(self):
        """
        Sync the followers in the database

        Database followers list is updated according to the user's kademlia info
        """
        db_followers = self.database.get_followers()

        for follower in db_followers:
            if follower not in self.info.followers:
                self.database.del_follower(follower)
        
        for follower in self.info.followers:
            if follower not in db_followers:
                self.database.add_follower(follower)
    
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
        await self.set_kademlia_info(self.username, self.info)
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

    async def get_missing_posts(self) -> None:
        """
        Get the missing posts from the database when you are offline
        Since the previous last_post_id to the current last_post_id
        """
        set
        for following in self.info.following:
            last_post_id = self.database.get_max_post_id_for_username(following)
            message = Message.sync_missing(
                self.username, 
                last_post_id, 
                following
                )

            try:
                following_info = await self.get_kademlia_info(following)
                # If user is online get the missing posts from them
                if following_info is not None and following_info.online == True:
                    await self.send_message(following_info.ip, following_info.port, message)
                # If user is offline get the missing posts from their followers
                elif following_info is not None and following_info.online == False:
                    print(f'User {following} is offline')
                    for int_following in following_info.followers:
                        following_info = await self.get_kademlia_info(int_following)
                        if following_info is not None and following_info.online == True:
                            await self.send_message(following_info.ip, following_info.port, message)
                        elif following_info.online == False:
                            print(f'User {int_following} is offline')
            # If the user is not found in the try and get the missing posts from other accounts
            except ConnectionRefusedError:
                for int_following in self.info.following:
                    following_info = await self.get_kademlia_info(int_following)

                    if following_info.following in following:
                        try:
                            await self.send_message(following_info.ip, following_info.port, message)
                        except ConnectionRefusedError:
                            pass

    async def sync_following(self):
        """
        Sync users that self follows
        """
        print('test')
        for unotified in self.database.get_unotified_following():
            if await self.ping(unotified):
                new_follow_info = await self.get_kademlia_info(unotified)
                new_follow_info.followers.append(self.username)
                await self.set_kademlia_info(unotified, new_follow_info)
                await self.send_message(new_follow_info.ip, new_follow_info.port, Message.follow_message(self.username))
                self.database.notified_following(unotified)