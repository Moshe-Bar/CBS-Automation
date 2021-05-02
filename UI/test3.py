import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, QGridLayout, QLabel, QPushButton, QGroupBox, QDialog, \
    QVBoxLayout, QProgressBar, QScrollArea, QWidget, QHBoxLayout


class CbsSiteTestWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'Site Test'
        self.logo_path = '../Images/3773~1.png'
        self.width = 1080
        self.height = 720
        self.left = 400
        self.top = 250
        # widgets
        self.scroll = QScrollArea()
        self.set_window()
        self.generate_base_widgets()
        self.show()

    def set_window(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.logo_path))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)

    def selection_section_setup(self):
        pass

    def generate_base_widgets(self):
        base_top_grid = QGridLayout()
        base_buttom_box = QHBoxLayout()

        base_top_grid.setRowStretch(0, 4)
        base_top_grid.setRowStretch(1, 4)
        base_top_grid.setColumnStretch(0, 4)
        base_top_grid.setColumnStretch(1, 4)
        self.setLayout(base_top_grid)


app = QApplication(sys.argv)
window = CbsSiteTestWindow()
# window = App()
sys.exit(app.exec_())
