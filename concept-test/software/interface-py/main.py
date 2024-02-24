import sys
import os
from pathlib import Path
import serial
from serial.tools.list_ports import comports
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import pandas as pd
import warnings
import json
from interfaz import *

warnings.simplefilter(action='ignore', category=FutureWarning)

scurve_sp_cmap = plt.get_cmap("inferno").copy()  # cmap for the summary 2D plot
scurve_sp_norm = Normalize(vmin=0.0, vmax=200, clip=False)


class Interfaz(Ui_MainWindow):
    def __init__(self, interfaz):
        super(Interfaz, self).__init__()
        self.setupUi(interfaz)

        # auxiliar vars
        self.n_heights = 10
        self.plot_index = 0
        self.current_height = 0

        # setting up the serial conectrion panel 
        self.serial_port = serial.Serial(timeout=1)
        self.baud_list = ["1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"]
        self.baud_comboBox.addItems(self.baud_list)
        self.baud_comboBox.setCurrentIndex(-1)
        self.show_status_message("Seleccione un puerto y presione conectar...")
        self.refreshCOMPorts()
        self.redLedIcon = QPixmap("led-red-on.png").scaled(20,20)
        self.greenLedIcon = QPixmap("green-led-on.png").scaled(20,20)
        self.LED_label.setPixmap(self.redLedIcon)

        # setting up the button colors
        self.connect_disconnect_button.setStyleSheet("QPushButton {background-color:lightgreen}")
        self.motor_enb_dis_pushButton.setStyleSheet("QPushButton {background-color:lightgreen}")
        self.oven_enb_dis_pushButton.setStyleSheet("QPushButton {background-color:lightgreen}")

        # setting up the file panel
        self.output_path = Path(".")
        self.file_path_lineEdit.setText(str(self.output_path.cwd()))

        # setting up the data viewer panel
        self.setup_canvas()

        self.plot_timer = QTimer(self.centralwidget)
        self.plot_timer.timeout.connect(self.update_plots)
        self.plot_delay = 100

        # connection buttons
        self.COM_comboBox.currentIndexChanged.connect(self.portSelection)
        self.baud_comboBox.currentIndexChanged.connect(self.baudSelection)
        self.connect_disconnect_button.clicked.connect(self.open_close_port)

        # motor buttons
        self.motor_enb_dis_pushButton.clicked.connect(self.enable_disable_motor)
        self.send_speed_pushButton.clicked.connect(self.send_speed)
        self.set_cero_ref_pushButton.clicked.connect(self.set_ceroRef)
        self.move_pushButton.clicked.connect(self.move_motor)

        # oven buttons
        self.send_oven_temp_pushButton.clicked.connect(self.send_temp_setPoint)
        self.send_oven_param_pushButton.clicked.connect(self.send_tunning_params)
        self.oven_enb_dis_pushButton.clicked.connect(self.enable_disable_oven)

        # plots buttons
        self.take_data_horizontalSlider.valueChanged.connect(self.enb_dis_data_taking)
        self.reset_plots_pushButton.clicked.connect(self.reset_plots)
        self.path_pushButton.clicked.connect(self.choose_file_path)
        self.save_plots_pushButton.clicked.connect(self.save_plots)


    # ---------------------------- Arduino connection functions ------------------------------------
    def open_close_port(self):
        if self.connect_disconnect_button.isChecked():
            if self.open_port():
                self.connect_disconnect_button.setText("Desconectar")
                self.connect_disconnect_button.setStyleSheet("QPushButton {background-color:lightcoral}")
            else:
                self.show_warning_messageBox("Falla al conectar, intente de nuevo.")
        else:
            self.close_port()
            self.connect_disconnect_button.setText("Conectar")
            self.connect_disconnect_button.setStyleSheet("QPushButton {background-color:lightgreen}")


    def open_port(self):
        self.show_status_message("conectando...")
        try:
            self.serial_port.close()
            self.serial_port.open()
            self.serial_port.flushInput()
            self.serial_port.flushOutput()
            self.LED_label.setPixmap(self.greenLedIcon)
            self.show_status_message("conectado")
            return True

        except:
            self.LED_label.setPixmap(self.redLedIcon)
            self.close_port()
            self.show_status_message("Falla al conectar, intente de nuevo")
            return False


    def close_port(self):
        self.serial_port.flushInput()
        self.serial_port.flushOutput()
        self.serial_port.close()
        self.LED_label.setPixmap(self.redLedIcon)
        self.show_status_message("Puerto desconectado")
        self.show_status_message("Seleccione un puerto y presione conectar...")


    def portSelection(self):
        selectItem = self.COM_comboBox.currentText()
        self.show_status_message("")
        if selectItem == "refresh":
            self.refreshCOMPorts()
            self.show_status_message("Actualizando puertos")

        elif selectItem == "---":
            self.show_status_message("Seleccione un puerto y presione conectar...")

        else:
            self.serial_port.port = selectItem
            self.show_status_message("Puerto establecido: " + selectItem)


    def baudSelection(self):
        self.show_status_message("")
        selectItem = self.baud_comboBox.currentText()
        self.serial_port.baudrate = selectItem
        self.show_status_message("Baud rate establecida: " + selectItem)


    def refreshCOMPorts(self):
        ports = ["---", "refresh"]
        
        for i in comports():
            ports.append(i.device)

        self.COM_comboBox.clear()
        self.COM_comboBox.addItems(ports)

    # ---------------------------- Arduino control functions ---------------------------------------
    def enable_disable_motor(self):
        try: 
            if self.motor_enb_dis_pushButton.isChecked():
                self.arduino_request("em")
                _ = self.arduino_response()
                self.motor_enb_dis_pushButton.setText("Deshabilitar")
                self.motor_enb_dis_pushButton.setStyleSheet("QPushButton {background-color:lightcoral}")

            else:
                self.arduino_request("dm")
                _ = self.arduino_response()
                self.motor_enb_dis_pushButton.setText("Habilitar")
                self.motor_enb_dis_pushButton.setStyleSheet("QPushButton {background-color:lightgreen}")

            return True

        except serial.serialutil.PortNotOpenError as err:
            self.show_critical_messageBox(err)
            self.motor_enb_dis_pushButton.setChecked(False)

            return False


    def send_speed(self):
        try:
            self.arduino_request("v" + str(self.speed_spinBox.value()))
            _ = self.arduino_response()

        except serial.serialutil.PortNotOpenError as err:
            self.show_critical_messageBox(err)


    def  move_motor(self):
        if self.motor_enb_dis_pushButton.isChecked():
            self.arduino_request("p" + str(self.pos_spinBox.value()))
            _ = self.arduino_response()

        else:
            self.show_warning_messageBox("No ha habilitado el movimiento del motor")


    def set_ceroRef(self):
        try:
            if not self.motor_enb_dis_pushButton.isChecked():
                self.arduino_request("p0")
                _ = self.arduino_response()
                self.arduino_request("c")
                _ = self.arduino_response()
                self.pos_spinBox.setValue(0)

            else:
                self.show_warning_messageBox(
                    "Deshabilite el movimiento del motor para poder cambiar el cero de referencia."
                )

        except serial.serialutil.PortNotOpenError as err:
            self.show_critical_messageBox(err)


    def enable_disable_oven(self):
        try:
            if self.oven_enb_dis_pushButton.isChecked():
                self.arduino_request("eo")
                _ = self.arduino_response()
                self.oven_enb_dis_pushButton.setText("Apagar")
                self.oven_enb_dis_pushButton.setStyleSheet("QPushButton {background-color:lightcoral}")

            else:
                self.arduino_request("do")
                _ = self.arduino_response()
                self.oven_enb_dis_pushButton.setText("Encender")
                self.oven_enb_dis_pushButton.setStyleSheet("QPushButton {background-color:lightgreen}")

            return True

        except serial.serialutil.PortNotOpenError as err:
            self.show_critical_messageBox(err)
            self.oven_enb_dis_pushButton.setChecked(False)

            return False


    def send_temp_setPoint(self):
        try:
            self.arduino_request("s" + str(self.setPoint_temp_doubleSpinBox.value()))
            _ = self.arduino_response()

        except serial.serialutil.PortNotOpenError as err:
            self.show_critical_messageBox(err)


    def send_tunning_params(self):
        try:
            self.arduino_request("kp" + str(self.kp_doubleSpinBox.value()))
            self.arduino_request("ki" + str(self.kp_doubleSpinBox.value()))
            self.arduino_request("kd" + str(self.kp_doubleSpinBox.value()))
            _ = self.arduino_response()

        except serial.serialutil.PortNotOpenError as err:
            self.show_critical_messageBox(err)

    # ------------------------------------- plot functions -----------------------------------------
    def setup_canvas(self):
        self.reset_data()
        self.produce_plots(first_time=True)
        self.temp_plot_widget.canvas.draw()
        self.tempPID_plot_widget.canvas.draw()


    def reset_data(self):
        # initialize data with zeros
        self.data_base = [pd.DataFrame()] * self.n_heights
        for i in  range(self.n_heights):
            self.data_base[i] = self.data_base[i].append(
                {"time": 0, "T": 0, "T_PID": 0},
                ignore_index=True
            )


    def enb_dis_data_taking(self):
        if self.take_data_horizontalSlider.value():
            # enable motor interface
            self.motor_enb_dis_pushButton.setChecked(True)
            if self.enable_disable_motor():
                # enable linear plots timer
                self.plot_timer.start(self.plot_delay)
            else:
                self.take_data_horizontalSlider.blockSignals(True)
                self.take_data_horizontalSlider.setValue(0)
                self.take_data_horizontalSlider.blockSignals(False)
        else:
            # disble motor interface
            self.motor_enb_dis_pushButton.setChecked(False)
            self.enable_disable_motor()
            # disable linear plots timer
            self.plot_timer.stop()

        #     return True

        # except:
        #     self.motor_enb_dis_pushButton.setChecked(False)
            
        #     return False


    def update_plots(self):
        # get data from arduino
        self.arduino_request("g")
        res = json.loads(self.arduino_response())
        # add time value
        res["time"] = self.data_base[self.current_height]["time"].iloc[-1] + self.plot_delay
        
        # add data to data_base
        self.data_base[self.current_height] = self.data_base[self.current_height].append(
            res,
            ignore_index=True,
        )

        # redraw plots with the new data
        self.produce_plots()
        self.temp_plot_widget.canvas.draw()
        self.tempPID_plot_widget.canvas.draw()

        # ------------------ section to produce temperature maps -------------
        # self.old_index = 0
        # if t  % self.delay_spinBox.value() == 0 and abs(self.pos_spinBox.value() - self.path_steps_spinBox.value())!=0:
        #     self.pos_spinBox.setValue(self.pos_spinBox.value() + self.steps_spinBox.value())
        #     self.move_motor()
        #     self.new_index = len(self.T_data)-1
        #     self.map[0] += [sum(self.T_data[self.old_index:self.new_index])/len(self.T_data)]
        #     self.old_index=self.new_index
        #     self.update_map = True
        # else:
        #     self.update_map = False
        # self.temp_map_widget.canvas.draw()


    def produce_plots(self, first_time=False, to_render=True):
        self.temp_plot_widget.canvas.axes.cla()
        self.tempPID_plot_widget.canvas.axes.cla()

        if not to_render:
            self.plot_index = 0

        self.temp_plot_widget.canvas.axes.plot(
            self.data_base[self.current_height]["time"][self.plot_index:],
            self.data_base[self.current_height]["T"][self.plot_index:],
            "--.g"
        )
        self.tempPID_plot_widget.canvas.axes.plot(
            self.data_base[self.current_height]["time"][self.plot_index:],
            self.data_base[self.current_height]["T_PID"][self.plot_index:],
            "--.r"
        )

        self.temp_plot_widget.canvas.axes.grid(True, color="gray", linewidth=0.5)
        self.temp_plot_widget.canvas.axes.set_title("Temperatura de la muestra")
        self.temp_plot_widget.canvas.axes.set_ylabel(r"T ($^\circ$C)")
        self.temp_plot_widget.canvas.axes.set_xlabel("t (ms)")
        self.tempPID_plot_widget.canvas.axes.grid(True, color="gray", linewidth=0.5)
        self.tempPID_plot_widget.canvas.axes.set_title("Temperatura de control")
        self.tempPID_plot_widget.canvas.axes.set_ylabel(r"T ($^\circ$C)")
        self.tempPID_plot_widget.canvas.axes.set_xlabel("t (ms)")

        # this index is to draw just 20 points in the linear plots
        if self.data_base[self.current_height].shape[0] > 20:
            self.plot_index += 1


        #-------------- section to plot the temperature map -----------------
        # self.temp_map_widget.canvas.axes.cla()
        # if self.update_map:
        #     print("Entro")
        #     self.ims = self.temp_map_widget.canvas.axes.imshow(
        #         self.map,
        #         #aspect= 20.0 / 20,
        #         cmap=scurve_sp_cmap,
        #         norm=scurve_sp_norm,
        #         origin="lower",
        #     )
        #     if first_time:
        #         self.plot_index = 0
        #         self.cbar = self.temp_map_widget.canvas.figure.colorbar(
        #             self.ims,
        #             ax=self.temp_map_widget.canvas.axes,
        #             pad=0.15,
        #             fraction=0.048,
        #             orientation="horizontal"
        #         )


    def reset_plots(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText("Esta seguro de querer borrar las graficas?")
        msgBox.setWindowTitle("")
        msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        buttonY = msgBox.button(QMessageBox.Yes)
        buttonN = msgBox.button(QMessageBox.No)
        msgBox.exec_()

        if msgBox.clickedButton() == buttonY:
            self.temp_plot_widget.canvas.axes.cla()
            self.temp_map_widget.canvas.axes.cla()
            #self.temp_map_widget.canvas.axes.cla()
            self.setup_canvas()
            self.show_status_message("Graficas borradas")

        elif msgBox.clickedButton() == buttonN:
            pass


    def choose_file_path(self):
        self.show_status_message("")
        path = Path(
            QFileDialog.getExistingDirectory(self.centralwidget, "Ruta de resultados", "./results")
            )

        if path.is_dir():
            self.output_path = path
            self.file_path_lineEdit.setText(str(path))
            self.show_status_message("Ruta establecida")

        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Error: " + repr("Escoja una ruta correcta"))
            msgBox.setWindowTitle("Error")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
            self.show_status_message("Error estableciendo ruta")


    def save_plots(self):
        # This functions doesn't work well, it is necessary to create the figures from the begin
        # since take the plot from interface result in a very bad resolution image. It could be
        # better to save data insted of plot.
        self.show_status_message("")
        try:
            self.produce_plots(to_render=False)
            self.temp_plot_widget.canvas.draw()
            self.tempPID_plot_widget.canvas.draw()
            self.temp_plot_widget.canvas.axes.figure.savefig(self.output_path / "plot_test.png")
            self.tempPID_plot_widget.canvas.axes.figure.savefig(self.output_path / "plotPID_test.png")
            saved = True
        except:
            saved = False

        if saved:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Graficas guardadas exitosamente")
            msgBox.setWindowTitle("")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
            self.show_status_message("Guardado exitosamente")
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("No se pudo guardar las graficas")
            msgBox.setWindowTitle("")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
            self.show_status_message("No se pudo guardar las graficas")


    # ---------------------------------- auxiliar functions ----------------------------------------
    def arduino_request(self, command):
        self.serial_port.flushInput()
        self.serial_port.flushOutput()
        self.show_status_message("Enviando " + command)
        self.serial_port.write(str.encode(command))


    def arduino_response(self):
        while self.serial_port.in_waiting == 0:        
            pass
        res = self.serial_port.readline().decode("utf-8")
        self.show_status_message("recibido: " + res)
        return res


    def show_status_message(self, message):
        self.statusbar.clearMessage()
        self.statusbar.showMessage(message)


    def show_warning_messageBox(self, w_message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Warning: " + repr(w_message))
        msgBox.setWindowTitle("Warning")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()


    def show_critical_messageBox(self, err):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Error: " + repr(err))
            msgBox.setWindowTitle("Error")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()


def main():
    app = QApplication(sys.argv)
    interfaz = QMainWindow()
    ui = Interfaz(interfaz)
    interfaz.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()