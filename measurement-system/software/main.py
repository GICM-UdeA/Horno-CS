import sys
import os
from pathlib import Path
import serial
from serial.tools.list_ports import comports
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
import pandas as pd
import warnings
import json
from numpy import random, arange, zeros
from interface import *


warnings.simplefilter(action='ignore', category=FutureWarning)

class MS_interface(MS_interface_layout):
    def __init__(self):
        super(MS_interface, self).__init__()
        # setting up layout interface
        self.setupUi()

        self.COM_connect_button.clicked.connect(lambda: self.connect_disconnect_COM(1))
        self.COM_disconnect_button.clicked.connect(lambda: self.connect_disconnect_COM(0))

    def connect_disconnect_COM(self, state):
        if state:
            try:
                self.serial_port.__init__(timeout=1, **self.serial_params)

                self.serial_port.close()
                self.serial_port.open()
                self.serial_port.flushInput()
                self.serial_port.flushOutput()

                self.disconnect_frame.show()
                self.connect_frame.hide()
                self.serial_monitor_textEdit.appendPlainText(self.serial_params["port"] + " Connected...")

            except Exception as e:
                self.serial_monitor_textEdit.appendPlainText(str(e))

        else:
            try:
                self.serial_port.close()
                self.disconnect_frame.hide()
                self.connect_frame.show()
                self.serial_monitor_textEdit.appendPlainText(self.serial_params["port"] + " Disconnected...")

            except Exception as e:
                self.serial_monitor_textEdit.appendPlainText("Error trying to close " + self.serial_params["port"])

def main():
    # Handle high resolution displays:
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    ui = MS_interface()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()