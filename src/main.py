import sys
import os

from PySide6.QtWidgets import QApplication
from view.main_window import MainWindow

from model.user import User
from threading import Thread
from controller.controller import Controller

def main():
    '''
    python main.py <ip> <port> <bootstrap_config_file>
    '''
    # Create the peer and run in thread
    peer = User(sys.argv[1], int(sys.argv[2]), '', sys.argv[3])

    server_thread = Thread(target=peer.loop.run_forever, daemon=True)

    server_thread.start()


    # Create the controller and run in thread
    controller = Controller(peer)

    controller_thread = Thread(target=controller.start, daemon=True)

    controller_thread.start()


    # Start the GUI
    app = QApplication(sys.argv)

    timeline_window = MainWindow(controller)

    with open("view/layouts/style.qss", "r") as f:
        _style = f.read()
        timeline_window.setStyleSheet(_style)

    app.exec()

    # After the GUI is closed, stop the peer
    peer.server.stop()
    peer.listener.server.close()
    peer.loop.stop()
    
    os._exit(0)

if __name__ == "__main__":
    main()
