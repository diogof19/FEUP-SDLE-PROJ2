import sys
import os

from PySide6.QtWidgets import QApplication
from view.main_window import MainWindow

from model.user import User
from threading import Thread
from controller.controller import Controller

'''
python main.py -register 'name' 'port'
python main.py -timeline 'name'

'''

def main():
    peer = User(sys.argv[1], int(sys.argv[2]), '', sys.argv[3])

    server_thread = Thread(target=peer.loop.run_forever, daemon=True)

    server_thread.exit = False

    server_thread.start()

    controller = Controller(peer)

    controller_thread = Thread(target=controller.start, daemon=True)

    controller_thread.start()
    
    app = QApplication(sys.argv)

    timeline_window = MainWindow(controller)

    peer.listener.set_view(timeline_window)

    with open("view/layouts/style.qss", "r") as f:
        _style = f.read()
        timeline_window.setStyleSheet(_style)

    app.exec()
    
    os._exit(0)

if __name__ == "__main__":
    main()
