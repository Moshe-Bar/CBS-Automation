import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QStackedWidget, QDialog
from PyQt6.uic import loadUi

# from UI.Qt_GUI import LogInScreen, TestPropertiesScreen


class LogInScreen(QDialog):
    def __init__(self):
        super(LogInScreen, self).__init__()
        loadUi('Qt_ui/WrapWindow.ui', self)
        # self.login_button.clicked.connect(self.login_clicked)

    def login_clicked(self):
        # TODO verification using the data base

        self.login_label.setText('ready')
        self.login_label.setStyleSheet("QLabel#login_label {color: black}")

        print(self.user_n_input.text())
        print(self.pass_input.text())
        if self.user_n_input.text()=='TEST' and self.pass_input.text()=='TEST':
            # screen_manager.setFixedWidth(820)
            # screen_manager.setFixedHeight(660)
            # screen_manager.setCurrentIndex((screen_manager.currentIndex() + 1))
            pass
        else:
            self.login_label.setText('wrong details')
            self.login_label.setStyleSheet("QLabel#login_label {color: red}")


class CBSTestApplication(QApplication):
    def __init__(self, arguments):
        super(CBSTestApplication, self).__init__(arguments)
        self.screen_manager = QStackedWidget()
        self.screen_manager.addWidget(LogInScreen())
        self.screen_manager.setFixedHeight(650)
        self.screen_manager.setFixedWidth(820)
        self.screen_manager.show()


class ScreenManager(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.login = LogInScreen()
        # self.choose = TestPropertiesScreen()
        self.addWidget(self.login)
        # self.addWidget(self.choose)




if __name__ == "__main__":
    app = CBSTestApplication(sys.argv)
    # screen_manager = QStackedWidget()
    # screen_manager.setWindowIcon(QIcon('../DataBase/Images/1200px-LOGO_LAMAS.jpg'))
    sys.exit(app.exec())
