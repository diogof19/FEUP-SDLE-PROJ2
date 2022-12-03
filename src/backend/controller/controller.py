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
                print(run_in_loop(self.user.register(), self.user.loop).result())
                self.user.start_listening() 
            elif cmd == 'post':
                body = input('Enter message: ')
                print(run_in_loop(self.user.post(body), self.user.loop).result())
            elif cmd == 'follow':
                run_in_loop(self.user.follow(input("Enter username: ")), self.user.loop)
            elif cmd == 'unfollow':
                self.unfollow()
            elif cmd == 'timeline':
                self.timeline()
            elif cmd == 'exit':
                self.user.stop_ntp.set()
                break
            else:
                print('Invalid command')
