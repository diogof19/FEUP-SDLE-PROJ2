import logging
import asyncio
import os

from kademlia.network import Server
from utils.node_utils import read_config_file
from model.user_info import UserInfo
from .message import Message
from comms.sender import Sender

class Node:
    def __init__(self, ip : str, port : int, bootstrap_file : str) -> None:
        self.setup_logger()

        self.ip = ip
        self.port = port

        self.connected_nodes = [(node['ip'], node['port']) for node in read_config_file(bootstrap_file) if node['ip'] != ip or node['port'] != port]

        print(self.connected_nodes)

        self.loop = asyncio.get_event_loop()

        self.server = Server()
        
        self.loop.run_until_complete(self.server.listen(self.port))
        self.loop.run_until_complete(self.server.bootstrap(self.connected_nodes))

    def setup_logger(self) -> None:
        if os.getenv('DEBUG'):
            logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("kademlia").setLevel(logging.INFO)

    def send_message(self, dest_ip : str, dest_port : int, message : str) -> None:
        self.loop.run_until_complete(Sender.send_message(dest_ip, dest_port, message))

    async def set_kademlia_info(self, username : str, info : UserInfo) -> None:
        await self.server.set(username, info.serialize)

    async def get_kademlia_info(self, username : str) -> UserInfo:
        """
        Get the kademlia info for a user
        """
        user_info = await self.server.get(username)
        if user_info is None:
            return None
        return UserInfo.deserialize(user_info)

    def stop(self) -> None:
        self.server.stop()
        asyncio.get_event_loop().stop()