import serial
from serial.tools.list_ports import comports
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
import resources
from dialogwidgets import *
from pandasmodel import PandasModel
from pandas import DataFrame
from numpy import zeros, arange

class MS_interface_layout(QtWidgets.QMainWindow):
    def setupUi(self):
        loadUi('interface.ui', self)

        # ------------------------  ----- setting up UI elements -------------------------------------
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.show_hide_menu(0, "main")
        self.show_hide_menu(0, "advance-connection")
        self.disconnect_frame.hide()
        self.frame_4.hide()
        self.resize_window(0)
        self.size_grip_button.hide() # Need to be fixed
        self.set_body_page(0)

        self.body_header.mouseMoveEvent = self.move_window

        self.show_main_menu_button.clicked.connect(lambda: self.show_hide_menu(1, "main"))
        self.hide_main_menu_button.clicked.connect(lambda: self.show_hide_menu(0, "main"))
        self.show_connection_settings_menu_button.clicked.connect(lambda: self.show_hide_menu(1, "connection"))
        self.hide_connection_settings_menu_button.clicked.connect(lambda: self.show_hide_menu(0, "connection"))
        self.show_advance_connection_settings_button.clicked.connect(lambda: self.show_hide_menu(1, "advance-connection"))
        self.hide_advance_connection_settings_button.clicked.connect(lambda: self.show_hide_menu(0, "advance-connection"))

        self.minimize_mainWindow.clicked.connect(lambda: self.showMinimized())
        self.restore_max_mainWindow.clicked.connect(lambda: self.resize_window(1))
        self.restore_min_mainWindow.clicked.connect(lambda: self.resize_window(0))
        self.close_mainWindow.clicked.connect(lambda: self.close())

        self.home_button.clicked.connect(lambda: self.set_body_page(0))
        self.connect_button.clicked.connect(lambda: self.set_body_page(1))
        self.data_plot_button.clicked.connect(lambda: self.set_body_page(2))
        self.data_regs_button.clicked.connect(lambda: self.set_body_page(3))
        self.info_button.clicked.connect(self.show_info)
        # --------------------------- setting up COM interfaces ------------------------------------
        self.serial_port = serial.Serial(timeout=1)
        self.serial_params = dict()
        self.baud_list = {
            "1200": 1200, "2400": 2400, "4800": 4800, "9600": 9600, "19200": 19200,
            "38400": 38400, "57600": 57600, "115200": 115200
        }
        self.data_bits_list = {
            "5": serial.FIVEBITS, "6": serial.SIXBITS, "7": serial.SEVENBITS, "8": serial.EIGHTBITS
        }
        self.parity_list = {
            "None": serial.PARITY_NONE, "Even": serial.PARITY_EVEN, "Odd": serial.PARITY_ODD
        }
        self.stop_bits_list = {
            "1": serial.STOPBITS_ONE, "1.5": serial.STOPBITS_ONE_POINT_FIVE, "2": serial.STOPBITS_TWO
        }
        self.flowcontrol_list = ["None", "XON/XOFF", "RTS/CTS", "DTR/DSR"]

        self.refreshCOMPorts()
        self.baud_combobox.addItems([*self.baud_list])
        self.databits_combobox.addItems([*self.data_bits_list])
        self.parity_combobox.addItems([*self.parity_list])
        self.stopbits_combobox.addItems([*self.stop_bits_list])
        self.flowcontrol_combobox.addItems([*self.flowcontrol_list])

        self.COM_combobox.currentIndexChanged.connect(lambda: self.serial_combobox_selection("port"))
        self.baud_combobox.currentIndexChanged.connect(lambda: self.serial_combobox_selection("baudrate"))
        self.databits_combobox.currentIndexChanged.connect(lambda: self.serial_combobox_selection("databits"))
        self.parity_combobox.currentIndexChanged.connect(lambda: self.serial_combobox_selection("parity"))
        self.stopbits_combobox.currentIndexChanged.connect(lambda: self.serial_combobox_selection("stopbits"))
        self.flowcontrol_combobox.currentIndexChanged.connect(lambda: self.serial_combobox_selection("flowcontrol"))

        self.baud_combobox.setCurrentIndex(7)
        self.databits_combobox.setCurrentIndex(3)
    
        #---------------------------- setting up User interface ------------------------------------
        self.user_name = "None"
        self.user_email = "None"
        self.user_role = "None"
        
        self.user_button.setToolTip(
            "name: " + self.user_name + 
            "\nRole: " + self.user_role + 
            "\ne-mail: " + self.user_email + "\n"
        )
        self.user_button.clicked.connect(self.update_user_info)

        # --------------------------- setting up data regs interface -------------------------------
        self.reset_table_data()


    # ----------------------------------- serial configurations ------------------------------------
    def refreshCOMPorts(self):
        ports = ["---", "refresh"]
        for i in comports():
            ports.append(i.device)

        self.COM_combobox.clear()
        self.COM_combobox.addItems(ports)

    def serial_combobox_selection(self, combobox):
        if combobox == "port":
            selectItem = self.COM_combobox.currentText()
            if selectItem == "refresh":
                self.refreshCOMPorts()
            elif selectItem == "---":
                pass
            else:
                self.serial_params["port"] = selectItem

        elif combobox == "baudrate":
            self.serial_params["baudrate"] = self.baud_list[self.baud_combobox.currentText()]

        elif combobox == "databits":
            self.serial_params["bytesize"] = self.data_bits_list[self.databits_combobox.currentText()]

        elif combobox == "parity":
            self.serial_params["parity"] = self.parity_list[self.parity_combobox.currentText()]

        elif combobox == "stopbits":
            self.serial_params["stopbits"] = self.stop_bits_list[self.stopbits_combobox.currentText()]

        elif combobox == "flowcontrol":
            selectItem = self.flowcontrol_combobox.currentText()

            if selectItem == "XON/XOFF":
                self.serial_params["xonxoff"] = True
            elif selectItem == "RTS/CTS":
                self.serial_params["rtscts"] = True
            elif selectItem == "DTR/DSR":
                self.serial_params["dsrdtr"] = True
            else:
                pass

    # ----------------------------------- UIX style and effects ------------------------------------
    def show_hide_menu(self, show, menu):
        if menu == "main":
            widget = self.leftMenu
            show_button = self.show_main_menu_button
            hide_button = self.hide_main_menu_button
            animate = b"maximumWidth"
            values = (120, 35)

        elif menu == "connection":
            widget = self.connection_settings
            show_button = self.show_connection_settings_menu_button
            hide_button = self.hide_connection_settings_menu_button
            animate = b"maximumWidth"
            values = (150, 0)

        elif menu == "advance-connection":
            if show:
                self.advanced_connection_setting_frame.show()
                self.show_advance_connection_settings_button.hide()
                self.hide_advance_connection_settings_button.show()
            else:
                self.advanced_connection_setting_frame.hide()
                self.hide_advance_connection_settings_button.hide()
                self.show_advance_connection_settings_button.show()
            return 0

        animation = QtCore.QPropertyAnimation(widget, animate)

        if show:
            show_button.hide()
            hide_button.show()
            animation.setStartValue(values[0])
            animation.setEndValue(values[1])
        else:
            show_button.show()
            hide_button.hide()
            animation.setStartValue(values[1])
            animation.setEndValue(values[0])

        animation.setDuration(1000)
        animation.setEasingCurve(QtCore.QEasingCurve.Linear)
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
        else:
            self.show_hide_menu(0, "connection")
        if page == 2:
            self.main_body_content.setCurrentWidget(self.data_viewer_page)
        if page == 3:
            self.main_body_content.setCurrentWidget(self.data_regs_page)

        if page == 2 or page == 3:
            self.data_control_panel.show()
            self.frame_4.show()
        else:
            self.data_control_panel.hide()
            self.frame_4.hide()

        if page != 0:
            self.connection_control_panel.show()
        else:
            self.connection_control_panel.hide()

    def show_info(self):
        info_window = InfoDialog(self)
        info_window.exec_()

    # ----------------------------------- UIX data methods -----------------------------------------

    def update_user_info(self):
        try:
            user_dialog = UserDialog(self)
            user_dialog.setModal(True)
            if user_dialog.exec_() == QtWidgets.QDialog.Accepted :
                self.user_name, self.user_email, self.user_role = user_dialog.get_user_values()

        except Exception as e:
            print(e)

        self.user_button.setToolTip(
            "name: " + self.user_name + 
            "\nRole: " + self.user_role + 
            "\ne-mail: " + self.user_email + "\n"
        )

    def reset_table_data(self):
        # initialize data with zeros
        data = dict(zip(["T1", "T2", "T3", "T4", "T5", "T6"], zeros((6, 100))))
        data["time"] = arange(-24750, 250, 250)

        self.data = DataFrame(
            data,
            columns=["time", "T1", "T2", "T3", "T4", "T5", "T6"]
        )
        self.update_table_data()

    def update_table_data(self):    
        self.data_table_viewer.setModel(PandasModel(self.data))


if __name__ == "__main__":
    import sys

    # Handle high resolution displays:
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    ui = MS_interface_layout()
    ui.setupUi()
    ui.show()
    sys.exit(app.exec_())
