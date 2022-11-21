import sys
import asyncio
from kademlia.network import Server

from comms import sender
from comms import listener

'''
python main.py -register 'name' 'port'
python main.py -timeline 'name'

'''

# async def main():
#     #server = Server()
    
#     #boostrap_node = (sys.argv[1], int(sys.argv[2]))
#     #await server.bootstrap([boostrap_node])
#     if(len(sys.argv) == 4): # ip port msg
#         await sender.send_message(sys.argv[1], int(sys.argv[2]), sys.argv[3]), asyncio.get_event_loop()
#     else: #ip port
#         #await server.listen(int(sys.argv[2]))
#         server_listener = listener.Listener(sys.argv[1], int(sys.argv[2]))
#         server_listener.daemon = True

#         server_listener.start()

#         try:
#             while True:
#                 pass
#         except KeyboardInterrupt:
#             server_listener.stop()
        
#     #server.stop()
    
#     #node = Node(sys.argv[1], int(sys.argv[2]), sys.argv[3])

# if __name__ == "__main__":
#     asyncio.run(main())

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel
#from view.timeline_window import TimelineWindow
from view.start_window import StartWindow

                                                     

if __name__ == "__main__":

    app = QApplication(sys.argv)

    timeline_window = StartWindow()

    sys.exit(app.exec())