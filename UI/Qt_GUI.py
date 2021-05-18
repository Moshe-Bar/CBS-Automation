import sys
import threading
import time
from multiprocessing import Queue

from PyQt5.QtCore import pyqtSignal
from PyQt5.uic.properties import QtCore
from PyQt6.QtCore import Qt, QVariant, QThread
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QApplication, QMainWindow, QStackedWidget, QLabel, \
    QLineEdit, QScrollArea, QWidget, QCheckBox, QListView
from PyQt6.uic import loadUi

from Testing.TestUtility import TestUtility


class ThreadTry(QtCore.QThread):

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.sig1 = pyqtSignal(str)
        self.running = True
        self.source_txt = None

    def on_source(self, lineftxt):
        self.source_txt = lineftxt

    def run(self):
        while self.running:
            self.sig1.emit(self.source_txt)
            time.sleep(1)


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

        pages = TestUtility.get_pages()
        model = QStandardItemModel()
        for i, page in enumerate(pages):
            item = QStandardItem(page.name)
            # item.setFlags(Qt.ItemSelectionMode | Qt.ItemSelectionOperation)
            # item.setData(QVariant(Qt.Checked), Qt.CheckStateRole)
            model.appendRow(item)
            # item = QStandardItem(page.name)
            # item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            # item.setData(QVariant(Qt.Checked), Qt.CheckStateRole)
            # model.appendRow(item)

        self.listView.setModel(model)
        self.listView.show()

    def goto_test_progress(self):
        screen_manager.setCurrentIndex((screen_manager.currentIndex() + 1))


class TestProgressScreen(QDialog):
    def __init__(self):
        super(TestProgressScreen, self).__init__()
        loadUi('Qt_ui/TestProgress.ui', self)
        self.textMonitor.append('hhhhhhh')
        self.progress_signal = pyqtSignal(str)
        # print(self.insideWidget.children())

        self.start_button.clicked.connect(self.start_click)
        self.cancel_button.clicked.connect(self.cancel_click)

    def start_click(self):
        self.pushButton.setEnabled(False)
        self.shared_data = Queue()
        self.progress = Queue()
        self.ev = threading.Event()
        pages = TestUtility.get_pages()
        self.start_btn.disabled = True
        print('start button clicked')
        self.print_terminal('start clicked')
        data = Queue()
        # self.end_flag = Queue()

        self.working_event.set()
        threading.Thread(target=self.main_thread,
                         args=(self.shared_data, self.progress, self.working_event, pages)).start()
        threading.Thread(target=self.second_thread, args=(self.shared_data, self.working_event)).start()

    def cancel_click(self):
        pass
        # self.working_event.clear()

    def second_thread(self, shared_data: Queue, ev: threading.Event()):
        print('second thread enter')
        while ev.isSet():
            if self.progress.qsize() > 0:
                self.pb.value = self.progress.get() * 1000
                # self.new_progress.set_value(self.progress.get()*100)
            if shared_data.qsize() > 0:
                self.print_terminal(shared_data.get())
        print('second thread exit')
        # temp = end_process.get()
        # shared_data.put(temp)
        # end_process.put(temp)
        shared_data.put('exiting second process')

    def main_thread(self, shared_data: Queue, progress: Queue, ev: threading.Event(), pages=None):
        try:
            print('start test')
            TestUtility.test_with_events(working=ev, shared_data=shared_data, progress_status=progress, pages=pages)
            print('after test')
        except Exception:
            print(Exception)
            # end_flag.put('end for exception')
            if ev.isSet():
                ev.clear()
            if shared_data.qsize() > 0:
                data = shared_data.get()
                self.print_terminal(data)
                print(data)
            else:
                print('shared data is empty')
        finally:
            self.start_btn.disabled = False

    def start_button_click(self, instance, value):
        self.start_btn.disabled = True
        print('start button clicked')
        self.print_terminal('start clicked')
        data = Queue()
        # self.end_flag = Queue()

        self.working_event.set()
        threading.Thread(target=self.main_thread, args=(data, self.progress, self.working_event)).start()
        threading.Thread(target=self.second_thread, args=(data, self.working_event)).start()


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()


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

    sys.exit(app.exec())
