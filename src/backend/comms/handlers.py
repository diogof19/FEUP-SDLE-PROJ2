from model.message import Message
from database.database import PostsDatabase


def followHandler(db: PostsDatabase, username: str):
    db.add_follower(username)

def unfollowHandler(db: PostsDatabase, username: str):
    db.del_follower(username)

def postHandler(db: PostsDatabase, post_id: int, username: str, body: str):
    db.insert_post(post_id=post_id, username=username, body=body)


