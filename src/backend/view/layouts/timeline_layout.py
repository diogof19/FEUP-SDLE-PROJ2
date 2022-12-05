from PySide6.QtWidgets import QVBoxLayout, QFrame, QGridLayout, QHBoxLayout, QLabel, QGroupBox, QSizePolicy, QScrollArea, QLineEdit, QPushButton
from PySide6.QtCore import Slot, Qt, QSize
from PySide6 import QtWidgets

class TimelineLayout(QGridLayout):
    def __init__(self, parent, search_results=[]):
        super().__init__()
        self.parent = parent
        self.post_text = ""
        self.search_text = ""
        self.search_results = search_results
        
        super().setContentsMargins(0, 0, 0, 0)
        self.setup()
        
    def setup(self):
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
        
        # ------------------ Posts ------------------
        
        posts_layout = QVBoxLayout()
        
        posts = self.get_all_posts()
        for post in posts:
            card = self.create_post_card(post)
            posts_layout.addWidget(card)
            
        # ----------------- Info Area -----------------
        
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignTop)
        info_layout.setContentsMargins(10, 10, 10, 10)
        
        search_widget = self.create_search_widget()
        info_layout.setSpacing(0)
        info_layout.addWidget(search_widget)
        
        followers_widget = self.create_followers_widget()
        info_layout.setSpacing(0)
        info_layout.addWidget(followers_widget)
        
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
        post1 = {'username': 'User11111111111111111111', 'body':'Body text sdasdsdasdasdasdasdasdasdasdasdasdasdsdsdadasdasdasdasdasdsdadasdd', 'date': '2021-01-01'}
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
        return self.parent.controller.get_following()
    
    def get_all_followers(self):
        return self.parent.controller.get_followers()
    
    def on_search_text_changed(self, text):
        self.search_text = text
        print('search text changed:', text)
        
    def search(self):
        #DO SEARCH
        """ self.search_results = ['User7', 'User8']
        print('search results:', self.search_results)
        super().update() """
        self.parent.do_search(self.search_text)
        
    def unfollow(self, username):
        print('unfollow:', username)
        self.parent.controller.unfollow(username)
        self.parent.reload()
    
    def follow(self, username):
        print('follow:', username)
        self.parent.controller.follow(username)
        self.parent.reload()
    
    def create_search_widget(self):
        widget = QGroupBox()
        widget.setObjectName('followers_widget')
        widget.setMaximumSize(400, 400)
        widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        
        layout = QVBoxLayout()
        
        search = QLineEdit()
        search.setObjectName('input_post')
        search.setPlaceholderText('Search Users')
        search.setMaximumWidth(300)
        search.setAlignment(Qt.AlignLeft)
        search.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        search.textChanged.connect(self.on_search_text_changed)
        
        search_button = QPushButton('Search')
        search_button.setObjectName('create_post_button')
        search_button.clicked.connect(self.search)
        search_button.setMaximumWidth(100)
        search.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        
        search_layout = QHBoxLayout()
        
        search_layout.setSpacing(0)
        search_layout.addWidget(search)
        search_layout.setSpacing(0)
        search_layout.addWidget(search_button)

        layout.setSpacing(0)
        layout.addLayout(search_layout)
        
        results_layout = QVBoxLayout()
        following_list = self.get_all_following()
        for result in self.search_results:
            result_layout = QHBoxLayout()
            
            result_name = self.create_follow_widget(result)
            result_name.setAlignment(Qt.AlignVCenter)
            
            if(result in following_list):
                result_button = QPushButton('Unfollow')
                result_button.setObjectName('unfollow_button')
                result_button.clicked.connect(lambda: self.unfollow(result))
            else:
                result_button = QPushButton('Follow')
                result_button.setObjectName('follow_button')
                result_button.clicked.connect(lambda: self.follow(result))
            
            result_layout.setSpacing(0)
            result_layout.addWidget(result_name)
            result_layout.setSpacing(0)
            result_layout.addWidget(result_button)
            
            results_layout.setSpacing(0)
            results_layout.addLayout(result_layout)
            
        results_widget = QGroupBox()
        results_widget.setObjectName('followers_list')
        results_widget.setLayout(results_layout)
        
        results_scroll = QScrollArea()
        results_scroll.setWidgetResizable(True)
        results_scroll.setContentsMargins(0, 0, 0, 0)
        results_scroll.setViewportMargins(0, 0, 0, 0)
        results_scroll.setObjectName('followers_scroll')
        results_scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        results_scroll.setWidget(results_widget)
        
        layout.addWidget(results_scroll)
        widget.setLayout(layout)
        
        return widget
        
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
    
    def on_post_text_changed(self, text):
        self.post_text = text
    
    def create_post(self):
        print('Create post:', self.post_text)
        self.parent.controller.post(self.post_text)
        self.parent.reload()
        
    def logout(self):
        self.parent.setup()