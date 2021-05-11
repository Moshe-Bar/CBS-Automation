import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QApplication, QMainWindow, QStackedWidget, QLabel, QLineEdit, QScrollArea, QWidget
from PyQt5.uic import loadUi


class LogInScreen(QDialog):
    def __init__(self):
        super(LogInScreen, self).__init__()
        loadUi('Qt_ui/login.ui', self)

        self.login_button.clicked.connect(self.login_clicked)
        # self.setStyleSheet("background-image: url('../dataBase/Images/LOGO_LAMAS.jpg');  background-repeat: no-repeat;background-size: auto;")
        # self.layout = QVBoxLayout()
        #
        # self.create_widgets()
        # self.layout.addWidget(self.login_button)
        # self.layout.addWidget(self.line)
        # self.layout.addWidget(self.nameLabel)

    def login_clicked(self):
        screen_manager.setCurrentIndex((screen_manager.currentIndex() + 1))

    # self.setLayout(self.layout)
    # self.show()

    # def create_widgets(self):
    #     # configure 'login' button
    #     self.login_button = QPushButton('Login')
    #     self.login_button.setFixedWidth(int(self.size().width() * 0.5))
    #     self.login_button.setGeometry(500, 150, 50, 40)
    #     self.login_button.clicked.connect(self.login_pressed)
    #
    #     self.nameLabel = QLabel(self)
    #     self.nameLabel.setText('UserName:')
    #     self.line = QLineEdit(self)
    #     self.line.move(80, 20)
    #     self.line.resize(200, 32)
    #     self.nameLabel.move(20, 20)

    def login_pressed(self):
        pass

class TestPropertiesScreen(QDialog):
    def __init__(self):
        super(TestPropertiesScreen, self).__init__()
        loadUi('Qt_ui/TestProperties.ui', self)
        self.
    #     self.right_scroll =  QScrollArea()
    #     self.left_scroll =  QScrollArea()
    #     self.init_temp_list()
    #
    # def init_temp_list(self):
    #     self.left_widget = QWidget()
    #     self.right_widget = QWidget()
    #     self.left_vbox = QVBoxLayout()
    #     self.right_vbox = QVBoxLayout()
    #
    #     for i in range(1, 100):
    #         object = QLabel("TextLabel")
    #         self.left_vbox.addWidget(object)
    #         self.right_vbox.addWidget(object)
    #     self.left_widget.setLayout(self.left_vbox)
    #     self.right_widget.setLayout(self.right_vbox)
    #
    #     self.right_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    #     self.left_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    #     self.right_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    #     self.left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    #
    #     self.right_scroll.setWidgetResizable(True)
    #     self.left_scroll.setWidgetResizable(True)
    #     self.right_scroll.setWidget(self.right_widget)
    #     self.left_scroll.setWidget(self.left_widget)
    #
    #     self.setLayout(self.right_vbox)


        # self.setGeometry(600, 100, 500, 200)
        # self.setWindowTitle('Scroll Area Demonstration')
        self.show()

class TestProgressScreen(QMainWindow):
    pass

class ResultsScreen(QDialog):
    pass

class CBSTestApplication(QApplication):
    def __init__(self, arguments):
        super(CBSTestApplication, self).__init__(arguments)
        # self.resize(1080, 720)




if __name__ == "__main__":
    app = CBSTestApplication(sys.argv)
    screen_manager = QStackedWidget()
    screen_manager.setWindowIcon(QIcon('../dataBase/Images/1200px-LOGO_LAMAS.jpg'))

    login = LogInScreen()
    choose = TestPropertiesScreen()
    test_prog = TestProgressScreen()
    result = ResultsScreen()

    screen_manager.addWidget(login)
    screen_manager.addWidget(choose)
    screen_manager.addWidget(test_prog)
    screen_manager.addWidget(result)
    screen_manager.setFixedWidth(1080)
    screen_manager.setFixedHeight(720)
    # screen_manager.setCurrentIndex((screen_manager.currentIndex() + 1))
    screen_manager.show()

    sys.exit(app.exec_())