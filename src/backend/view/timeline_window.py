# from PySide6.QtWidgets import QApplication, QWidget, QPushButton
# from PySide6.QtCore import Slot

# from .consts import BACKGROUND_COLOR

# class TimelineWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.title = 'Singer'
#         self.left = 100
#         self.top = 100
#         self.width = 640
#         self.height = 480
#         self.setup()
        
#     def setup(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#         self.setStyleSheet(f'\
#             background-color: {BACKGROUND_COLOR};\
#             color: #FFFFFF;\
#         ')
        
#         button = QPushButton('PyQt5 button', self)
#         button.setToolTip('This s an example button')
#         button.setStyleSheet("\
#             background-color: #FFFFFF;\
#             color: #000000;\
#         ")
#         button.clicked.connect(self.on_click)
        
#         self.show()
        
#     @Slot()
#     def on_click(self):
#         print('PyQt5 button click')