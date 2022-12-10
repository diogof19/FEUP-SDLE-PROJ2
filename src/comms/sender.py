from asyncio import open_connection


class Sender:
    """
    Class responsible for sending messages
    """
    @staticmethod
    async def send_message(ip : str, port : int, message : str) -> None:
        """
        Sends a message to a user

        :param ip: The ip of the user
        :param port: The port of the user
        :param message: The message to be sent
        """
        try:
            _, writer = await open_connection(ip, port)
            writer.write(message.encode())
            await writer.drain()
            writer.close()
            return True
        except Exception as _:
            return False