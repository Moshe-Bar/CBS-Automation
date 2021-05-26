import sys
import threading
import time
from multiprocessing import Queue
from ast import literal_eval
from PyQt5.QtCore import pyqtSignal
# from PyQt5.uic.properties import QtCore  after instalation PyQt5-stubs==5.15.2.0
from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import Qt, QVariant, QThread, QObject, QRunnable, pyqtSlot, QThreadPool
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem, QFont, QTextListFormat
from PyQt6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QApplication, QMainWindow, QStackedWidget, QLabel, \
    QLineEdit, QScrollArea, QWidget, QCheckBox, QListView, QListWidgetItem, QAbstractItemView, QTextBrowser
from PyQt6.uic import loadUi
# from PyQt6.uic.properties import QtGui, QtWidgets

from Testing.TestUtility import TestUtility

font_but = QFont()
font_but.setFamily("David")
font_but.setPointSize(10)
font_but.setWeight(95)




class LogInScreen(QDialog):
    def __init__(self):
        super(LogInScreen, self).__init__()
        loadUi('Qt_ui/login.ui', self)

        self.login_button.clicked.connect(self.login_clicked)
        # self.setStyleSheet("background-image: url('../dataBase/Images/LOGO_LAMAS.jpg');  background-repeat:
        # no-repeat;background-size: auto;")

    def login_clicked(self):
        # TODO verification using the data base
        screen_manager.setCurrentIndex((screen_manager.currentIndex() + 1))


class TestPropertiesScreen(QDialog):
    def __init__(self):
        super(TestPropertiesScreen, self).__init__()
        loadUi('Qt_ui/TestProperties.ui', self)
        self.pushButton.clicked.connect(self.goto_test_progress)
        self.list = QListView()

        pages = TestUtility.get_pages()
        # model = QStandardItemModel()

        self.h_pages_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        for i, page in enumerate(pages):
            it = QListWidgetItem(page.name)
            self.h_pages_list.addItem(it)
            it.setSelected(True)

    def goto_test_progress(self):
        screen_manager.setCurrentIndex((screen_manager.currentIndex() + 1))


class TestProgressScreen(QDialog):

    def __init__(self):
        super(TestProgressScreen, self).__init__()
        loadUi('Qt_ui/TestProgress.ui', self)
        # self.progress_signal = pyqtSignal(str)


        self.test_button = QPushButton('test')
        self.start_button.clicked.connect(self.start_click)
        self.cancel_button.clicked.connect(self.cancel_click)
        self.cancel_button.setEnabled(False)



        self.signals = WorkerSignals()
        self.signals.status.connect(self.update_progress_bar)
        self.signals.page_info.connect(self.convert_to_hyper_text)
        self.signals.finished.connect(self.close_test)
        self.signals.error.connect(self.update_terminal)
        self.signals.monitor_data.connect(self.update_terminal)

        self.thread_pool = QThreadPool()
        # self.test = QTextBrowser()
        # self.test.setOpenLinks(True)
        # self.textMonitor.setReadOnly(False)
        self.textMonitor.setOpenExternalLinks(True)
        self.textMonitor.setOpenLinks(True)

    def update_terminal(self, data):
        data = '<p>{}</p>'.format(data)
        self.textMonitor.append(data)

    def convert_to_hyper_text(self,data):
        dict_data = literal_eval(data)
        error = 'style="color:#FF0000;"'
        if dict_data['error']:
            info ='<a href="{}" {} >{}</a>'.format(dict_data['url'],error,dict_data['name'])
        else:
            info = '<a href="{}" >{}</a>'.format(dict_data['url'],dict_data['name'])
        self.textMonitor.append(info)

    def update_progress_bar(self, value):
        self.progressBar.setValue(value)

    def cancel_click(self):
        self.signals.end_flag.put(True)
        self.close_test()

    def close_test(self):
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.update_terminal('Test Finished')

    def start_click(self):
        if not self.signals.end_flag.empty():
            self.signals.end_flag.get()
        self.test_runner = Excecutor(TestUtility.test_with_pyqt_slots, self.signals)
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.update_terminal('test started')
        self.thread_pool.start(self.test_runner)

class WorkerSignals(QObject):
    page_info = QtCore.pyqtSignal(str)
    status = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(tuple)
    result = QtCore.pyqtSignal(object)
    monitor_data = QtCore.pyqtSignal(str)
    end_flag = Queue()

class Excecutor(QRunnable):

    def __init__(self, function, *args, **kwargs):
        super(Excecutor, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.autoDelete()
        # self.signals = self.WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            self.function(*self.args,pages=None)
        except Exception as e:
            print('Exception was raised during test, '+str(e))

            return

class ResultsScreen(QDialog):
    pass

class CBSTestApplication(QApplication):
    def __init__(self, arguments):
        super(CBSTestApplication, self).__init__(arguments)

if __name__ == "__main__":
    app = CBSTestApplication(sys.argv)
    screen_manager = QStackedWidget()
    screen_manager.setWindowIcon(QIcon('../dataBase/Images/1200px-LOGO_LAMAS.jpg'))

    login = LogInScreen()
    choose = TestPropertiesScreen()
    test_progress = TestProgressScreen()
    result = ResultsScreen()

    screen_manager.addWidget(login)
    screen_manager.addWidget(choose)
    screen_manager.addWidget(test_progress)
    screen_manager.addWidget(result)

    # screen_manager.setFixedWidth(1080)
    # screen_manager.setFixedHeight(720)
    # screen_manager.setCurrentIndex((screen_manager.currentIndex() + 1))
    screen_manager.show()

    sys.exit(app.exec())
