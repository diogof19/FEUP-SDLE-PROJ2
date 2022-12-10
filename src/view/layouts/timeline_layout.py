from PySide6.QtWidgets import QVBoxLayout, QFrame, QGridLayout, QHBoxLayout, QLabel, QGroupBox, QSizePolicy, QScrollArea, QLineEdit, QPushButton, QStackedWidget
from PySide6.QtCore import Slot, Qt, QSize
from PySide6 import QtWidgets

class TimelineLayout(QGridLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.post_text = ""
        self.follow_text = ""
        self.follow_error_widget = None
        self.stacked_posts = None
        self.stacked_followers = None
        self.stacked_following = None
        
        super().setContentsMargins(0, 0, 0, 0)
        self.setup()
        
    def setup(self):
        """
        Timeline layout
        """
        header = QGroupBox()
        header.setObjectName('timeline_header')
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.setAlignment(Qt.AlignRight)
        
        name = QLabel(self.parent.controller.get_username())
        name.setObjectName('timeline_header_name')
        header_layout.addWidget(name)
        
        logout = QPushButton('Logout')
        logout.setObjectName('timeline_header_logout')
        logout.clicked.connect(self.logout)
        header_layout.addWidget(logout)
        
        header.setLayout(header_layout)
        
        # ----------------- Info Area -----------------
        
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignTop)
        info_layout.setContentsMargins(10, 10, 10, 10)
        
        followers_widget = self.create_followers_widget()
        self.stacked_followers = QStackedWidget()
        self.stacked_followers.addWidget(followers_widget)
        info_layout.setSpacing(0)
        info_layout.addWidget(self.stacked_followers)
        
        following_widget = self.create_following_widget()
        info_layout.setSpacing(15)
        info_layout.addWidget(following_widget)
        
        info_widget = QGroupBox()
        info_widget.setObjectName('info_widget')
        info_widget.setFixedHeight(600)
        info_widget.setAlignment(Qt.AlignTop)
    
        info_widget.setLayout(info_layout)
        
        # ----------------- Vertical Separator ----------------- #
        
        separator = QFrame()
        separator.setFrameStyle(QFrame.VLine | QFrame.Plain)
        
        # ----------------- Posts Scroll ----------------- #
        
        posts_widget = self.create_posts_widget()
        
        self.stacked_posts = QStackedWidget()
        self.stacked_posts.addWidget(posts_widget)
        
        scroll_posts = QScrollArea()
        scroll_posts.setMaximumWidth(1200)
        scroll_posts.setWidgetResizable(True)
        scroll_posts.setContentsMargins(0, 0, 0, 0)
        scroll_posts.setViewportMargins(0, 0, 0, 0)
        scroll_posts.setObjectName('scroll_posts')
        scroll_posts.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        scroll_posts.setWidget(self.stacked_posts)
        
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
        create_post_button.clicked.connect(lambda: input_post.clear())
        create_post_button.setFixedWidth(200)
        
        create_post_layout = QHBoxLayout()
        create_post_layout.setSpacing(0)
        create_post_layout.addWidget(input_post)
        
        create_post_layout.setSpacing(0)
        create_post_layout.addWidget(create_post_button)
        
        # ----------------- Main Layout ----------------- #
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        
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
        
        super().addWidget(header, 0, 0, 1, 3)
        super().addLayout(main_layout, 1, 0)
        super().addWidget(separator, 1, 1)
        super().addWidget(info_widget, 1, 2)
        
    def get_all_posts(self):
        """
        Get all posts from the database
        """
        posts = self.parent.controller.get_posts(self.parent.controller.get_username())
        return posts
    
    def create_posts_widget(self):
        """
        Create the posts widget
        """
        posts_layout = QVBoxLayout()
        posts_layout.setAlignment(Qt.AlignTop)
        
        posts = self.get_all_posts()
        for post in posts:
            card = self.create_post_card(post)
            posts_layout.setSpacing(10)
            posts_layout.addWidget(card)
            
        posts_widget = QtWidgets.QWidget()
        posts_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        posts_widget.setLayout(posts_layout)
        
        return posts_widget
    
    def create_post_card(self, post):
        """
        Creates a post card
        """
        card = QGroupBox()
        
        #card.setMaximumWidth(1000)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        card.setObjectName('post_card')
        
        layout = QVBoxLayout()
        
        username = QLabel(post[1])
        username.setObjectName('post_username')
        username.setAlignment(Qt.AlignLeft)
        username.setMargin(0)
        
        date = QLabel(post[3])
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
        
        body = QLabel(post[2])
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
        """
        Get all following from the database
        """
        return self.parent.controller.get_following()
    
    def get_all_followers(self):
        """
        Get all followers from the database    
        """
        return self.parent.controller.get_followers()
    
    def on_follow_text_changed(self, text):
        """
        When the follow text changes
        """
        self.follow_text = text
        
    def unfollow(self, username):
        """
        Unfollow a user
        """
        print('unfollow:', username)
        self.parent.controller.unfollow(username)
        self.update_following()
        
    def update_followers(self):
        """
        Update the followers widget
        """
        if self.stacked_followers != None:
            followers = self.create_followers_widget()
            self.stacked_followers.removeWidget(self.stacked_followers.currentWidget())
            self.stacked_followers.addWidget(followers)
            self.stacked_followers.setCurrentWidget(followers)
        
    def follow(self):
        """
        Follow a user
        """
        if not self.parent.controller.follow(self.follow_text):
            self.follow_error_widget.show()
        else:
            self.follow_error_widget.hide()
            self.update_following()
        
        
    def create_follow_widget(self, follow):
        """
        Create a follow widget
        """
        username = QLabel(follow)
        username.setObjectName('follow_username')
        username.setAlignment(Qt.AlignTop)
        username.setMargin(0)
        username.setFixedHeight(30)
        
        return username
    
    def create_followers_widget(self):
        """
        Create the followers widget
        """
        widget = QGroupBox()
        widget.setObjectName('followers_widget')
        widget.setMaximumHeight(400)
        widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        followers_title = QLabel('Followers:')
        followers_title.setObjectName('followers_title')
        followers_title.setAlignment(Qt.AlignLeft)
        followers_title.setMargin(0)
        followers_title.setFixedHeight(30)

        layout.setSpacing(0)
        layout.addWidget(followers_title)
        
        followers_layout = QVBoxLayout()
        followers_layout.setAlignment(Qt.AlignTop)
        followers = self.get_all_followers()
        for follower in followers:
            follower_widget = self.create_follow_widget(follower)
            followers_layout.setSpacing(0)
            followers_layout.addWidget(follower_widget)
            
        followers_widget = QGroupBox()
        followers_widget.setObjectName('followers_list')
        followers_widget.setMaximumHeight(400)
        followers_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        followers_widget.setLayout(followers_layout)
        
        followers_scroll = QScrollArea()
        followers_scroll.setWidgetResizable(True)
        followers_scroll.setContentsMargins(0, 0, 0, 0)
        followers_scroll.setViewportMargins(0, 0, 0, 0)
        followers_scroll.setObjectName('followers_scroll')
        followers_scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        followers_scroll.setWidget(followers_widget)
        
        layout.setSpacing(0)
        layout.addWidget(followers_scroll)
        
        widget.setLayout(layout)
        
        return widget
    
    def update_following(self):
        """
        Update the following widget
        """
        if self.stacked_following != None:
            following = self.create_following_list_widget()
            self.stacked_following.removeWidget(self.stacked_following.currentWidget())
            self.stacked_following.addWidget(following)
            self.stacked_following.setCurrentWidget(following)
    
    def create_following_list_widget(self):
        """
        Create the following list widget
        """
        followers_layout = QVBoxLayout()
        followers_layout.setAlignment(Qt.AlignTop)
        
        followers = self.get_all_following()
        for follower in followers:
            follower_layout = QHBoxLayout()
            
            follower_name = self.create_follow_widget(follower)
            follower_name.setAlignment(Qt.AlignLeft)
            
            unfollow_button = QPushButton('Unfollow')
            unfollow_button.setObjectName('unfollow_button')
            unfollow_button.clicked.connect(lambda: self.unfollow(follower))
            
            follower_layout.setSpacing(0)
            follower_layout.addWidget(follower_name)
            follower_layout.setSpacing(0)
            follower_layout.addWidget(unfollow_button)
            
            followers_layout.setSpacing(0)
            followers_layout.addLayout(follower_layout)
            
            
        followers_widget = QGroupBox()
        followers_widget.setObjectName('followers_list')
        followers_widget.setMaximumHeight(400)
        followers_widget.setLayout(followers_layout)
        followers_widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        
        return followers_widget
    
    def create_following_widget(self):
        """
        Create the following widget
        """
        widget = QGroupBox()
        widget.setObjectName('following_widget')
        widget.setMaximumHeight(600)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        
        layout = QVBoxLayout()
                
        followers_title = QLabel('Following:')
        followers_title.setObjectName('following_title')
        followers_title.setAlignment(Qt.AlignLeft)
        followers_title.setMargin(0)
        followers_title.setFixedHeight(30)

        layout.setSpacing(0)
        layout.addWidget(followers_title)
        
        followers_widget = self.create_following_list_widget()
        
        self.stacked_following = QStackedWidget()
        self.stacked_following.addWidget(followers_widget)
        
        followers_scroll = QScrollArea()
        followers_scroll.setWidgetResizable(True)
        followers_scroll.setContentsMargins(0, 0, 0, 0)
        followers_scroll.setViewportMargins(0, 0, 0, 0)
        followers_scroll.setObjectName('followers_scroll')
        followers_scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        followers_scroll.setWidget(self.stacked_following)
        
        layout.addWidget(followers_scroll)
        
        follow_input = QLineEdit()
        follow_input.setObjectName('input_post')
        follow_input.setPlaceholderText('Username')
        follow_input.setMaximumWidth(300)
        follow_input.setAlignment(Qt.AlignLeft)
        follow_input.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        follow_input.textChanged.connect(self.on_follow_text_changed)
        
        follow_button = QPushButton('Follow')
        follow_button.setObjectName('create_post_button')
        follow_button.clicked.connect(self.follow)
        follow_button.clicked.connect(follow_input.clear)
        follow_button.setMaximumWidth(100)
        follow_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        
        self.follow_error_widget = QLabel('Unable to follow user.')
        self.follow_error_widget.setObjectName('follow_error')
        self.follow_error_widget.setAlignment(Qt.AlignLeft)
        self.follow_error_widget.hide()
        
        follow_layout = QGridLayout()
        follow_layout.setAlignment(Qt.AlignLeft)
        follow_layout.setSpacing(0)
        follow_layout.addWidget(follow_input, 0, 0)
        follow_layout.setSpacing(0)
        follow_layout.addWidget(follow_button, 0, 1)
        follow_layout.setSpacing(0)
        follow_layout.addWidget(self.follow_error_widget, 1, 0, 1, 2)
        
        layout.addLayout(follow_layout)
        
        widget.setLayout(layout)
        
        return widget
    
    def on_post_text_changed(self, text):
        """
        Called when the post text changes
        """
        self.post_text = text
    
    def update_posts(self):
        """
        Update the posts widget
        """
        if self.stacked_posts != None:
            posts_widget = self.create_posts_widget()
            posts_widget.layout().setAlignment(Qt.AlignTop)
            self.stacked_posts.removeWidget(self.stacked_posts.currentWidget())
            self.stacked_posts.addWidget(posts_widget)
            self.stacked_posts.setCurrentWidget(posts_widget)
    
    def create_post(self):
        """
        Create a post
        """
        print('Create post:', self.post_text)
        self.parent.controller.post(self.post_text)
        self.update_posts()
        
    def logout(self):
        """
        Logout
        """
        self.parent.logout()