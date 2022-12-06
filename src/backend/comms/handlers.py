from model.message import Message
from database.database import PostsDatabase

from utils.node_utils import run_in_loop


async def follow_handler(db: PostsDatabase, username: str, user):
    db.add_follower(username)
    user.info.followers.append(username)
    await user.set_kademlia_info(user.username, user.info)

async def unfollow_handler(db: PostsDatabase, username: str, user):
    db.del_follower(username)
    user.info.followers.remove(username)
    await user.set_kademlia_info(user.username, user.info)

async def post_handler(db: PostsDatabase, post_id: int, username: str, body: str, date: str, user):
    if(db.is_following(username)):
        db.insert_post(post_id=post_id, username=username, body=body, date=date)
    else:
        messager_info = await user.get_kademlia_info(username)
        run_in_loop(user.send_message(messager_info.ip, messager_info.port, Message.unfollow_message(username)), user.loop)

def set_own_kademlia_info_handler(user):
    run_in_loop(user.set_own_info(), user.loop)
