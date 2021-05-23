import time

# from PyQt5 import QtWidgets, QtGui, QtCore

import traceback, sys

# from PyQt6.QtCore import pyqtSlot
from PyQt6 import QtCore
from PyQt6.QtCore import QRunnable, pyqtSlot, QThreadPool, pyqtSignal, QObject

from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QProgressBar, QVBoxLayout, QGraphicsObject


class Worker(QRunnable):
    class WorkerSignals(QObject):
        status = QtCore.pyqtSignal(int)
        finished = QtCore.pyqtSignal()
        error = QtCore.pyqtSignal(tuple)
        result = QtCore.pyqtSignal(object)

    def __init__(self, function):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.function = function
        # self.args = args
        # self.kwargs = kwargs
        self.signals = self.WorkerSignals()

    @pyqtSlot()
    def run(self):
        counter = 0
        while counter < 100:
            self.signals.status.emit(counter)
            counter += 1
            time.sleep(0.1)


class QthreadApp(QDialog):
    def __init__(self):
        super(QthreadApp, self).__init__()
        self.layout = QVBoxLayout()
        self.button = QPushButton('start process')
        self.button.clicked.connect(self.start_progress)
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.progress)
        self.setLayout(self.layout)
        self.thread_pool = QThreadPool()

    def start_progress(self):
        # print('clicked')
        # back_process = MainProcess()
        # back_process.process_status.connect(self.change_progressbar)
        # back_process.run()
        worker = Worker(self.change_status_bar)

        worker.signals.status.connect(self.change_progressbar)
        self.thread_pool.start(worker)


    def change_progressbar(self, data):
        self.progress.setValue(data)

    def change_status_bar(self):
        counter =0
        while counter<100:
            time.sleep(0.1)
            counter+=1



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = QthreadApp()
    myapp.show()
    sys.exit(app.exec())
