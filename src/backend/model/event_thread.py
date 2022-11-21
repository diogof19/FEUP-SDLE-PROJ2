from threading import Thread, Event

from utils.event_thread_utils import sync_time

class EventThread(Thread):
    def __init__(self, stop_event : Event, interval=1):
        super().__init__()
        self.stop_event = stop_event
        self.interval = interval

    def run(self):
        """
        Run the thread
        """
        while not self.stop_event.wait(self.interval):
            sync_time()