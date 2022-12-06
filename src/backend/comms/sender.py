from asyncio import open_connection


class Sender:
    @staticmethod
    async def send_message(ip : str, port : int, message : str) -> None:
        try:
            _, writer = await open_connection(ip, port)
            writer.write(message.encode())
            await writer.drain()
            writer.close()
            print(f'Sent message to {ip}:{port} ({message})')
            return True
        except Exception as _:
            return False