import sys
import os
import time

from multiprocessing import Queue
from ast import literal_eval

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QObject, QRunnable, pyqtSlot, QThreadPool, QCoreApplication
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QDialog, QPushButton, QApplication, QStackedWidget, QListView, QListWidgetItem, \
    QAbstractItemView
from PyQt6.uic import loadUi

from Utility.Util import Util



class LogInScreen(QDialog):
    def __init__(self):
        super(LogInScreen, self).__init__()
        loadUi('gui_windows/login.ui', self)

        self.login_button.clicked.connect(self.login_clicked)

    def login_clicked(self):
        # TODO verification using the data base

        self.login_label.setText('ready')
        self.login_label.setStyleSheet("QLabel#login_label {color: black}")

        print(self.user_n_input.text())
        print(self.pass_input.text())
        if self.user_n_input.text() == 'TEST' and self.pass_input.text() == 'TEST':
            screen_manager.setFixedWidth(820)
            screen_manager.setFixedHeight(660)
            screen_manager.setCurrentIndex((screen_manager.currentIndex() + 1))
        else:
            self.login_label.setText('wrong details')
            self.login_label.setStyleSheet("QLabel#login_label {color: red}")


class TestPropertiesScreen(QDialog):
    def __init__(self):
        super(TestPropertiesScreen, self).__init__()
        loadUi('Qt_ui/TestProperties.ui', self)
        self.pushButton.clicked.connect(self.goto_test_progress)
        self.list = QListView()

        self.h_pages = Util.get_pages(lang='he')
        self.e_pages = Util.get_pages(lang='en')
        # model = QStandardItemModel()
        # se =QListWidget()
        # se.setFont(QFont("Times", 5))
        # se.sizeHint()
        self.h_pages_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.h_pages_list.setFont(QFont("Sans-Serif", 15))
        self.h_pages_list.setStyleSheet("#h_pages_list::Item{\n"
                                        "height:20px;}\n"
                                        "#h_pages_list::Item:hover{\n"
                                        "background-color: rgb(41, 189, 139);\n"
                                        "}")
        for i, page in enumerate(self.h_pages):
            it = QListWidgetItem(page.name)
            it.setToolTip(page.name)
            self.h_pages_list.addItem(it)
            it.setSelected(True)

        self.e_pages_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.e_pages_list.setFont(QFont("Sans-Serif", 15))
        self.e_pages_list.setStyleSheet("#e_pages_list::Item{\n"
                                        "height:20px;}\n"
                                        "#e_pages_list::Item:hover{\n"
                                        "background-color: rgb(41, 189, 139);\n"
                                        "}")
        for i, page in enumerate(self.e_pages):
            it = QListWidgetItem(page.name)
            it.setToolTip(page.name)
            self.e_pages_list.addItem(it)
            it.setSelected(True)

        # se = QCheckBox()

        self.check_all_hpages.setCheckState(Qt.CheckState.Checked)
        self.check_all_hpages.stateChanged.connect(self.select_all_hpages)
        self.check_all_epages.setCheckState(Qt.CheckState.Checked)
        self.check_all_epages.stateChanged.connect(self.select_all_epages)

        # INITIALIZE CHECKED PAGES
        self.checked_hpages = []
        for i in range(self.h_pages_list.count()):
            self.checked_hpages.append(True)
        self.checked_epages = []
        for i in range(self.e_pages_list.count()):
            self.checked_epages.append(True)

    def select_all_hpages(self, state):
        if state == Qt.CheckState.Checked.value:
            # save the old chosen pages before selecting all
            for i in range(self.h_pages_list.count()):
                self.checked_hpages.append(self.h_pages_list.item(i).isSelected())
            # selct all
            for i in range(self.h_pages_list.count()):
                self.h_pages_list.item(i).setSelected(True)

        elif state == Qt.CheckState.Unchecked.value:
            for i in range(self.h_pages_list.count()):
                self.h_pages_list.item(i).setSelected(self.checked_hpages[i])

    def select_all_epages(self, state):
        if state == Qt.CheckState.Checked.value:
            # save the old chosen pages before selecting all
            for i in range(self.e_pages_list.count()):
                self.checked_epages.append(self.e_pages_list.item(i).isSelected())
            # select all
            for i in range(self.e_pages_list.count()):
                self.e_pages_list.item(i).setSelected(True)

        elif state == Qt.CheckState.Unchecked.value:
            for i in range(self.e_pages_list.count()):
                self.e_pages_list.item(i).setSelected(self.checked_epages[i])

    def goto_test_progress(self):
        self.chosen_pages = []
        for i in range(self.h_pages_list.count()):
            if self.h_pages_list.item(i).isSelected():
                self.chosen_pages.append(self.h_pages[i])
        screen_manager.addWidget(TestProgressScreen(chosen_pages=self.chosen_pages))
        # screen_manager.setFixedWidth(630)
        # screen_manager.setFixedHeight(550)
        screen_manager.setCurrentIndex((screen_manager.currentIndex() + 1))


class TestProgressScreen(QDialog):

    def __init__(self, chosen_pages):
        super(TestProgressScreen, self).__init__()
        loadUi('gui_windows/TestProgress.ui', self)
        # self.progress_signal = pyqtSignal(str)
        self.pages = chosen_pages
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

        self.result_button.clicked.connect(self.goto_result_screen)
        self.result_button.setEnabled(False)

        self.test_key = None

        self.back_to_prop_button.setEnabled(True)
        self.back_to_prop_button.clicked.connect(self.back_to_prop_screen)

    def back_to_prop_screen(self):

        screen_manager.removeWidget(self)
        self.deleteLater()

    def goto_result_screen(self):
        screen_manager.addWidget(ResultsScreen(log_key=self.test_key))
        screen_manager.setCurrentIndex((screen_manager.currentIndex() + 1))

    def update_terminal(self, data):
        data = '<p>{}</p>'.format(data)
        self.textMonitor.append(data)

    def convert_to_hyper_text(self, data):
        dict_data = literal_eval(data)
        error = 'style="color:#FF0000;"'
        if dict_data['error']:
            info = '<a href="{}" {} >{}</a>'.format(dict_data['url'], error, dict_data['name'])
        else:
            info = '<a href="{}" >{}</a>'.format(dict_data['url'], dict_data['name'])
        self.textMonitor.append(info)

    def update_progress_bar(self, value):
        self.progressBar.setValue(value)

    def cancel_click(self):
        self.signals.end_flag.put(True)
        self.close_test()

    def close_test(self):
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.result_button.setEnabled(True)
        self.back_to_prop_button.setEnabled(True)
        self.update_terminal('Test Finished ')

    def start_click(self):
        if not self.signals.end_flag.empty():
            self.signals.end_flag.get()
        self.test_key = time.strftime("%d_%b_%Y_%H.%M.%S", time.gmtime())
        self.test_runner = Excecutor(TestUtility.test_with_pyqt_slots, self.signals, self.pages, self.test_key)
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.back_to_prop_button.setEnabled(False)
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
            self.function(*self.args)
        except Exception as e:
            print('Exception was raised during test, ' + str(e))
            return


class ResultsScreen(QDialog):
    def __init__(self, log_key):
        super(ResultsScreen, self).__init__()
        loadUi('Qt_ui/result.ui', self)
        self.data, self.file_path = TestUtility.get_test_result(log_key=log_key)
        self.data.replace('target="_blank"', '')
        self.result_monitor.setOpenExternalLinks(True)
        self.result_monitor.setOpenLinks(True)
        self.result_monitor.append(self.data)
        self.open_rfile_button.clicked.connect(self.open_result_file)
        self.exit_button.clicked.connect(self.exit_program)

    def open_result_file(self):
        os.system("start {}".format(self.file_path))

    def exit_program(self):
        QCoreApplication.quit()


class CBSTestApplication(QApplication):
    def __init__(self, arguments):
        super(CBSTestApplication, self).__init__(arguments)


if __name__ == "__main__":
    app = CBSTestApplication(sys.argv)
    screen_manager = QStackedWidget()
    screen_manager.setWindowIcon(QIcon('../usable/Images/1200px-LOGO_LAMAS.jpg'))

    login = LogInScreen()
    choose = TestPropertiesScreen()
    # test_progress = TestProgressScreen()
    # result = ResultsScreen()

    screen_manager.addWidget(login)
    screen_manager.addWidget(choose)
    # screen_manager.addWidget(test_progress)
    # screen_manager.addWidget(result)

    screen_manager.setFixedWidth(630)
    screen_manager.setFixedHeight(550)

    # screen_manager.setCurrentIndex((screen_manager.currentIndex() + 1))
    screen_manager.show()

    sys.exit(app.exec())
