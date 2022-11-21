import logging
import asyncio
import os

from kademlia.network import Server
from utils.node_utils import read_config_file
from models.user_info import UserInfo

class Node:
    def __init__(self, ip : str, port : int, bootstrap_file : str) -> None:
        self.setup_logger()

        self.ip = ip
        self.port = port

        self.connected_nodes = read_config_file(bootstrap_file)

        self.server = Server()
        
        asyncio.run(self.server.listen(self.port))
        asyncio.run(self.server.bootstrap(self.connected_nodes))

    def setup_logger(self) -> None:
        if os.getenv('DEBUG'):
            logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("kademlia").setLevel(logging.INFO)

    def set_kademlia_info(self, username : str, info : UserInfo) -> None:
        self.server.set(username, info.serialize)

    def get_kademlia_info(self, username : str) -> UserInfo:
        return UserInfo.deserialize(self.server.get(username))

    def stop(self) -> None:
        self.server.stop()
        asyncio.get_event_loop().stop()