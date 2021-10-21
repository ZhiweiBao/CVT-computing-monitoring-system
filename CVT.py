# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtCore import Qt, pyqtSlot, QTimer, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from ui.Ui_cvt import Ui_MainWindow
from serial_setting import serial_setting
from database_setting import database_setting
from station_initialize import station_initialize
from odbc import odbc_operate
import threads
import os
import logging
import configparser
from datetime import datetime, timedelta
import traceback


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(Qt.Window)
        self.showMaximized()
        self.setWindowFlags(Qt.WindowStaysOnBottomHint)
        self.database_set = database_setting()

        self.serial_set = serial_setting()
        self.serial_set.signal_open_receive.connect(self.get_serial_setting_open_receive)
        self.serial_set.signal_saveData.connect(self.sampleData)

        self.time_ini = station_initialize()
        self.database_info = []

        self.logger = self.setLogger()

        self.db = QSqlDatabase.addDatabase("QODBC3")

        self.stationID = '0001'
        self.initialNum = 8000
        self.pass_num = 12
        self.pretreatNum = 0
        self.execNum = 0
        self.datetime = ''

        self.currentPath = "D:\CVT"
        ini_path = self.currentPath + "\sample_config.ini"
        ini_exist = os.path.exists(ini_path)
        config = configparser.ConfigParser()
        if ini_exist == 1:
            # ---已存在配置文件，
            try:
                # ---读取当前exist的数值

                config.read_file(open(r"%s" % ini_path))
                self.pretreatNum = int(config.get("计数", "采样计数"))
                self.execNum = int(config.get("计数", "计算计数"))

            except:
                self.logger.exception("Exception Logged")
        else:
            try:
                # -----创建配置文件config.ini---------
                config.add_section("计数")
                config.set("计数", "采样计数", str(self.pretreatNum))
                config.set("计数", "计算计数", str(self.execNum))
                config.write(open(r"%s" % ini_path, "w"))
            except:
                self.logger.exception("Exception Logged")

        self.interval_sendraw_h = None
        self.interval_sendraw_m = None

        self.interval_mlab_h = None
        self.interval_mlab_m = None

        # currentPath = os.getcwd()
        ini_path = self.currentPath + "\database_config.ini"
        ini_exist = os.path.exists(ini_path)
        if ini_exist == 1:
            # ---已存在配置文件，
            try:
                # ---读取当前exist的数值
                config = configparser.ConfigParser()
                config.read_file(open(r"%s" % ini_path))
                serverName = config.get("数据库信息", "服务器名称")
                dbName = config.get("数据库信息", "数据库名称")
                userName = config.get("数据库信息", "用户名")
                password = config.get("数据库信息", "密码")
                self.database_info = [serverName, dbName, userName, password]
                dsn = "DRIVER={SQL SERVER};SERVER=%s;DATABASE=%s" % (self.database_info[0], self.database_info[1])
                self.db.setDatabaseName(dsn)
                self.db.setUserName(self.database_info[2])
                self.db.setPassword(self.database_info[3])
                self.refreshTable()
            except:
                self.logger.exception("Exception Logged")

        # currentPath = os.getcwd()
        ini_path = self.currentPath + "\station_config.ini"
        ini_exist = os.path.exists(ini_path)
        if ini_exist == 1:
            # ---已存在配置文件，
            try:
                # ---读取当前exist的数值
                config = configparser.ConfigParser()
                config.read_file(open(r"%s" % ini_path))

                self.stationID = str(config.get("站点信息", "站号"))

                self.interval_sendraw_h = int(config.get("原始数据发送", "时间间隔（时）"))
                self.interval_sendraw_m = int(config.get("原始数据发送", "时间间隔（分）"))

                self.interval_mlab_h = int(config.get("Matlab处理及结果发送", "时间间隔（时）"))
                self.interval_mlab_m = int(config.get("Matlab处理及结果发送", "时间间隔（分）"))
            except:
                self.logger.exception("Exception Logged")

        try:
            if len(self.database_info) == 4 \
                    and self.interval_sendraw_h != None and self.interval_sendraw_m != None \
                    and self.interval_mlab_h != None and self.interval_mlab_m != None\
                    and self.serial_set.comboBox_comName_receive1.currentText() != '' \
                    and self.serial_set.comboBox_comName_send.currentText() != '':
                db_op = odbc_operate.sqlserver(self.database_info[0], self.database_info[1], self.database_info[2],
                                               self.database_info[3])
                flag = db_op.checkconnect()
                if flag:
                    self.serial_set.set_database(self.database_info, self.stationID)
                    self.serial_set.on_pushButton_open_receive_clicked()
                    self.serial_set.on_pushButton_open_send_clicked()
                else:
                    QtWidgets.QMessageBox.warning(self, "Warning:", "数据库连接失败！")
                    return
            else:

                QtWidgets.QMessageBox.warning(self, "Warning:", "请先完成1.数据库连接；2.时间配置；3.串口设置！")
        except:
            self.logger.exception("Exception Logged")

    def setLogger(self):
        # 创建一个logger,可以考虑如何将它封装
        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(os.path.join(os.getcwd(), 'log.txt'))
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)

        # 记录一条日志
        logger.info('hello world, i\'m log helper in python, may i help you')

        return logger

    @pyqtSlot()
    def on_pushButton_database_setting_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            self.database_set.setWindowFlags(Qt.Dialog)
            self.database_set.show()

            self.database_set.signal_connect.connect(self.get_database_setting)
        except:
            self.logger.exception("Exception Logged")

    def get_database_setting(self, database_setting):
        try:
            self.database_info = database_setting
            # self.db.setHostName(self.database_info[0])
            self.serial_set.set_database(self.database_info, self.stationID)
            dsn = "DRIVER={SQL SERVER};SERVER=%s;DATABASE=%s" % (self.database_info[0], self.database_info[1])
            self.db.setDatabaseName(dsn)
            self.db.setUserName(self.database_info[2])
            self.db.setPassword(self.database_info[3])
            self.refreshTable()
        except:
            self.logger.exception("Exception Logged")

    def refreshTable(self):
        try:
            self.db.open()
            tablelist = self.db.tables()
            # print(tablelist)
            self.comboBox_tableName.clear()
            for i in range(len(tablelist)-2):
                self.comboBox_tableName.addItem(tablelist[i])
            self.db.close()
        except:
            self.logger.exception("Exception Logged")

    @pyqtSlot()
    def on_pushButton_time_ini_clicked(self):
        try:
            self.time_ini.setWindowFlags(Qt.Dialog)
            self.time_ini.show()

            self.time_ini.signal_station_ini.connect(self.get_station_ini_setting)
        except:
            self.logger.exception("Exception Logged")

    def get_station_ini_setting(self, time_info):
        try:
            self.stationID = str(time_info[0])

            self.interval_sendraw_h = int(time_info[1][0])
            self.interval_sendraw_m = int(time_info[1][1])

            self.interval_mlab_h = int(time_info[2][0])
            self.interval_mlab_m = int(time_info[2][1])
            self.pretreatNum = 0
            self.execNum = self.initialNum
            execNum = int(timedelta(hours=self.interval_mlab_h, minutes=self.interval_mlab_m) /
                          timedelta(hours=self.interval_sendraw_h, minutes=self.interval_sendraw_m))
            while True:
                if self.execNum >= execNum:
                    self.execNum = self.execNum - execNum
                elif self.execNum > 0 and self.execNum < execNum:
                    self.execNum = 0 - self.execNum
                else:
                    break
        except:
            self.logger.exception("Exception Logged")


    @pyqtSlot()
    def on_pushButton_serial_setting_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            if self.database_info == []:
                QtWidgets.QMessageBox.warning(self, "Warning:", "请先完成数据库连接！")
                return
            db_op = odbc_operate.sqlserver(self.database_info[0], self.database_info[1], self.database_info[2], self.database_info[3])
            flag = db_op.checkconnect()
            if flag:
                pass
            else:
                QtWidgets.QMessageBox.warning(self, "Warning:", "数据库连接失败！")
                return
            if self.interval_sendraw_h == None or self.interval_sendraw_m == None:
                QtWidgets.QMessageBox.warning(self, "Warning:", "请先进行发送数据时间配置！")
                return
            if self.interval_mlab_h == None or self.interval_mlab_m == None:
                QtWidgets.QMessageBox.warning(self, "Warning:", "请先进行Matlab处理时间配置！")
                return
            self.serial_set.setWindowFlags(Qt.Dialog)
            self.serial_set.show()
        except:
            self.logger.exception("Exception Logged")


        # self.serial_set.signal_open_send.connect(self.get_serial_setting_open_send)
        # self.serial_set.signal_close_send.connect(self.serial_setting_close_send)
        # self.serial_set.signal_receiveData.connect(self.get_serial_data)

    def get_serial_setting_open_receive(self, serial_setting):
        try:
            print('接收'+serial_setting[0] +'打开，波特率：' + str(serial_setting[1]))
            self.datetime = serial_setting[2]
            print(self.datetime)
            # print('正在接收……')
        except:
            self.logger.exception("Exception Logged")


    @pyqtSlot()
    def on_pushButton_select_clicked(self):
        self.pushButton_select.setDisabled(True)
        if self.database_info == []:
            QtWidgets.QMessageBox.warning(self, "Warning:", "请先完成数据库连接！")
            self.pushButton_select.setDisabled(False)
            return
        db_op = odbc_operate.sqlserver(self.database_info[0], self.database_info[1], self.database_info[2],
                                       self.database_info[3])
        flag = db_op.checkconnect()
        try:
            if flag:
                headers = db_op.getheaders(self.comboBox_tableName.currentText())
                # print(headers)
                str_cmd = ""
                for i in range(len(headers)):
                    str_cmd = str_cmd + "[" + headers[i][0] + "],"
                # print(str_cmd)
                # data    = db_op.getalldata()
                data = db_op.getseldata(str_cmd[:len(str_cmd) - 1], self.comboBox_tableName.currentText())
            else:
                QtWidgets.QMessageBox.warning(self, "Warning:", "数据库连接失败！")
                self.pushButton_select.setDisabled(False)
                return
            self.tableWidget_db_data.setColumnCount(len(headers))  # 设置表格的列数
            self.tableWidget_db_data.setRowCount(len(data))  # 设置表格的行数
            # ---------set headers--------
            for i in range(len(headers)):
                self.tableWidget_db_data.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(
                    "%s" % headers[i][0]))
            # ---------set datas----------
            for i in range(len(data)):
                for j in range(len(data[0])):
                    item0 = QtWidgets.QTableWidgetItem("%s" % data[i][j])
                    # item0 = QtGui.QTableWidgetItem("%s" % data[i][j].decode('gbk'))
                    item0.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    # -------禁止修改已写入的数据！！！-------
                    item0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_db_data.setItem(i, j, item0)
            self.tableWidget_db_data.resizeColumnsToContents()
        except:
            self.logger.exception("Exception Logged")
        self.pushButton_select.setDisabled(False)

    @pyqtSlot()
    def on_pushButton_test_clicked(self):
        # self.pushButton_test.setEnabled(False)
        try:
            if self.database_info == []:
                QtWidgets.QMessageBox.warning(self, "Warning:", "请先完成数据库连接！")
                self.pushButton_test.setEnabled(True)
                return
            if self.interval_sendraw_h == None or self.interval_sendraw_m == None:
                QtWidgets.QMessageBox.warning(self, "Warning:", "请先进行发送数据时间配置！")
                return
            if self.interval_mlab_h == None or self.interval_mlab_m == None:
                QtWidgets.QMessageBox.warning(self, "Warning:", "请先进行Matlab处理时间配置！")
                return

            execNum = int(timedelta(hours=int(self.interval_mlab_h), minutes=int(self.interval_mlab_m)) /
                          timedelta(hours=int(self.interval_sendraw_h), minutes=int(self.interval_sendraw_m)))

            db_op = odbc_operate.sqlserver(self.database_info[0], self.database_info[1], self.database_info[2],
                                           self.database_info[3])
            flag = db_op.checkconnect()
            if flag:
                # self.sampleThreads = threads.sample_data()
                # self.sampleThreads.setValue(self.database_info, '2019-02-26 18:07:18')
                # # self.sampleThreads.signal_insert_mlab.connect(self.mlab_exec)
                # self.sampleThreads.signal_sendRawData.connect(self.serial_set.sendData)
                # self.sampleThreads.start()

                self.mlabExecThraed = threads.mlab_exec()
                self.mlabExecThraed.setValue(self.database_info, execNum, self.initialNum, self.pass_num)
                self.mlabExecThraed.signal_mlab_result.connect(self.mlab_end)
                self.mlabExecThraed.signal_sendResultData.connect(self.serial_set.sendData)
                self.mlabExecThraed.start()
            else:
                QtWidgets.QMessageBox.warning(self, "Warning:", "数据库连接失败！")
                self.pushButton_test.setEnabled(True)
                return
        except:
            self.logger.exception("Exception Logged")

    @pyqtSlot()
    def sampleData(self):
        try:
            self.pretreatNum += 1
            # print(self.pretreatNum)
            # currentPath = os.getcwd()
            ini_path = self.currentPath + "\sample_config.ini"
            ini_exist = os.path.exists(ini_path)
            config = configparser.ConfigParser()

            pretreatNum = int(timedelta(hours=self.interval_sendraw_h, minutes=self.interval_sendraw_m) / timedelta(seconds=10))
            print('采样：%s/%s' % (self.pretreatNum, pretreatNum))
            if self.pretreatNum >= pretreatNum:
                self.pretreatNum = self.pretreatNum - pretreatNum
                if ini_exist == 1:
                    # ---已存在配置文件，
                    try:
                        # ---读取当前exist的数值
                        config.read(r"%s" % ini_path)
                        config.set("计数", "采样计数", str(self.pretreatNum))
                        config.write(open(r"%s" % ini_path, "w"))
                    except:
                        self.logger.exception("Exception Logged")
                else:
                    try:
                        # -----创建配置文件config.ini---------
                        config.add_section("计数")
                        config.set("计数", "采样计数", str(self.pretreatNum))
                        config.set("计数", "计算计数", str(self.execNum))
                        config.write(open(r"%s" % ini_path, "w"))
                    except:
                        self.logger.exception("Exception Logged")
            else:
                if ini_exist == 1:
                    # ---已存在配置文件，
                    try:
                        # ---读取当前exist的数值
                        config.read(r"%s" % ini_path)
                        config.set("计数", "采样计数", str(self.pretreatNum))
                        config.write(open(r"%s" % ini_path, "w"))
                    except:
                        self.logger.exception("Exception Logged")
                else:
                    try:
                        # -----创建配置文件config.ini---------
                        config.add_section("计数")
                        config.set("计数", "采样计数", str(self.pretreatNum))
                        config.set("计数", "计算计数", str(self.execNum))
                        config.write(open(r"%s" % ini_path, "w"))
                    except:
                        self.logger.exception("Exception Logged")
                return


            db_op = odbc_operate.sqlserver(self.database_info[0], self.database_info[1], self.database_info[2],
                                           self.database_info[3])
            flag = db_op.checkconnect()
            if flag:
                self.sampleThreads = threads.sample_data()
                print(self.datetime)
                self.sampleThreads.setValue(self.database_info, self.datetime)
                self.sampleThreads.signal_insert_mlab.connect(self.mlab_exec)
                # TODO
                self.sampleThreads.signal_sendRawData.connect(self.serial_set.sendData)
                # self.sampleThreads.signal_sendRawData.connect(self.sample_count)
                self.sampleThreads.start()
                dt = datetime.strptime(self.datetime, "%Y-%m-%d %H:%M:%S")
                self.datetime = str(dt + timedelta(hours=int(self.interval_sendraw_h), minutes=int(self.interval_sendraw_m)))

            else:
                QtWidgets.QMessageBox.warning(self, "Warning:", "数据库连接失败！")
                return
        except:
            self.logger.exception("Exception Logged")

    @pyqtSlot()
    def mlab_exec(self):
        try:
            self.execNum += 1
            # print(self.execNum)
            # currentPath = os.getcwd()
            ini_path = self.currentPath + "\sample_config.ini"
            ini_exist = os.path.exists(ini_path)
            config = configparser.ConfigParser()

            execNum = int(timedelta(hours=int(self.interval_mlab_h), minutes=int(self.interval_mlab_m))/
                          timedelta(hours=int(self.interval_sendraw_h), minutes=int(self.interval_sendraw_m)))
            print('计算：%s/%s' % (self.execNum, execNum))
            if self.execNum >= execNum:
                self.execNum = self.execNum - execNum
                if ini_exist == 1:
                    # ---已存在配置文件，
                    try:
                        # ---读取当前exist的数值
                        config.read(r"%s" % ini_path)
                        config.set("计数", "计算计数", str(self.execNum))
                        config.write(open(r"%s" % ini_path, "w"))

                    except:
                        self.logger.exception("Exception Logged")
                else:
                    try:
                        # -----创建配置文件config.ini---------
                        config.add_section("计数")
                        config.set("计数", "采样计数", str(self.pretreatNum))
                        config.set("计数", "计算计数", str(self.execNum))
                        config.write(open(r"%s" % ini_path, "w"))
                    except:
                        self.logger.exception("Exception Logged")
            else:
                if ini_exist == 1:
                    # ---已存在配置文件，
                    try:
                        # ---读取当前exist的数值
                        config.read(r"%s" % ini_path)
                        config.set("计数", "计算计数", str(self.execNum))
                        config.write(open(r"%s" % ini_path, "w"))

                    except:
                        self.logger.exception("Exception Logged")
                else:
                    try:
                        # -----创建配置文件config.ini---------
                        config.add_section("计数")
                        config.set("计数", "采样计数", str(self.pretreatNum))
                        config.set("计数", "计算计数", str(self.execNum))
                        config.write(open(r"%s" % ini_path, "w"))
                    except:
                        self.logger.exception("Exception Logged")
                return



            db_op = odbc_operate.sqlserver(self.database_info[0], self.database_info[1], self.database_info[2],
                                           self.database_info[3])
            flag = db_op.checkconnect()
            if flag:
                self.mlabExecThraed = threads.mlab_exec()
                self.mlabExecThraed.setValue(self.database_info, execNum, self.initialNum, self.pass_num)
                self.mlabExecThraed.signal_sendResultData.connect(self.serial_set.sendData)
                # self.mlabExecThraed.signal_mlab_count(self.mlab_count)
                self.mlabExecThraed.start()
            else:
                QtWidgets.QMessageBox.warning(self, "Warning:", "数据库连接失败！")
                # self.pushButton_mlab_exec.setDisabled(False)
                return
        except:
            self.logger.exception("Exception Logged")

    def mlab_end(self):
        self.pushButton_test.setEnabled(True)


    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               "本程序",
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.Cancel,
                                               QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            self.db.close()
            self.serial_set.close()
            self.database_set.close()
            self.time_ini.close()
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())