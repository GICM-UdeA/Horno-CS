from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.uic import loadUi
import resources

class InfoDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(InfoDialog, self).__init__(parent)
        loadUi('info_dialog.ui', self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.info_title.mouseMoveEvent = self.move_window
        self.info_ok_button.clicked.connect(lambda: self.close())

    def move_window(self, event):
        self.clickPosition = self.pos()
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.clickPosition)
            self.clickPosition = event.globalPos()
            event.accept()

class MS_interface(QtWidgets.QMainWindow):
    def __init__(self):
        super(MS_interface, self).__init__()

        loadUi('interface.ui', self)
        
        # ----------------------------- setting up UI elements -------------------------------------
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.show_hide_menu(0)
        self.resize_window(0)
        self.size_grip_button.hide() # Need to be fixed
        self.set_body_page(0)

        self.body_header.mouseMoveEvent = self.move_window

        self.show_menu_button.clicked.connect(lambda: self.show_hide_menu(1))
        self.hide_menu_button.clicked.connect(lambda: self.show_hide_menu(0))

        self.minimize_mainWindow.clicked.connect(lambda: self.showMinimized())
        self.restore_max_mainWindow.clicked.connect(lambda: self.resize_window(1))
        self.restore_min_mainWindow.clicked.connect(lambda: self.resize_window(0))
        self.close_mainWindow.clicked.connect(lambda: self.close())

        self.home_button.clicked.connect(lambda: self.set_body_page(0))
        self.connect_button.clicked.connect(lambda: self.set_body_page(1))
        self.user_button.clicked.connect(lambda: self.set_body_page(2))
        self.data_plot_button.clicked.connect(lambda: self.set_body_page(3))
        self.data_regs_button.clicked.connect(lambda: self.set_body_page(4))

        self.info_button.clicked.connect(self.show_info)
        # ------------------------------------------------------------------------------------------

    def show_hide_menu(self, show):
        animation = QtCore.QPropertyAnimation(self.leftMenu, b"maximumWidth")

        if show:
            self.show_menu_button.hide()
            self.hide_menu_button.show()
            animation.setStartValue(90)
            animation.setEndValue(30)
        else:
            self.show_menu_button.show()
            self.hide_menu_button.hide()
            animation.setStartValue(30)
            animation.setEndValue(90)

        animation.setDuration(1000)
        animation.setEasingCurve(QtCore.QEasingCurve.InOutBack)
        animation.start()
    
    def resize_window(self, size):
        if size:
            self.restore_max_mainWindow.hide()
            self.restore_min_mainWindow.show()
            self.showMaximized()
        else:
            self.restore_max_mainWindow.show()
            self.restore_min_mainWindow.hide()
            self.showNormal()

    def move_window(self, event):
        if not self.isMaximized():
            self.clickPosition = self.pos()
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()
        if event.globalPos().y() <= 10:
            self.resize_window(1)
        else:
            self.resize_window(0)

    def set_body_page(self, page):
        if page == 0:
            self.main_body_content.setCurrentWidget(self.home_page)
        if page == 1:
            self.main_body_content.setCurrentWidget(self.connection_page)
        if page == 2:
            self.main_body_content.setCurrentWidget(self.user_page)
        if page == 3:
            self.main_body_content.setCurrentWidget(self.data_viewer_page)
        if page == 4:
            self.main_body_content.setCurrentWidget(self.data_regs_page)
        if page == 3 or page == 4:
            self.control_panel.show()
        else:
            self.control_panel.hide()

    def show_info(self):
        info_window = InfoDialog(self)
        info_window.exec_()

if __name__ == "__main__":
    import sys

    # Handle high resolution displays:
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    ui = MS_interface()
    ui.show()
    sys.exit(app.exec_())
