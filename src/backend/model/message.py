import json

class Message:
    @staticmethod
    def create_message(username : str, message_type : str, args : dict) -> str:
        """
        Create a message to be sent to another user
        """
        args['username'] = username
        args['message_type'] = message_type
        return json.dumps(args)