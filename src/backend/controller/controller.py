from utils.node_utils import run_in_loop
import signal

class Controller:
    def __init__(self, user):
        self.user = user

    def start(self):
        """
        Start the controller
        """
        try:     
            while True:
                cmd = input('Enter command: ')

                if cmd == 'register':
                    self.register()
                elif cmd == 'post':
                    body = input('Enter message: ')
                    self.post(body)
                elif cmd == 'follow':
                    print(self.follow(input("Enter username: ")))
                elif cmd == 'unfollow':
                    self.unfollow(input("Enter username: "))
                elif cmd == 'timeline':
                    self.timeline()
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
                else:
                    print('Invalid command')
        except KeyboardInterrupt:
            print('Exiting...')
            self.user.stop()
        
    
    def post(self, body):
        print(run_in_loop(self.user.post(body), self.user.loop).result())
    
    def register(self):
        print(run_in_loop(self.user.register(), self.user.loop).result())
        self.user.start_listening()
        
    def login(self):
        print(run_in_loop(self.user.login(), self.user.loop).result())
        self.user.start_listening()
    
    def timeline(self):
        #TODO: Implement timeline
        pass
    
    def get_posts(self, user):
        posts = self.user.database.get_posts()
        return posts
    
    def unfollow(self, username):
        try:
            run_in_loop(self.user.unfollow(username), self.user.loop).result()
            return True
        except Exception as e:
            return False
    
    def follow(self, username):
        try:
            return run_in_loop(self.user.follow(username), self.user.loop).result()
        except Exception as e:
            if(str(e) == 'This event loop is already running'):
                return True
            else:
                return False
        
    def get_followers(self):
        return self.user.get_followers()
    
    def get_following(self):
        return self.user.get_following()
    
    def get_username(self):
        return self.user.username
        
    def get_missing(self):
        print(run_in_loop(self.user.get_missing_posts(), self.user.loop).result())
