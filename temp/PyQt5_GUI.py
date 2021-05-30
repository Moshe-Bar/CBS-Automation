import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, QGridLayout, QLabel, QPushButton, QGroupBox, QDialog, \
    QVBoxLayout, QProgressBar, QScrollArea, QWidget, QHBoxLayout


# class CbsSiteTestWindow(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.title = 'Site Test'
#         self.logo_path = '../dataBase/Images/1200px-LOGO_LAMAS.jpg'
#         self.width = 1080
#         self.height = 720
#         self.left = 400
#         self.top = 250
#         # widgets
#         self.scroll = QScrollArea()
#         self.set_window()
#         self.generate_base_widgets()
#         self.show()
#
#     def set_window(self):
#         self.setWindowTitle(self.title)
#         self.setWindowIcon(QIcon(self.logo_path))
#         self.setGeometry(self.left, self.top, self.width, self.height)
#         self.setFixedWidth(self.width)
#         self.setFixedHeight(self.height)
#
#     def selection_section_setup(self):
#         pass
#
#     def generate_base_widgets(self):
#         base_top_grid = QGridLayout()
#         base_buttom_box = QHBoxLayout()
#
#         base_top_grid.setRowStretch(0, 4)
#         base_top_grid.setRowStretch(1, 4)
#         base_top_grid.setColumnStretch(0, 4)
#         base_top_grid.setColumnStretch(1, 4)
#         self.setLayout(base_top_grid)

import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QProgressBar, QVBoxLayout, QApplication

class Thread(QThread):
    _signal = pyqtSignal(int)
    def __init__(self):
        super(Thread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self._signal.emit(i)

class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.setWindowTitle('QProgressBar')
        self.btn = QPushButton('Click me')
        self.btn.clicked.connect(self.btnFunc)
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.resize(300, 100)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.pbar)
        self.vbox.addWidget(self.btn)
        self.setLayout(self.vbox)
        self.show()

    def btnFunc(self):
        self.thread = Thread()
        self.thread._signal.connect(self.signal_accept)
        self.thread.start()
        self.btn.setEnabled(False)

    def signal_accept(self, msg):
        self.pbar.setValue(int(msg))
        if self.pbar.value() == 99:
            self.pbar.setValue(0)
            self.btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

# app = QApplication(sys.argv)
# window = CbsSiteTestWindow()
# # window = App()
# sys.exit(app.exec_())
