from utils.node_utils import run_in_loop

class Controller:
    """
    Controller class for MVC

    This class s used to control the user
    Since we are using Qt this class is not strictly necessary
    As Qt is meant to be used with a Model/ViewController architecture
    However we kept it for the command line interface and Qt still uses it
    to ensure consistency
    """
    def __init__(self, user):
        self.user = user

    def start(self):
        """
        Start the controller
        This function is run in a separate thread
        and is only used for the command line interface
        """
        try:     
            while True:
                cmd = input('Enter command: ')
                if cmd == 'register':
                    self.user.username = input('Enter username: ')
                    self.register()
                elif cmd == 'post':
                    body = input('Enter message: ')
                    self.post(body)
                elif cmd == 'follow':
                    print(self.follow(input("Enter username: ")))
                elif cmd == 'unfollow':
                    self.unfollow(input("Enter username: "))
                elif cmd == 'exit':
                    self.user.stop_ntp.set()
                    break
                elif cmd == 'printKademlia':
                    print(self.user.info)
                elif cmd == 'get_info':
                    username = input('Enter username: ')
                    print(run_in_loop(self.user.get_kademlia_info(username), self.user.loop).result())
                elif cmd == 'missing':
                    self.get_missing()
                elif cmd == 'set_own_info':
                    run_in_loop(self.user.set_own_info(), self.user.loop)
                elif cmd == 'ping':
                    username = input('Enter username: ')
                    print(run_in_loop(self.user.ping(username), self.user.loop).result())  
                else:
                    print('Invalid command')
        except KeyboardInterrupt:
            print('Exiting...')
            self.user.stop()

    def post(self, body):
        """
        Handles making a post
        """
        result = run_in_loop(self.user.post(body), self.user.loop).result()
        print(result)
        return result
    
    def register(self):
        """
        Handles registering a user
        """
        print(run_in_loop(self.user.register(), self.user.loop).result())
        
    def login(self):
        """
        Handles logging in a user
        """
        print(run_in_loop(self.user.login(), self.user.loop).result())

    def logout(self):
        """
        Handles logging out a user
        """
        print(run_in_loop(self.user.logout(), self.user.loop).result())
    
    def get_posts(self, user):
        """
        Gets the posts of a user
        """
        posts = self.user.database.get_posts()
        return posts
    
    def unfollow(self, username):
        """
        Handles unfollowing a user
        """
        result = run_in_loop(self.user.unfollow(username), self.user.loop).result()
        print(result)
        return result
    
    def follow(self, username):
        """
        Handles following a user
        """
        result = run_in_loop(self.user.follow(username), self.user.loop).result()
        print(result)
        return result
        
    def get_followers(self):
        """
        Handles getting the followers of a user
        """
        return self.user.get_followers()
    
    def get_following(self):
        """
        Handles getting the users a user is following
        """
        return self.user.get_following()
    
    def get_username(self):
        """
        Handles getting the username of a user
        """
        return self.user.username
        
    def get_missing(self):
        """
        Handles getting the missing posts of a user
        """
        print(run_in_loop(self.user.get_missing_posts(), self.user.loop).result())
