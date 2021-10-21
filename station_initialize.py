# -*- coding: utf-8 -*-

"""
Module implementing time_initialize
"""
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog

from ui.Ui_station_initialize import Ui_station_initialize
import os
import configparser
import traceback


class station_initialize(QDialog, Ui_station_initialize):
    """
    Class documentation goes here.
    """
    signal_station_ini = pyqtSignal(list)
    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(station_initialize, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(Qt.Dialog)
        # currentPath = os.getcwd()
        self.currentPath = "D:\CVT"
        ini_path = self.currentPath + "\station_config.ini"
        ini_exist = os.path.exists(ini_path)
        if ini_exist == 1:
            # ---已存在配置文件，
            try:
                # ---读取当前exist的数值
                config = configparser.ConfigParser()
                config.read_file(open(r"%s" % ini_path))
                stationID = config.get("站点信息", "站号")
                self.LineEdit_stationID.setText(stationID)
                interval_sendraw_h = config.get("原始数据发送", "时间间隔（时）")
                interval_sendraw_m = config.get("原始数据发送", "时间间隔（分）")
                self.spinBox_send_rawdata_h.setProperty("value", int(interval_sendraw_h))
                self.spinBox_send_rawdata_m.setProperty("value", int(interval_sendraw_m))
                interval_mlab_h = config.get("Matlab处理及结果发送", "时间间隔（时）")
                interval_mlab_m = config.get("Matlab处理及结果发送", "时间间隔（分）")
                self.spinBox_mlab_h.setProperty("value", int(interval_mlab_h))
                self.spinBox_mlab_m.setProperty("value", int(interval_mlab_m))
            except Exception as e:
                print(e)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        try:
            #-----get db releated info from ui----
            stationID = self.LineEdit_stationID.text()
            while len(stationID) < 4:
                stationID = '0' + stationID

            if len(stationID) > 4:
                stationID = stationID[-4:]

            interval_sendraw_h = self.spinBox_send_rawdata_h.text()
            interval_sendraw_m = self.spinBox_send_rawdata_m.text()

            interval_mlab_h = self.spinBox_mlab_h.text()
            interval_mlab_m = self.spinBox_mlab_m.text()

            #---read db config data---
            # currentPath = os.getcwd()
            ini_path = self.currentPath + "\station_config.ini"
            ini_exist = os.path.exists(ini_path)
            # ---if database_config is not exist created it-------
            config = configparser.ConfigParser()
            if ini_exist == 0:
                try:
                    # -----创建配置文件config.ini---------
                    config.add_section("站点信息")
                    config.set("站点信息", "站号", stationID)

                    config.add_section("原始数据发送")
                    config.set("原始数据发送", "时间间隔（时）", interval_sendraw_h)
                    config.set("原始数据发送", "时间间隔（分）", interval_sendraw_m)

                    config.add_section("Matlab处理及结果发送")
                    config.set("Matlab处理及结果发送", "时间间隔（时）", interval_mlab_h)
                    config.set("Matlab处理及结果发送", "时间间隔（分）", interval_mlab_m)

                    config.write(open(r"%s" % ini_path, "w"))
                except Exception as e:
                    print(e)
            else:
                # -----改写exiest的数值
                config.read(r"%s" % ini_path)
                config.set("站点信息", "站号", stationID)

                config.set("原始数据发送", "时间间隔（时）", interval_sendraw_h)
                config.set("原始数据发送", "时间间隔（分）", interval_sendraw_m)

                config.set("Matlab处理及结果发送", "时间间隔（时）", interval_mlab_h)
                config.set("Matlab处理及结果发送", "时间间隔（分）", interval_mlab_m)

                config.write(open(r"%s" % ini_path, "r+"))

            QtWidgets.QMessageBox.information(self, "消息:", "时间配置修改成功！")
            self.signal_station_ini.emit([stationID, [int(interval_sendraw_h), int(interval_sendraw_m)],
                                          [int(interval_mlab_h), int(interval_mlab_m)]])
        except:
            traceback.print_exc()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    time_initialize = QtWidgets.QDialog()
    ui = Ui_station_initialize()
    ui.setupUi(time_initialize)
    time_initialize.show()
    sys.exit(app.exec_())