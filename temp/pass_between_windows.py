from PyQt5 import QtCore, QtGui, QtWidgets

#from Calendar import Ui_CalendarWindow
class Ui_CalendarWindow(object):
    def setupUi(self, CalendarWindow):
        CalendarWindow.setObjectName("CalendarWindow")
        CalendarWindow.resize(512, 458)
        self.centralwidget = QtWidgets.QWidget(CalendarWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.CalendarBox = QtWidgets.QCalendarWidget(self.centralwidget)
        self.CalendarBox.setGeometry(QtCore.QRect(20, 20, 464, 289))
        self.CalendarBox.setObjectName("CalendarBox")
        self.pbSelect = QtWidgets.QPushButton(self.centralwidget)
        self.pbSelect.setGeometry(QtCore.QRect(160, 330, 181, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pbSelect.setFont(font)
        self.pbSelect.setObjectName("pbSelect")
#        self.pbSelect.clicked.connect(self.PickedDate)
        CalendarWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(CalendarWindow)
        self.statusbar.setObjectName("statusbar")
        CalendarWindow.setStatusBar(self.statusbar)

        self.retranslateUi(CalendarWindow)
        QtCore.QMetaObject.connectSlotsByName(CalendarWindow)

    def retranslateUi(self, CalendarWindow):
        _translate = QtCore.QCoreApplication.translate
        CalendarWindow.setWindowTitle(_translate("CalendarWindow", "MainWindow"))
        self.pbSelect.setText(_translate("CalendarWindow", "Select"))


class Ui_FirstWindow(object):
    def setupUi(self, FirstWindow):
        FirstWindow.setObjectName("FirstWindow")
        FirstWindow.resize(654, 242)
        self.centralwidget = QtWidgets.QWidget(FirstWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lbDate = QtWidgets.QLabel(self.centralwidget)
        self.lbDate.setGeometry(QtCore.QRect(330, 70, 281, 131))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.lbDate.setFont(font)
        self.lbDate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbDate.setObjectName("lbDate")
        self.pbSelectDate = QtWidgets.QPushButton(self.centralwidget)
        self.pbSelectDate.setGeometry(QtCore.QRect(80, 100, 191, 61))
        self.pbSelectDate.setObjectName("pbSelectDate")
#        self.pbSelectDate.clicked.connect(self.Open_Calendar)
        FirstWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(FirstWindow)
        self.statusbar.setObjectName("statusbar")
        FirstWindow.setStatusBar(self.statusbar)

        self.retranslateUi(FirstWindow)
        QtCore.QMetaObject.connectSlotsByName(FirstWindow)

    def retranslateUi(self, FirstWindow):
        _translate = QtCore.QCoreApplication.translate
        FirstWindow.setWindowTitle(_translate("FirstWindow", "MainWindow"))
        self.lbDate.setText(_translate("FirstWindow", "Sep"))
        self.pbSelectDate.setText(_translate("FirstWindow", "Select Date"))


class CalendarWindow(QtWidgets.QMainWindow, Ui_CalendarWindow):              # +
    def __init__(self):
        super(CalendarWindow, self).__init__()
        self.setupUi(self)


class FirstWindow(QtWidgets.QMainWindow, Ui_FirstWindow):                    # +
    def __init__(self):
        super(FirstWindow, self).__init__()
        self.setupUi(self)

        self.pbSelectDate.clicked.connect(self.Open_Calendar)

    def Open_Calendar(self):
        self.window = CalendarWindow()
        self.window.setupUi(self.window)
        self.window.show()

        self.window.pbSelect.clicked.connect(self.PickedDate)

    def PickedDate(self):    # , var
        self.selecteddate = self.window.CalendarBox.selectedDate()
#        print(self.selecteddate.toString('MMM')+'-'+self.selecteddate.toString('yyyy'))
        self.lbDate.setText(self.selecteddate.toString('ddd-MMM-yyyy'))     # <---

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = FirstWindow()
    w.show()
    sys.exit(app.exec_())