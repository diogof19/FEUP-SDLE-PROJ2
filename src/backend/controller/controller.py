from utils.node_utils import run_in_loop
import signal

class Controller:
    def __init__(self, user):
        self.user = user
        self.stop = False

    def start(self):
        """
        Start the controller
        """        
        while not self.stop:
            try:
                cmd = input('Enter command: ')
            except KeyboardInterrupt:
                self.stop = True
                break

            if cmd == 'register':
                self.register()
            elif cmd == 'post':
                body = input('Enter message: ')
                self.post(body)
            elif cmd == 'follow':
                run_in_loop(self.user.follow(input("Enter username: ")), self.user.loop)
            elif cmd == 'unfollow':
                self.unfollow()
            elif cmd == 'timeline':
                self.timeline()
            elif cmd == 'exit':
                self.user.stop_ntp.set()
                break
            elif cmd == 'missing':
                self.get_missing()
            elif cmd == 'printKademlia':
                print(self.user.info)
            elif cmd == 'get_info':
                username = input('Enter username: ')
                print(run_in_loop(self.user.get_kademlia_info(username), self.user.loop).result())
            elif cmd == 'get_posts':
                username = input('Enter username: ')
                print(self.get_posts(username))
            elif cmd == 'set_own_info':
                run_in_loop(self.user.set_own_info(), self.user.loop)
            else:
                print('Invalid command')
    
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
        return self.user.database.get_posts_for_user(user)
    
    def unfollow(self, username):
        #TODO: Implement unfollow
        pass
    
    def follow(self, username):
        run_in_loop(self.user.follow(username), self.user.loop)

    def get_missing(self):
        print(run_in_loop(self.user.get_missing_posts(), self.user.loop).result())
    
    def get_followers(self):
        return self.user.get_followers()
    
    def get_following(self):
        return self.user.get_following()
    
    def get_username(self):
        return self.user.username