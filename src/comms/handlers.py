from model.message import Message
from database.database import PostsDatabase

from utils.node_utils import run_in_loop


async def follow_handler(db: PostsDatabase, username: str, user):
    """
    Handles a follow request

    :param db: The database to use
    :param username: The username of the user who followed
    :param user: The user who received the follow request
    """
    db.add_follower(username)
    user.info.followers.append(username)
    await user.set_kademlia_info(user.username, user.info)

async def unfollow_handler(db: PostsDatabase, username: str, user):
    """
    Handles an unfollow request

    :param db: The database to use
    :param username: The username of the user who unfollowed
    :param user: The user who received the unfollow request
    """
    db.del_follower(username)
    user.info.followers.remove(username)
    await user.set_kademlia_info(user.username, user.info)

async def sync_handler(db: PostsDatabase, username: str, follow: str, last_post_id: int, user):
    """
    Handles a sync request
    A sync request is made by a node that went offline and wants to sync the posts of the people it was following

    :param db: The database to use
    :param username: The username of the user who made the sync request
    :param follow: The username of the user who the node that went offline was following
    :param last_post_id: The last post id of the node that went offline
    :param user: The user who received the sync request
    """
    posts = db.get_posts_since_post_id(follow, last_post_id)
    user_info = await user.get_kademlia_info(username)
    await user.send_message(user_info.ip, user_info.port, Message.send_posts(user.username, posts))

async def post_handler(db: PostsDatabase, post_id: int, username: str, body: str, date: str, user):
    """
    Handles a post request
    """
    # If the user is following the user who posted, insert the post in the database
    if(db.is_following(username)):
        db.insert_post(post_id=post_id, username=username, body=body, date=date)
    # If the user is not following the user who posted send an unfollow request to remove the user from the followers list
    else:
        messager_info = await user.get_kademlia_info(username)
        run_in_loop(user.send_message(messager_info.ip, messager_info.port, Message.unfollow_message(user.username)), user.loop)

async def send_posts_handler(db: PostsDatabase, posts: list, user):
    """
    Handles a send posts request
    A send posts request is made in response to a sync request
    It contains the posts that the node that went offline missed
    """
    for post in posts:
        db.insert_post(post_id=post[0], username=post[1], body=post[2], date=post[3])

def set_own_kademlia_info_handler(user):
    """
    Handles a set own kademlia info request
    This is useful for bootsrap nodes, since they must be initialized first
    and kademlia only let us set a key value pair in the network
    if there are at minimum 2 nodes in the network
    """
    run_in_loop(user.set_own_info(), user.loop)
