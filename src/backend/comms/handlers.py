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

async def sync_handler(db: PostsDatabase, username: str, last_post_id: int, user):
    posts = db.get_posts_since_post_id(user.username, last_post_id)
    user_info = await user.get_kademlia_info(username)
    await user.send_message(user_info.ip, user_info.port, Message.send_posts(user.username, posts))

async def post_handler(db: PostsDatabase, post_id: int, username: str, body: str, date: str, user):
    if(db.is_following(username)):
        db.insert_post(post_id=post_id, username=username, body=body, date=date)
    else:
        messager_info = await user.get_kademlia_info(username)
        run_in_loop(user.send_message(messager_info.ip, messager_info.port, Message.unfollow_message(username)), user.loop)

async def send_posts_handler(db: PostsDatabase, posts: list, user):
    for post in posts:
        db.insert_post(post_id=post[0], username=post[1], body=post[2], date=post[3])

def set_own_kademlia_info_handler(user):
    run_in_loop(user.set_own_info(), user.loop)
