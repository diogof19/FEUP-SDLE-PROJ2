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
            );'
        )

    def insert_post(self, post_id : int, username : str, body : str):
        self.connection.execute(
            'INSERT INTO posts (post_id, username, body) VALUES (?, ?, ?);',
            (post_id, username, body)
        )

    def get_posts_for_user(self, username):
        cursor = self.connection.execute(
            'SELECT * FROM posts WHERE username = ? ORDER BY date DESC;',
            (username,)
        )
        
        return cursor.fetchall()

    def get_last_post_id_for_user(self, username):
        cursor = self.connection.execute(
            'SELECT id FROM posts WHERE username = ? ORDER BY date ASC;',
            (username,)
        )
        return cursor.fetchall()

        
