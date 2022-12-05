from model.message import Message
from database.database import PostsDatabase


def followHandler():
    pass

def unfollowHandler():
    pass

def postHandler(db: PostsDatabase, post_id: int, username: str, body: str):
    db.insert_post(post_id=post_id, username=username, body=body)

