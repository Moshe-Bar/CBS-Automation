import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QScrollArea, QApplication


class Screen3(QWidget):       # Screen to display data
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # layout for check box container widget
        chkBoxLayout = QVBoxLayout()
        # create list of checkboxes
        self.checkboxes = []
        numofCheckboxes = 30
        for x in range(numofCheckboxes):
            self.checkboxes.append(QCheckBox('test'))
        # add checkboxes to chkBoxLayout
        for i, chkbox in enumerate(self.checkboxes):
            chkbox.setChecked(True)
            chkBoxLayout.addWidget(chkbox)
        chkBoxLayout.addStretch(1)
        chkBoxLayout.setMargin(0)
        chkBoxLayout.setContentsMargins(0,0,0,0)
        chkBoxLayout.setSpacing(0)

        # checkbox container widget
        widget = QWidget()
        widget.setStyleSheet(""".QWidget {background-color: rgb(255, 255, 255);}""")
        widget.setLayout(chkBoxLayout)

        # checkbox scroll area, gives scrollable view on widget
        scroll = QScrollArea()
        scroll.setMinimumWidth(120)
        scroll.setMinimumHeight(200) # would be better if resizable
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(widget)

        lay = QVBoxLayout(self)
        lay.addWidget(scroll)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    s = Screen3()
    # screen_manager = QStackedWidget()
    # screen_manager.setWindowIcon(QIcon('../DataBase/Images/1200px-LOGO_LAMAS.jpg'))