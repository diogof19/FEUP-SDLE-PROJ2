import sqlite3

from os.path import exists, join
from os import getcwd

class PostsDatabase:
    def __init__(self, username):
        self.db_path = join(getcwd(), 'database', 'db', f'{username}.db')
        exists_db = exists(self.db_path)

        self.connection = sqlite3.connect(self.db_path, check_same_thread=False, isolation_level=None)

        if not exists_db:
            self.create_tables()

    def create_tables(self):
        self.connection.execute(
            'CREATE TABLE posts (\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                post_id INTEGER NOT NULL,\
                username TEXT NOT NULL,\
                body TEXT NOT NULL,\
                date TEXT DEFAULT CURRENT_TIMESTAMP,\
                UNIQUE(post_id, username)\
            );\
            CREATE TABLE followers (\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                username TEXT NOT NULL,\
                UNIQUE(username)\
            );\
            CREATE TABLE following (\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                username TEXT NOT NULL,\
                UNIQUE(username)\
            );'
        )

    def insert_post(self, post_id : int, username : str, body : str):
        self.connection.execute(
            'INSERT INTO posts (post_id, username, body) VALUES (?, ?, ?);',
            (post_id, username, body)
        )

    def add_follower(self, username: str):
        self.connection.execute(
            'INSERT INTO followers (username) VALUES (?);',
            (username,)
        )

    def del_follower(self, username: str):
        self.connection.execute(
            'DELETE FROM followers WHERE username == ?;',
            (username,)
        )

    def get_followers(self):
        self.connection.execute(
            'SELECT username FROM followers;'
            )

    def add_following(self, username: str):
        self.connection.execute(
            'INSERT INTO following (username) VALUES (?);',
            (username,)
        )

    def del_following(self, username: str):
        self.connection.execute(
            'DELETE FROM following WHERE username == ?;',
            (username,)
        )        
        self.del_posts_for_user(username)

    def get_following(self):
        self.connection.execute(
            'SELECT username FROM following'
            )

    def get_posts_for_user(self, username):
        cursor = self.connection.execute(
            'SELECT * FROM posts WHERE username = ? SORT BY date DESC;',
            (username,)
        )

        return cursor.fetchall()

    def del_posts_for_user(self, username):
        cursor = self.connection.execute(
            'DELETE FROM posts WHERE username = ?;',
            (username,)
        )

        return cursor.fetchall()