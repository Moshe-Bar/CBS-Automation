from PyQt5 import QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.listwidget = QtWidgets.QListWidget()
        self.listwidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        self.setCentralWidget(self.listwidget)
        # add some items
        for i in range(5):
            self.listwidget.addItem(str(i))

        # add items with selection
        for i in range(5):
            it = QtWidgets.QListWidgetItem(str(i))
            self.listwidget.addItem(it)
            it.setSelected(True)

        # selected items
        for item in self.listwidget.selectedItems():
            print(item.text())

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())