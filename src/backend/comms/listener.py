import asyncio
from threading import Thread, Event

class Listener(Thread):
    def __init__(self, ip : str, port : int, user) -> None:
        super().__init__()
        self.ip = ip
        self.port = port
        self.user = user

    async def request_handler(self, reader, _) -> None:
        """
        Handles incoming requests.
        """
        message = await reader.read(-1)

        print(message.decode())

        print(await self.user.get_kademlia_info(self.user.username))

        print(message)

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
