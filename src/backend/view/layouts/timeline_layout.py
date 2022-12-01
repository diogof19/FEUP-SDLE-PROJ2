from PySide6.QtWidgets import QVBoxLayout, QFrame, QGridLayout, QHBoxLayout, QLabel, QGroupBox, QSizePolicy
from PySide6.QtCore import Slot, Qt, QSize
from PySide6 import QtWidgets

class TimelineLayout(QGridLayout):
    def __init__(self):
        super().__init__()
        self.setup()
        
    def setup(self):
        
        posts_layout = QVBoxLayout()
        #posts_layout.setSpacing(0)
        
        posts = self.get_all_posts()
        for post in posts:
            layout = self.create_post_layout(post)
            posts_layout.addWidget(layout)
            #posts_layout.addLayout(layout)
        
        info_layout = QVBoxLayout()
        
        followers_title = QLabel('Followers:')
        followers_title.setObjectName('followers_title')
        info_layout.addWidget(followers_title)
        
        followers = self.get_all_followers()
        for follower in followers:
            layout = self.create_follow_layout(follower)
            info_layout.addLayout(layout)
        
        horizontal_separator = QFrame()
        horizontal_separator.setFrameStyle(QFrame.HLine | QFrame.Plain)
        
        info_layout.addWidget(horizontal_separator)
        
        following_title = QLabel('Following:')
        following_title.setObjectName('following_title')
        info_layout.addWidget(following_title)
        
        following = self.get_all_following()
        for follow in following:
            layout = self.create_follow_layout(follow)
            info_layout.addLayout(layout)
        
        separator = QFrame()
        separator.setFrameStyle(QFrame.VLine | QFrame.Plain)
        
        super().addLayout(posts_layout, 0, 0)
        super().addWidget(separator, 0, 1)
        super().addLayout(info_layout, 0, 2)
        
    def get_all_posts(self):
        post1 = {'username': 'User11111111111111111111', 'body':'Body text dsadasdasdsdadsadasdasdasdasdasdasdsadasdasdasdasdasdasdasdasdasdsdasdasdasdasdasdasdasdasdasdasdsdsdadasdasdasdasdasdsdadasdd', 'date': '2021-01-01'}
        post2 = {'username': 'User2', 'body':'Body text', 'date': '2021-01-01'}
        post3 = {'username': 'User2', 'body':'Body text', 'date': '2021-01-01'}
        post4 = {'username': 'User2', 'body':'Body text', 'date': '2021-01-01'}
        post5 = {'username': 'User2', 'body':'Body text', 'date': '2021-01-01'}
        post6 = {'username': 'User2', 'body':'Body text', 'date': '2021-01-01'}
        return [post1, post2, post3]
    
    def create_post_layout(self, post):
        card = QGroupBox()
        
        card.setMaximumWidth(1000)
        card.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        card.setObjectName('post_card')
        
        layout = QVBoxLayout()
        
        username = QLabel(post['username'])
        username.setObjectName('post_username')
        username.setAlignment(Qt.AlignLeft)
        username.setMargin(0)
        
        date = QLabel(post['date'])
        date.setObjectName('post_date')
        date.setAlignment(Qt.AlignRight)
        date.setMargin(0)
        
        title = QGroupBox()
        title.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        title.setObjectName('post_title')
        
        title_layout = QHBoxLayout()
        title_layout.setSpacing(0)
        title_layout.addWidget(username)
        title_layout.setSpacing(0)
        title_layout.addWidget(date)
        
        title.setLayout(title_layout)
        
        body = QLabel(post['body'])
        body.setObjectName('post_body')
        body.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        body.setAlignment(Qt.AlignLeft)
        body.setMargin(0)
        
        layout.maximumSize()
        layout.addWidget(title)
        layout.setSpacing(0)
        layout.addWidget(body)
        
        card.setLayout(layout)
        return card
    
    def get_all_following(self):
        return ['User3', 'User4']
    
    def get_all_followers(self):
        return ['User5', 'User6']
        
    def create_follow_layout(self, follow):
        layout = QHBoxLayout()
        
        username = QLabel(follow)
        username.setObjectName('follow_username')
        username.setAlignment(Qt.AlignLeft)
        username.setMargin(0)
        
        layout.addWidget(username)
        
        return layout
    