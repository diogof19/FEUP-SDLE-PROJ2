from PySide6.QtWidgets import QVBoxLayout, QFrame, QGridLayout, QHBoxLayout, QLabel, QGroupBox, QSizePolicy, QScrollArea, QLineEdit, QPushButton
from PySide6.QtCore import Slot, Qt, QSize
from PySide6 import QtWidgets

class TimelineLayout(QGridLayout):
    def __init__(self, parent):
        super().__init__()
        self.setup()
        self.parent = parent
        self.post_text = ""
        
    def setup(self):
        posts_layout = QVBoxLayout()
        
        posts = self.get_all_posts()
        for post in posts:
            card = self.create_post_card(post)
            posts_layout.addWidget(card)
            
        # ----------------- Info Area -----------------
        
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignTop)
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        followers_widget = self.create_followers_widget()
        info_layout.setSpacing(0)
        info_layout.addWidget(followers_widget)
        
        following_widget = self.create_following_widget()
        info_layout.setSpacing(15)
        info_layout.addWidget(following_widget)
        
        info_widget = QGroupBox()
        info_widget.setObjectName('info_widget')
        info_widget.setFixedHeight(600)
        info_widget.setContentsMargins(0, 0, 0, 0)
        info_widget.setAlignment(Qt.AlignTop)
    
        info_widget.setLayout(info_layout)
        
        # ----------------- Vertical Separator ----------------- #
        
        separator = QFrame()
        separator.setFrameStyle(QFrame.VLine | QFrame.Plain)
        
        # ----------------- Posts Scroll ----------------- #
        
        posts_widget = QtWidgets.QWidget()
        posts_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        posts_widget.setLayout(posts_layout)
        
        scroll_posts = QScrollArea()
        scroll_posts.setMaximumWidth(1200)
        scroll_posts.setWidgetResizable(True)
        scroll_posts.setContentsMargins(0, 0, 0, 0)
        scroll_posts.setViewportMargins(0, 0, 0, 0)
        scroll_posts.setObjectName('scroll_posts')
        scroll_posts.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        scroll_posts.setWidget(posts_widget)
        
        # ----------------- Create Posts ----------------- #
        
        input_post = QLineEdit()
        input_post.setObjectName('input_post')
        input_post.setPlaceholderText('Write something...')
        input_post.setFixedWidth(1000)
        input_post.setAlignment(Qt.AlignLeft)
        input_post.textChanged.connect(self.on_post_text_changed)
        
        create_post_button = QPushButton('Create Post')
        create_post_button.setObjectName('create_post_button')
        create_post_button.clicked.connect(self.create_post)
        create_post_button.setFixedWidth(200)
        
        create_post_layout = QHBoxLayout()
        create_post_layout.setSpacing(0)
        create_post_layout.addWidget(input_post)
        
        create_post_layout.setSpacing(0)
        create_post_layout.addWidget(create_post_button)
        
        # ----------------- Main Layout ----------------- #
        
        main_layout = QVBoxLayout()
        
        main_layout.setSpacing(0)
        main_layout.addLayout(create_post_layout)
        
        horizontal_separator = QFrame()
        horizontal_separator.setFrameStyle(QFrame.HLine | QFrame.Plain)
        horizontal_separator.setObjectName('horizontal_separator')
        
        main_layout.setSpacing(0)
        main_layout.addWidget(horizontal_separator)
        
        main_layout.setSpacing(0)
        main_layout.addWidget(scroll_posts)
        
        # ----------------- Add to layout ----------------- #
        
        super().addLayout(main_layout, 0, 0)
        super().addWidget(separator, 0, 1)
        super().addWidget(info_widget, 0, 2)
        
    def get_all_posts(self):
        post1 = {'username': 'User11111111111111111111', 'body':'Body text dsadasdasdsdadsadasdasdasdasdasdasdsadasdasdasdasdasdasdasdasdasdsdasdasdasdasdasdasdasdasdasdasdsdsdadasdasdasdasdasdsdadasdd', 'date': '2021-01-01'}
        post2 = {'username': 'User2', 'body':'Body text', 'date': '2021-01-01'}
        post3 = {'username': 'User2', 'body':'Body text', 'date': '2021-01-01'}
        post4 = {'username': 'User2', 'body':'Body text', 'date': '2021-01-01'}
        post5 = {'username': 'User2', 'body':'Body text', 'date': '2021-01-01'}
        post6 = {'username': 'User2', 'body':'Body text', 'date': '2021-01-01'}
        
        return [post1, post2, post3, post4, post5, post6]
    
    def create_post_card(self, post):
        card = QGroupBox()
        
        #card.setMaximumWidth(1000)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
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
        return ['User5', 'User6','User5', 'User6','User5', 'User6','User5', 'User6','User5', 'User6','User5', 'User6','User5', 'User6','User5', 'User6', 'User6','User5', 'User6','User5', 'User6','User5', 'User6','User5', 'User6','User5', 'User6','User5', 'User6']
        
    def create_follow_widget(self, follow):
        username = QLabel(follow)
        username.setObjectName('follow_username')
        username.setAlignment(Qt.AlignTop)
        username.setMargin(0)
        username.setFixedHeight(30)
        
        return username
    
    def create_followers_widget(self):
        widget = QGroupBox()
        widget.setObjectName('followers_widget')
        widget.setMaximumSize(400, 400)
        widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        
        layout = QVBoxLayout()
                
        followers_title = QLabel('Followers:')
        followers_title.setObjectName('followers_title')
        followers_title.setAlignment(Qt.AlignLeft)
        followers_title.setMargin(0)
        followers_title.setFixedHeight(30)

        layout.setSpacing(0)
        layout.addWidget(followers_title)
        
        followers_layout = QVBoxLayout()
        followers = self.get_all_followers()
        for follower in followers:
            follower_widget = self.create_follow_widget(follower)
            followers_layout.setSpacing(0)
            followers_layout.addWidget(follower_widget)
            
        followers_widget = QGroupBox()
        followers_widget.setObjectName('followers_list')
        followers_widget.setLayout(followers_layout)
        
        followers_scroll = QScrollArea()
        followers_scroll.setWidgetResizable(True)
        followers_scroll.setContentsMargins(0, 0, 0, 0)
        followers_scroll.setViewportMargins(0, 0, 0, 0)
        followers_scroll.setObjectName('followers_scroll')
        followers_scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        followers_scroll.setWidget(followers_widget)
        
        layout.addWidget(followers_scroll)
        widget.setLayout(layout)
        
        return widget
    
    def create_following_widget(self):
        widget = QGroupBox()
        widget.setObjectName('following_widget')
        widget.setMaximumSize(400, 400)
        widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        
        layout = QVBoxLayout()
                
        followers_title = QLabel('Following:')
        followers_title.setObjectName('following_title')
        followers_title.setAlignment(Qt.AlignLeft)
        followers_title.setMargin(0)
        followers_title.setFixedHeight(30)

        layout.setSpacing(0)
        layout.addWidget(followers_title)
        
        followers_layout = QVBoxLayout()
        followers = self.get_all_following()
        for follower in followers:
            follower_widget = self.create_follow_widget(follower)
            followers_layout.setSpacing(0)
            followers_layout.addWidget(follower_widget)
            
        followers_widget = QGroupBox()
        followers_widget.setObjectName('followers_list')
        followers_widget.setLayout(followers_layout)
        
        followers_scroll = QScrollArea()
        followers_scroll.setWidgetResizable(True)
        followers_scroll.setContentsMargins(0, 0, 0, 0)
        followers_scroll.setViewportMargins(0, 0, 0, 0)
        followers_scroll.setObjectName('followers_scroll')
        followers_scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        followers_scroll.setWidget(followers_widget)
        
        layout.addWidget(followers_scroll)
        widget.setLayout(layout)
        
        return widget
        
        
        
        following_widget = QGroupBox()
        following_widget.setObjectName('following_widget')
        following_widget.setMaximumSize(400, 300)
        following_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        
        followers_title = QLabel('Following:')
        followers_title.setObjectName('following_title')
        followers_title.setAlignment(Qt.AlignLeft)
        followers_title.setMargin(0)
        followers_title.setFixedHeight(30)
        
        following_layout = QVBoxLayout()
        following_layout.setSpacing(0)
        following_layout.addWidget(followers_title)
        
        following = self.get_all_following()
        for follow in following:
            widget = self.create_follow_widget(follow)
            following_layout.setSpacing(0)
            following_layout.addWidget(widget)
            
        following_widget.setLayout(following_layout)
        
        return following_widget
    
    def on_post_text_changed(self, text):
        self.post_text = text
    
    def create_post(self):
        print('Create post:', self.post_text)
        self.parent.actions()[1].trigger()