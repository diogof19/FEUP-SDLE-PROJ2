import sqlite3

from os.path import exists, join
from os import getcwd

from model.user_info import UserInfo

class PostsDatabase:
    """
    Class that handles the database for the posts

    In our network each node will have its own database
    This acts as a local cache
    """
    def __init__(self, username):
        self.db_path = join(getcwd(), 'database', 'db', f'{username}.db')
        exists_db = exists(self.db_path)
        self.username = username

        self.connection = sqlite3.connect(self.db_path, check_same_thread=False, isolation_level=None)

        if not exists_db:
            self.create_tables()

    def create_tables(self):
        """
        Creates the tables for the database
        """
        self.connection.execute(
            'CREATE TABLE posts (\
                post_id INTEGER NOT NULL,\
                username TEXT NOT NULL,\
                body TEXT NOT NULL,\
                date TEXT DEFAULT CURRENT_TIMESTAMP,\
                PRIMARY KEY(post_id, username)\
            );')
        self.connection.execute(
            'CREATE TABLE followers (\
                username TEXT PRIMARY KEY NOT NULL\
            );')
        self.connection.execute(
            'CREATE TABLE following (\
                username TEXT PRIMARY KEY NOT NULL,\
                was_notified BOOLEAN NOT NULL\
            );')

    def insert_post(self, post_id : int, username : str, body : str, date : str = None):
        """
        Inserts a post into the database
        """
        if date is None:
            self.connection.execute(
                'INSERT INTO posts (post_id, username, body) VALUES (?, ?, ?);',
                (post_id, username, body)
            )
        else:
            self.connection.execute(
                'INSERT INTO posts (post_id, username, body, date) VALUES (?, ?, ?, ?);',
                (post_id, username, body, date)
            )

    def add_follower(self, username: str):
        """
        Adds a follower to the database
        """
        self.connection.execute(
            'INSERT INTO followers  VALUES (?);',
            (username,)
        )

    def del_follower(self, username: str):
        """
        Deletes a follower from the database
        """
        self.connection.execute(
            'DELETE FROM followers WHERE username == ?;',
            (username,)
        )

    def get_followers(self):
        """
        Gets all the followers from the database
        """
        cursor = self.connection.execute(
            'SELECT username FROM followers;'
            )

        followers = cursor.fetchall()

        return [follower[0] for follower in followers]

    def add_following(self, username: str, was_notified: bool):
        """
        Adds a user to the following list
        """
        self.connection.execute(
            'INSERT INTO following (username, was_notified) VALUES (?, ?);',
            (username,was_notified)
        )

    def del_following(self, username: str):
        """
        Deletes a user from the following list
        """
        self.connection.execute(
            'DELETE FROM following WHERE username == ?;',
            (username,)
        )        
        self.del_posts_for_user(username)

    def get_following(self):
        """
        Gets all the users that the current user is following
        """
        cursor = self.connection.execute(
            'SELECT username FROM following'
            )
        
        following = cursor.fetchall()

        return [follow[0] for follow in following]

    def get_posts_for_user(self, username):
        """
        Gets all the posts for a user
        """
        cursor = self.connection.execute(
            'SELECT * FROM posts WHERE username = ? ORDER BY date DESC;',
            (username,)
        )

        return cursor.fetchall()
    
    def get_posts(self):
        """
        Gets all the posts from the database
        """
        cursor = self.connection.execute(
            'SELECT * FROM posts ORDER BY date DESC;'
        )
        
        return cursor.fetchall()

    def del_posts_for_user(self, username):
        """
        Deletes all the posts for a user
        """
        cursor = self.connection.execute(
            'DELETE FROM posts WHERE username = ?;',
            (username,)
        )

        return cursor.fetchall()
    

    def get_max_post_id_for_username(self, username):
        """
        Gets the id of the latest post for a user present in the database
        """
        cursor = self.connection.execute(
            'SELECT MAX(post_id) FROM posts WHERE username = ?;',
            (username,)
        )

        last_post_id = cursor.fetchone()

        return last_post_id[0] if last_post_id[0] is not None else 0

    def get_info(self):
        """
        Gets the info for the current user according to the database
        """
        followers = self.get_followers()
        following = self.get_following()
        last_post_id = self.get_max_post_id_for_username(self.username)

        return {
            'followers': followers,
            'following': following,
            'last_post_id': last_post_id
        }

    def is_following(self, username):
        """
        Checks if the current user is following a user
        """
        cursor = self.connection.execute(
            'SELECT * FROM following WHERE username = ?;',
            (username,)
        )
        if cursor.fetchone() is None:
            return False
        else:
            return True

    def get_date(self, username, post_id):
        """
        Gets the date of a post
        """
        cursor = self.connection.execute(
            'SELECT date FROM posts WHERE post_id = ? AND username = ?;',
            (post_id,username)
        )
        return cursor.fetchone()[0]

    def get_posts_since_post_id(self, username, post_id):
        """
        Gets all the posts for a user since a post id
        """
        cursor = self.connection.execute(
            'SELECT * FROM posts WHERE username = ? AND post_id > ? ORDER BY date DESC;',
            (username, post_id)
        )
        return cursor.fetchall()
        
    def get_unotified_following(self):
        cursor = self.connection.execute(
            'SELECT username FROM following WHERE was_notified == false;'
        )
        unot = cursor.fetchall()
        return [follow[0] for follow in unot]

    def notified_following(self, username):
        cursor = self.connection.execute(
            'UPDATE following SET was_notified == True WHERE username == ?;',
            (username,)
        )
