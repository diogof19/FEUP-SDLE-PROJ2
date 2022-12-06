import asyncio
from threading import Thread, Event
from model.message import Message
from comms.handlers import postHandler,followHandler, set_own_kademlia_info_handler, unfollowHandler

class Listener(Thread):
    def __init__(self, ip : str, port : int, user) -> None:
        super().__init__()
        self.ip = ip
        self.port = port
        self.user = user
        self.view = None

    async def request_handler(self, reader, _) -> None:
        """
        Handles incoming requests.
        """
        message = await reader.read(-1)

        message = Message.parse_message(message)

        print(f"Received message: {message}")
        
        if(message['message_type'] == 'post'):
            postHandler(self.user.database, message['post_id'], message['username'], message['body'], message['date'])
        elif(message['message_type'] == 'follow'):
            followHandler(self.user.database, message['username'], self.user)
        elif(message['message_type'] == 'unfollow'):
            unfollowHandler(self.user.database, message['username'])
        elif (message['message_type'] == 'set_own_kademlia_info'):
            set_own_kademlia_info_handler(self.user)
            
        self.view.reload()

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

    def set_view(self, view):
        self.view = view
