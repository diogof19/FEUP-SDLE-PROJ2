import logging
import asyncio
import sys

from kademlia.network import Server

from utils.node_utils import read_config_file

# python get.py <bootstrap node> <bootstrap port> <key>
# get.py 1.2.348 3244 SpecialKey


class Node:
    def __init__(self, ip : str, port : int, name : str, bootstrap_file : str) -> None:
        self.setup_logger()

        self.ip = ip
        self.port = port
        self.name = name

        self.connected_nodes = read_config_file(bootstrap_file)

        self.server = Server()
        
        asyncio.run(self.server.listen(self.port))
        asyncio.run(self.server.bootstrap(self.connected_nodes))

    def setup_logger(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("kademlia").setLevel(logging.INFO)

def main():
    node = Node(sys.argv[1], int(sys.argv[2]), sys.argv[3])


if __name__ == "__main__":
    main()