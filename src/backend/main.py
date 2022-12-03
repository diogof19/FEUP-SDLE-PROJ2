import sys
import asyncio
import signal

from kademlia.network import Server
from model.user import User
from threading import Thread
from comms import sender
from comms import listener
from controller.controller import Controller

'''
python main.py -register 'name' 'port'
python main.py -timeline 'name'

'''
thread = None
controller = None

def main():
    peer = User(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])

    thread = Thread(target=peer.loop.run_forever, daemon=True)

    thread.start()

    controller = Controller(peer)

    def signal_handler():
        try:
            peer.stop_ntp.set()
        except:
            pass

    signal.signal(signal.SIGINT, lambda s, f: signal_handler())

    try:
        controller.start()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()


""" import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from view.main_window import MainWindow

                                                     

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # timeline_window = MainWindow()

    # with open("view/layouts/style.qss", "r") as f:
    #     _style = f.read()
    #     timeline_window.setStyleSheet(_style)

    sys.exit(app.exec()) """