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


class UserDialog(DialogWidget):
    def __init__(self, parent):
        super(UserDialog, self).__init__(parent, 'user_dialog.ui')
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("Change")
        self.close_button.clicked.connect(self.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.accept)

    def get_user_values(self):
        name = "None" if not self.name_lineEdit.text() else self.name_lineEdit.text()
        email = "None" if not self.email_lineEdit.text() else self.email_lineEdit.text()
        role = "None" if not self.role_lineEdit.text() else self.role_lineEdit.text()

        return name, email, role


class InfoDialog(DialogWidget):
    def __init__(self, parent):
        super(InfoDialog, self).__init__(parent, 'info_dialog.ui')
        self.info_ok_button.clicked.connect(lambda: self.close())
