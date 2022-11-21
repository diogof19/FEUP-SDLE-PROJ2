from threading import Thread

class EventThread(Thread):
    def __init__(self, stop_event, interval=1):
        super().__init__()
        self.stop_event = stop_event
        self.interval = interval

    def run(self):
        """
        Run the thread
        """
        while not self.stop_event.wait(self.interval):
            # Do something
            pass