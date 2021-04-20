import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, QGridLayout, QLabel, QPushButton, QGroupBox, QDialog, \
    QVBoxLayout, QProgressBar, QScrollArea, QWidget

widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": []
}


# class CbsSiteTestWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         # self.setFixedSize(QSize(800, 400))
#         # self.setGeometry(10, 10, 320, 100)
#         # self.setWindowTitle('SiteTest')
#         # self.setWindowIcon(QIcon('OPZOXK0.jpg'))
#         # self.horizontalGroupBox = QGroupBox("Grid")
#         # self.create_grid()
#         # self.show()
#         self.left = 10
#         self.top = 10
#         self.width = 320
#         self.height = 100
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('test1')
#         self.setGeometry(self.left, self.top, self.width, self.height)
#
#         self.createGridLayout()
#
#         windowLayout = QVBoxLayout()
#         windowLayout.addWidget(self.horizontalGroupBox)
#         self.setLayout(windowLayout)
#
#         self.show()
#
#     def createGridLayout(self):
#         # layout = QGridLayout()
#         # layout.setColumnStretch(1, 4)
#         # layout.setColumnStretch(2, 4)
#         # layout.setColumnStretch(3, 4)
#         #
#         # layout.addWidget(QPushButton('1'), 0, 0)
#         # layout.addWidget(QPushButton('2'), 0, 1)
#         # layout.addWidget(QPushButton('3'), 0, 2)
#         # layout.addWidget(QPushButton('4'), 1, 0)
#         # layout.addWidget(QPushButton('5'), 1, 1)
#         # layout.addWidget(QPushButton('6'), 1, 2)
#         # layout.addWidget(QPushButton('7'), 2, 0)
#         # layout.addWidget(QPushButton('8'), 2, 1)
#         # layout.addWidget(QPushButton('9'), 2, 2)
#         #
#         # self.horizontalGroupBox.setLayout(layout)
#         self.horizontalGroupBox = QGroupBox("Grid")
#         layout = QGridLayout()
#         layout.setColumnStretch(1, 4)
#         layout.setColumnStretch(2, 4)
#
#         layout.addWidget(QPushButton('1'), 0, 0)
#         layout.addWidget(QPushButton('2'), 0, 1)
#         layout.addWidget(QPushButton('3'), 0, 2)
#         layout.addWidget(QPushButton('4'), 1, 0)
#         layout.addWidget(QPushButton('5'), 1, 1)
#         layout.addWidget(QPushButton('6'), 1, 2)
#         layout.addWidget(QPushButton('7'), 2, 0)
#         layout.addWidget(QPushButton('8'), 2, 1)
#         layout.addWidget(QPushButton('9'), 2, 2)
#
#         self.horizontalGroupBox.setLayout(layout)
#
#     def create_input_tab(self):
#         pass
#
#     def create_log_tab(self):
#         pass


class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'Site test'
        self.left = 400
        self.top = 250
        self.width = 1080
        self.height = 720
        self.logo_path = '3773~1.png'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.logo_path))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.createGridLayout()


        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.baseHorizontalGroupBox)
        windowLayout.addWidget(self.buttomHorizontalGroupBox)
        self.setLayout(windowLayout)
        self.set_right_up_grid()
        # self.set_background_img()

        self.show()

    def createGridLayout(self):
        self.baseHorizontalGroupBox = QGroupBox("BaseGrid")
        self.set_background_img()

        layout = QGridLayout()
        layout.setColumnStretch(0, 4)
        layout.setColumnStretch(1, 4)
        layout.setRowStretch(0, 3)
        layout.setRowStretch(1, 3)

        layout.addWidget(QGroupBox("LeftUP"), 0, 0)
        layout.addWidget(QGroupBox("RightUp"), 0, 1)
        layout.addWidget(QGroupBox("LeftDown"), 1, 0)
        layout.addWidget(QGroupBox("RightDown"), 1, 1)
        # layout.addWidget(QPushButton('6'), 1, 2)
        # layout.addWidget(QPushButton('7'), 2, 0)
        # layout.addWidget(QPushButton('8'), 2, 1)
        # layout.addWidget(QPushButton('9'), 2, 2)
        self.buttomHorizontalGroupBox = QGroupBox("ButtomGrid")
        b_layout = QGridLayout()
        # b_layout.setRowStretch(0, 1)
        self.baseHorizontalGroupBox.setLayout(layout)
        self.baseHorizontalGroupBox.setAlignment(4)
        self.buttomHorizontalGroupBox.setLayout(b_layout)
        self.buttomHorizontalGroupBox.setAlignment(4)
        self.progress = QProgressBar(self)
        self.progress.setValue(25)
        b_layout.addWidget(self.progress)

    def update_progress_bar(self, value):
        pass

    def set_right_up_grid(self):
        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        for i in range(1, 50):
            obj = QLabel("TextLabel")
            self.vbox.addWidget(obj)

        self.widget.setLayout(self.vbox)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        # self.setCentralWidget(self.scroll)

        # self.setGeometry(600, 100, 1000, 900)
        # self.setWindowTitle('Scroll Area Demonstration')
        # self.show()

    def set_background_img(self):
        oImage = QImage("2396.jpg")
        sImage = oImage.scaled(QSize(1080, 720))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.baseHorizontalGroupBox.setPalette(palette)

app = QApplication(sys.argv)
# window = CbsSiteTestWindow()
window = App()
sys.exit(app.exec_())
