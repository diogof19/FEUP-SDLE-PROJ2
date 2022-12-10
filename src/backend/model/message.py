import json

class Message:

    @staticmethod
    def parse_message(message: str):
        message.strip()
        return json.loads(message)

    @staticmethod
    def create_message(username : str, message_type : str, args : dict) -> str:
        """
        Create a message to be sent to another user
        """
        args['username'] = username
        args['message_type'] = message_type
        return json.dumps(args)

    @staticmethod
    def follow_message(username : str) -> str:
        """
        Create a follow message
        """
        return Message.create_message(username, 'follow', {})

    @staticmethod
    def unfollow_message(username : str) -> str:
        """
        Create a unfollow message
        """
        return Message.create_message(username, 'unfollow', {})

    @staticmethod
    def post_message(username : str, post_id : int, body : str, date : str) -> str:
        """
        Create a post message
        """
        return Message.create_message(username, 'post', {'post_id': post_id, 'body': body, 'date': date})

    @staticmethod
    def set_own_kademlia_info_message() -> str:
        """
        Create a set own kademlia info message
        """
        return Message.create_message('', 'set_own_kademlia_info', {})

    @staticmethod
    def ping_message() -> str:
        """
        Create a ping message
        """
        return Message.create_message('', 'ping', {})


    @staticmethod
    def sync_missing(self_user, last_post_id, username) -> str:
        """
        Create a sync missing message
        """
        return Message.create_message(self_user, "sync_posts", {
            "last_post_id": last_post_id,
            "username": username,
        })


