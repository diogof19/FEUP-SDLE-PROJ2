from utils.node_utils import run_in_loop

class Controller:
    def __init__(self, user):
        self.user = user

    def start(self):
        """
        Start the controller
        """        
        self.user.start_listening() 
        while True:
            cmd = input('Enter command: ')

            if cmd == 'register':
                print(run_in_loop(self.user.register(), self.user.loop).result())
            elif cmd == 'post':
                self.post()
            elif cmd == 'follow':
                run_in_loop(self.user.follow(input("Enter username: ")), self.user.loop)
            elif cmd == 'unfollow':
                self.unfollow()
            elif cmd == 'timeline':
                self.timeline()
            elif cmd == 'exit':
                exit()
            else:
                print('Invalid command')
