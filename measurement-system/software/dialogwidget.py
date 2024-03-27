from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi


class DialogWidget(QtWidgets.QDialog):
    def __init__(self, parent, ui_file):
        super(DialogWidget, self).__init__(parent)
        loadUi(ui_file, self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.window_header.mouseMoveEvent = self.move_window

    def move_window(self, event):
        self.clickPosition = self.pos()
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()