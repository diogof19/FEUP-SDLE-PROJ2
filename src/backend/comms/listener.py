import asyncio
from threading import Thread
from model.message import Message
from comms.handlers import post_handler,follow_handler, set_own_kademlia_info_handler, unfollow_handler, sync_handler, send_posts_handler

class Listener(Thread):
    """
    Class responsible for listening for incoming messages
    """
    def __init__(self, ip : str, port : int, user) -> None:
        super().__init__()
        self.ip = ip
        self.port = port
        self.user = user

    async def request_handler(self, reader, _) -> None:
        """
        Handles incoming requests.

        :param reader: The reader to read the request from
        """

        # If the user is not logged in, ignore the request
        # We wanted to take the node down however we encountered a bug in kadmelia
        # where depending on the position of the node in the hash table the other 
        # nodes in the network would lose their neighbours gradually and the network
        # would eventually collapse.
        # This issue was also encountered in other groups
        if(not self.user.logged_in):
            return

        message = await reader.read(-1)

        message = Message.parse_message(message)

        print(f"Received message: {message}")
        
        if(message['message_type'] == 'post'):
            await post_handler(self.user.database, message['post_id'], message['username'], message['body'], message['date'], self.user)
        elif(message['message_type'] == 'follow'):
            await follow_handler(self.user.database, message['username'], self.user)
        elif(message['message_type'] == 'unfollow'):
            await unfollow_handler(self.user.database, message['username'], self.user)
        elif (message['message_type'] == 'set_own_kademlia_info'):
            set_own_kademlia_info_handler(self.user)
        elif (message['message_type'] == 'sync_posts'):
            await sync_handler(self.user.database, message['username'], message['follow'], message['last_post_id'], self.user)
        elif (message['message_type'] == 'send_posts'):
            await send_posts_handler(self.user.database, message['posts'], self.user)
        else:
            print('Unknown message type', message['message_type'])

    async def serve(self):
        """
        Start listening for incoming messages
        """
        self.server = await asyncio.start_server(self.request_handler, self.ip, self.port)

        await self.server.serve_forever()

    def run(self):
        """
        Start the server
        """
        new_event_loop = asyncio.new_event_loop()
        new_event_loop.run_until_complete(self.serve())
