from model.message import Message
from database.database import PostsDatabase

from utils.node_utils import run_in_loop


def followHandler(db: PostsDatabase, username: str, user):
    db.add_follower(username)
    user.info.followers.append(username)

def unfollowHandler(db: PostsDatabase, username: str):
    db.del_follower(username)

def postHandler(db: PostsDatabase, post_id: int, username: str, body: str, date: str):
    print('postHandler', post_id, username, body, date)
    print('following:', db.get_following())
    if(db.is_following(username)):
        db.insert_post(post_id=post_id, username=username, body=body, date=date)
    else:
        # unfollow
        pass

def set_own_kademlia_info_handler(user):
    run_in_loop(user.set_own_info(), user.loop)
