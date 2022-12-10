import json

from dataclasses import dataclass, asdict
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class UserInfo:
    ip : str
    port : int
    followers : list[str]
    following : list[str]
    online : bool
    last_post_id : int = 0

    def increment_post_id(self) -> int:
        """
        Increment the last post id
        """
        self.last_post_id += 1
        return self.last_post_id

    @property
    def serialize(self):
        """
        Serialize the user info
        """
        return json.dumps(asdict(self))

    @staticmethod
    def deserialize(json_str: str):
        """
        Deserialize the user info
        """
        user_info_json = json.loads(json_str)
        return UserInfo(
            user_info_json["ip"],
            user_info_json["port"],
            user_info_json["followers"],
            user_info_json["following"],
            user_info_json["online"],
            user_info_json["last_post_id"]
        )
