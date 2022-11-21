import json

from dataclasses import dataclass, asdict
from dataclasses_json import dataclass_json

@dataclass
@dataclass_json
class UserInfo:
    ip : str
    port : int
    followers : list[str]
    following : list[str]

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
            user_info_json["following"]
        )
