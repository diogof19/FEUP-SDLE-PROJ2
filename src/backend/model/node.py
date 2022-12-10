import logging
import asyncio
import os

from kademlia.network import Server
from utils.node_utils import read_config_file
from model.user_info import UserInfo
from .message import Message
from comms.sender import Sender

from utils.node_utils import run_in_loop

class Node:
    def __init__(self, ip : str, port : int, bootstrap_file : str) -> None:
        self.setup_logger()

        self.ip = ip
        self.port = port

        self.connected_nodes = [(node['ip'], node['port']) for node in read_config_file(bootstrap_file) if node['ip'] != ip or node['port'] != port]

        self.loop = asyncio.get_event_loop()

        self.server = Server()
        
        self.loop.run_until_complete(self.server.listen(self.port))
        self.loop.run_until_complete(self.server.bootstrap(self.connected_nodes))
        self.loop.run_until_complete(self.server._refresh_table())

        for node in self.connected_nodes:
            run_in_loop(self.send_message(node[0], node[1], Message.set_own_kademlia_info_message()), self.loop)

    def setup_logger(self) -> None:
        """
        Setup the logger for kadmelia
        """
        if os.getenv('DEBUG'):
            logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("kademlia").setLevel(logging.INFO)

    async def send_message(self, dest_ip : str, dest_port : int, message : str) -> None:
        """
        Send a message to a node
        """
        return await Sender.send_message(dest_ip, dest_port, message)

    async def set_kademlia_info(self, username : str, info : UserInfo) -> None:
        """
        Set the kademlia info for a user
        """
        return await self.server.set(username, info.serialize)

    async def get_kademlia_info(self, username : str) -> UserInfo:
        """
        Get the kademlia info for a user
        """
        user_info = await self.server.get(username)
        if user_info is None:
            return None
        return UserInfo.deserialize(user_info)

    def stop(self) -> None:
        """
        Stop the node
        """
        self.server.stop()
        asyncio.get_event_loop().stop()