from node import Node
from .user_info import UserInfo


class User(Node):
    def __init__(self, ip, port) -> None:
        super().__init__(ip, port)