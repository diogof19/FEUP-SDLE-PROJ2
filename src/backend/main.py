import sys
import asyncio
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

def main():
    peer = User(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])

    Thread(target=peer.loop.run_forever).start()

    controller = Controller(peer)
    controller.start()

if __name__ == "__main__":
    main()


""" import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from view.main_window import MainWindow

                                                     

if __name__ == "__main__":

    app = QApplication(sys.argv)

    timeline_window = MainWindow()

    with open("view/layouts/style.qss", "r") as f:
        _style = f.read()
        timeline_window.setStyleSheet(_style)

    sys.exit(app.exec()) """