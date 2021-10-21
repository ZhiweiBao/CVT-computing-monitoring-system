# -*- coding: utf-8 -*-

"""
Module implementing serial_setting.
"""
import binascii
import re
import struct
from odbc import odbc_operate
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QTimer
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from ui.Ui_serial_setting import Ui_serial_setting
import time
from datetime import datetime, timedelta
import os
import logging
import configparser
import traceback


def setLogger():
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

logger = setLogger()

class serial_setting(QDialog, Ui_serial_setting):
    """
    Class documentation goes here.
    """
    signal_open_receive = pyqtSignal(list)
    # signal_open_send = pyqtSignal(list)
    # signal_close_send = pyqtSignal()
    signal_processData1 = pyqtSignal()
    # signal_processData2 = pyqtSignal()
    signal_receiveData1 = pyqtSignal(list)
    # signal_receiveData2 = pyqtSignal(list)
    signal_saveData = pyqtSignal()

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(serial_setting, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(Qt.Dialog)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.com_receive1 = QSerialPort()
        # self.com_receive2 = QSerialPort()
        self.comboBox_Baudrate_receive.addItems(('9600', '19200', '115200', '250000', '1000000'))
        self.comboBox_Baudrate_receive.setCurrentText('115200')
        self.pushButton_close_receive.setEnabled(False)
        self.on_pushButton_refresh_receive_clicked()
        self.com_receive1.readyRead.connect(self.receiveData1)
        # self.com_receive2.readyRead.connect(self.receiveData2)

        self.com_send = QSerialPort()
        self.comboBox_Baudrate_send.addItems(('9600', '19200', '115200', '250000', '1000000'))
        self.comboBox_Baudrate_send.setCurrentText('115200')
        self.pushButton_close_send.setEnabled(False)
        self.on_pushButton_refresh_send_clicked()

        self.hexdata1 = []
        # self.hexdata2 = []
        self.signal_processData1.connect(self.processData1)
        # self.signal_processData2.connect(self.processData2)
        self.signal_receiveData1.connect(self.get_serial_data1)
        # self.signal_receiveData2.connect(self.get_serial_data2)
        self.list1 = []
        self.list2 = []
        self.list3 = []
        self.list4 = []
        self.list5 = []
        self.list6 = []
        self.list7 = []
        self.list8 = []
        self.list9 = []
        self.list10 = []
        self.list11 = []
        self.list12 = []

        # currentPath = os.getcwd()
        self.currentPath = "D:\CVT"
        ini_path = self.currentPath + "\com_config.ini"
        ini_exist = os.path.exists(ini_path)
        if ini_exist == 1:
            # ---已存在配置文件，
            try:
                # ---读取当前exist的数值
                config = configparser.ConfigParser()
                config.read_file(open(r"%s" % ini_path))
                com_name_receive = config.get("串口信息", "接收串口号")
                com_name_send = config.get("串口信息", "发送串口号")
                Baudrate = config.get("串口信息", "波特率")
                self.comboBox_comName_receive1.setCurrentText(com_name_receive)
                self.comboBox_comName_send.setCurrentText(com_name_send)
                self.comboBox_Baudrate_receive.setCurrentText(Baudrate)
                self.comboBox_Baudrate_send.setCurrentText(Baudrate)
            except:
                traceback.print_exc()


        # self.sendTimer = QTimer()
        # self.sendTimer.timeout.connect(self.sendData)

    def set_database(self, database_info, stationID):
        self.database_info = database_info
        self.stationID = stationID

    @pyqtSlot()
    def on_pushButton_open_receive_clicked(self):
        """
        打开串口
        """
        if self.com_send.isOpen() and self.comboBox_comName_receive1.currentText() == self.comboBox_comName_send.currentText():
            QMessageBox.warning(self, "警告:", "串口号已被占用或串口号相同！")
            return


        comName1 = self.comboBox_comName_receive1.currentText()
        comBaud = int(self.comboBox_Baudrate_receive.currentText())

        # currentPath = os.getcwd()
        ini_path = self.currentPath + "\com_config.ini"
        ini_exist = os.path.exists(ini_path)
        # ---if database_config is not exist created it-------
        config = configparser.ConfigParser()
        if ini_exist == 0:
            try:
                # -----创建配置文件config.ini---------
                config.add_section("串口信息")
                config.set("串口信息", "接收串口号", comName1)
                config.set("串口信息", "发送串口号", self.comboBox_comName_send.currentText())
                config.set("串口信息", "波特率", str(comBaud))
                config.write(open(r"%s" % ini_path, "w"))
            except Exception as e:
                print(e)
        else:
            # -----改写exiest的数值
            config.read(r"%s" % ini_path)
            config.set("串口信息", "接收串口号", comName1)
            config.set("串口信息", "波特率", str(comBaud))
            config.write(open(r"%s" % ini_path, "r+"))

        if comName1 == '':
            QMessageBox.warning(self, "警告:", "未选择串口号！")
            return
        self.com_receive1.setPortName(comName1)

        try:
            if self.com_receive1.open(QSerialPort.ReadWrite) == False:
                QMessageBox.critical(self, '严重错误', '串口打开失败')
                return
            else:
                dt_now = str(datetime.now())
                self.datetime = dt_now[0:14] + '00:00'
        except:
            QMessageBox.critical(self, '严重错误', '串口打开失败')
            return
        

        self.com_receive1.setBaudRate(comBaud)

        # if self.timerSendCheck.isChecked():
        # self.sendTimer.start(int(1000))

        self.pushButton_open_receive.setEnabled(False)
        self.pushButton_close_receive.setEnabled(True)
        self.comboBox_comName_receive1.setEnabled(False)
        # self.comboBox_comName_receive2.setEnabled(False)
        self.comboBox_Baudrate_receive.setEnabled(False)
        # self.sendButton.setEnabled(True)
        self.pushButton_refresh_receive.setEnabled(False)

        # self.comStatus.setText('串口状态：%s  打开   波特率 %s' % (comName, comBaud))
        self.signal_open_receive.emit([comName1, comBaud, self.datetime])
        # self.signal_open_receive.emit([comName1, '', comBaud])

    @pyqtSlot()
    def on_pushButton_open_send_clicked(self):
        """
        打开串口
        """
        try:
            if (self.com_receive1.isOpen() and self.comboBox_comName_send.currentText() == self.comboBox_comName_receive1.currentText()):
                QMessageBox.warning(self, "警告:", "串口号已被占用！")
                return
            comName = self.comboBox_comName_send.currentText()
            comBaud = int(self.comboBox_Baudrate_send.currentText())

            # currentPath = os.getcwd()
            ini_path = self.currentPath + "\com_config.ini"
            ini_exist = os.path.exists(ini_path)
            # ---if database_config is not exist created it-------
            config = configparser.ConfigParser()
            if ini_exist == 0:
                try:
                    # -----创建配置文件config.ini---------
                    config.add_section("串口信息")
                    config.set("串口信息", "接收串口号", self.comboBox_comName_receive1)
                    config.set("串口信息", "发送串口号", comName)
                    config.set("串口信息", "波特率", str(comBaud))
                    config.write(open(r"%s" % ini_path, "w"))
                except Exception as e:
                    print(e)
            else:
                # -----改写exiest的数值
                config.read(r"%s" % ini_path)
                config.set("串口信息", "发送串口号", comName)
                config.set("串口信息", "波特率", str(comBaud))
                config.write(open(r"%s" % ini_path, "r+"))

            if comName == '':
                QMessageBox.warning(self, "警告:", "未选择串口号！")
                return
            self.com_send.setPortName(comName)

            try:
                if self.com_send.open(QSerialPort.ReadWrite) == False:
                    QMessageBox.critical(self, '严重错误', '串口打开失败')
                    return
            except:
                QMessageBox.critical(self, '严重错误', '串口打开失败')
                return

            self.com_send.setBaudRate(comBaud)
            # if self.timerSendCheck.isChecked():
            # self.sendTimer.start(int(1000))

            self.pushButton_open_send.setEnabled(False)
            self.pushButton_close_send.setEnabled(True)
            self.comboBox_comName_send.setEnabled(False)
            self.comboBox_Baudrate_send.setEnabled(False)
            # self.sendButton.setEnabled(True)
            self.pushButton_refresh_send.setEnabled(False)
            # self.comStatus.setText('串口状态：%s  打开   波特率 %s' % (comName, comBaud))
            # self.signal_open_send.emit([comName, comBaud])
        except:
            traceback.print_exc()

    @pyqtSlot()
    def on_pushButton_close_receive_clicked(self):
        """
        关闭串口
        """
        self.com_receive1.close()
        # self.com_receive2.close()
        self.pushButton_open_receive.setEnabled(True)
        self.pushButton_close_receive.setEnabled(False)
        self.comboBox_comName_receive1.setEnabled(True)
        # self.comboBox_comName_receive2.setEnabled(True)
        self.comboBox_Baudrate_receive.setEnabled(True)
        # self.sendButton.setEnabled(False)
        self.pushButton_refresh_receive.setEnabled(True)
        # self.comStatus.setText('串口状态：%s  关闭' % self.com.portName())
        # if self.sendTimer.isActive():
        #     self.sendTimer.stop()

    @pyqtSlot()
    def on_pushButton_close_send_clicked(self):
        """
        关闭串口
        """
        # self.signal_close_send.emit()
        self.com_send.close()
        self.pushButton_open_send.setEnabled(True)
        self.pushButton_close_send.setEnabled(False)
        self.comboBox_comName_send.setEnabled(True)
        self.comboBox_Baudrate_send.setEnabled(True)
        # self.sendButton.setEnabled(False)
        self.pushButton_refresh_send.setEnabled(True)
        # self.comStatus.setText('串口状态：%s  关闭' % self.com.portName())
        # if self.sendTimer.isActive():
        #     self.sendTimer.stop()

    @pyqtSlot()
    def on_pushButton_refresh_receive_clicked(self):
        """
        刷新串口号
        """
        self.comboBox_comName_receive1.clear()
        # self.comboBox_comName_receive2.clear()
        com = QSerialPort()
        for info in QSerialPortInfo.availablePorts():
            com.setPort(info)
            if com.open(QSerialPort.ReadWrite):
                self.comboBox_comName_receive1.addItem(info.portName())
                # self.comboBox_comName_receive2.addItem(info.portName())
                com.close()

    @pyqtSlot()
    def on_pushButton_refresh_send_clicked(self):
        """
        刷新串口号
        """
        self.comboBox_comName_send.clear()
        com = QSerialPort()
        for info in QSerialPortInfo.availablePorts():
            com.setPort(info)
            if com.open(QSerialPort.ReadWrite):
                self.comboBox_comName_send.addItem(info.portName())
                com.close()

    def receiveData1(self):
        try:
            '''将串口接收到的QByteArray格式数据转为bytes'''
            receivedData = bytes(self.com_receive1.readAll())
            if len(receivedData) > 0:
                # self.receiveCount += len(receivedData)
                # if self.stopShowingButton.text() == '停止显示':
                #     if self.hexShowingCheck.isChecked() == False:
                #         receivedData = receivedData.decode(self.encoding, 'ignore')
                #         print(receivedData)
                #         self.receivedDataEdit.insertPlainText(receivedData)
                #     else:
                # print(receivedData)
                data = binascii.b2a_hex(receivedData).decode('ascii')
                pattern = re.compile('.{2,2}')
                # print(pattern.findall(data))
                hexStr = ' '.join(pattern.findall(data))
                # print(hexStr)
                # hexdata = hexStr.split()
                # print(hexdata)
                # print(hexStr)
                self.hexdata1.extend(hexStr.split())
                # print(self.hexdata)
                self.signal_processData1.emit()
            else:
                return
        except:
            QMessageBox.critical(self, '严重错误', '串口接收数据错误')

    def processData1(self):
        # if len(self.hexdata) >= 1144:
        #     p = self.hexdata.index('aa')
        #     print(p)
        try:
            if len(self.hexdata1) >= 1144\
                    and self.hexdata1[0:4] == ['aa', '55', 'aa', '55']\
                    and self.hexdata1[1140:1144] == ['aa', 'ff', 'aa', 'ff']:
                result = self.hex2num(self.hexdata1)
                self.signal_receiveData1.emit(result)
                del(self.hexdata1[0:1144])
            elif len(self.hexdata1) >= 1144\
                    and (self.hexdata1[0:4] != ['aa', '55', 'aa', '55']
                         or self.hexdata1[1140:1144] != ['aa', 'ff', 'aa', 'ff']):
                del(self.hexdata1[0])
                try:
                    aa = self.hexdata1.index('aa')
                    del(self.hexdata1[:aa])
                except:
                    raise Exception
            else:
                return
        except:
            logger.exception("Exception Logged")

    def hex2num(self, para):
        list1 = []
        list2 = []
        list3 = []
        list4 = []
        list5 = []
        list6 = []
        list7 = []
        list8 = []
        list9 = []
        list10 = []
        list11 = []
        list12 = []
        localtime = datetime.now()
        # localtime = datetime.now()
        # gpsTime = ''.join(para[9:11]) + '-' + ''.join(para[8]) + '-' + ''.join(para[7]) + ' ' + \
        #           ''.join(para[4]) + ':' + ''.join(para[5]) + ':' + ''.join(para[6])
        list1.append(localtime)
        if para[11] == 'bf' or para[11] == 'BF' or para[11] == 'bF' or para[11] == 'Bf':
            try:
                gpsTime = datetime(int(''.join(para[9:11])), int(para[8]), int(para[7]), int(para[4]), int(para[5]),
                                   int(para[6]))
                beijingTime = gpsTime + timedelta(hours=8)
                # timeStamp = time.mktime(bjTime.timetuple())
                # beijingTime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeStamp)))
                list1.append(beijingTime)
                list1.append(self.stationID)
                list1.append('')
                # list1.append(para[11])
            except:
                beijingTime = localtime
                list1.append(beijingTime)
                list1.append(self.stationID)
                list1.append('GPS时间格式错误')
                # list1.append(para[11])
        elif para[11] == '3f' or para[11] == '3F':
            beijingTime = localtime
            list1.append(beijingTime)
            list1.append(self.stationID)
            list1.append('无GPS信号')
            # list1.append(para[11])
        else:
            beijingTime = localtime
            list1.append(beijingTime)
            list1.append(self.stationID)
            list1.append(para[11])
            # list1.append(str(bin(int(para[11], 16))))
        list2.append(localtime)
        list2.append(beijingTime)
        list3.append(localtime)
        list3.append(beijingTime)
        list4.append(localtime)
        list4.append(beijingTime)
        list5.append(localtime)
        list5.append(beijingTime)
        list6.append(localtime)
        list6.append(beijingTime)
        list7.append(localtime)
        list7.append(beijingTime)
        list8.append(localtime)
        list8.append(beijingTime)
        list9.append(localtime)
        list9.append(beijingTime)
        list10.append(localtime)
        list10.append(beijingTime)
        list11.append(localtime)
        list11.append(beijingTime)
        list12.append(localtime)
        list12.append(beijingTime)

        list2.append(self.stationID)
        list3.append(self.stationID)
        list4.append(self.stationID)
        list5.append(self.stationID)
        list6.append(self.stationID)
        list7.append(self.stationID)
        list8.append(self.stationID)
        list9.append(self.stationID)
        list10.append(self.stationID)
        list11.append(self.stationID)
        list12.append(self.stationID)


        for i in range((3 + 47 * 0 + 0) * 4, (3 + 47 * 0 + 23) * 4, 4):
            b = ''.join(para[i:i + 4])
            hexstr = bytes.fromhex(b)
            data = struct.unpack('!f', hexstr)[0]
            list1.append(data)
        for i in range((3 + 47 * 0 + 23) * 4, (3 + 47 * 0 + 46) * 4, 4):
            b = ''.join(para[i:i + 4])
            hexstr = bytes.fromhex(b)
            data = struct.unpack('!f', hexstr)[0]
            list2.append(data)
        for i in range((3 + 47 * 1 + 0) * 4, (3 + 47 * 1 + 23) * 4, 4):
            b = ''.join(para[i:i + 4])
            hexstr = bytes.fromhex(b)
            data = struct.unpack('!f', hexstr)[0]
            list3.append(data)
        for i in range((3 + 47 * 1 + 23) * 4, (3 + 47 * 1 + 46) * 4, 4):
            b = ''.join(para[i:i + 4])
            hexstr = bytes.fromhex(b)
            data = struct.unpack('!f', hexstr)[0]
            list4.append(data)
        for i in range((3 + 47 * 2 + 0) * 4, (3 + 47 * 2 + 23) * 4, 4):
            b = ''.join(para[i:i + 4])
            hexstr = bytes.fromhex(b)
            data = struct.unpack('!f', hexstr)[0]
            list5.append(data)
        for i in range((3 + 47 * 2 + 23) * 4, (3 + 47 * 2 + 46) * 4, 4):
            b = ''.join(para[i:i + 4])
            hexstr = bytes.fromhex(b)
            data = struct.unpack('!f', hexstr)[0]
            list6.append(data)
        for i in range((3 + 47 * 3 + 0) * 4, (3 + 47 * 3 + 23) * 4, 4):
            b = ''.join(para[i:i + 4])
            hexstr = bytes.fromhex(b)
            data = struct.unpack('!f', hexstr)[0]
            list7.append(data)
        for i in range((3 + 47 * 3+ 23) * 4, (3 + 47 * 3 + 46) * 4, 4):
            b = ''.join(para[i:i + 4])
            hexstr = bytes.fromhex(b)
            data = struct.unpack('!f', hexstr)[0]
            list8.append(data)
        for i in range((3 + 47 * 4 + 0) * 4, (3 + 47 * 4 + 23) * 4, 4):
            b = ''.join(para[i:i + 4])
            hexstr = bytes.fromhex(b)
            data = struct.unpack('!f', hexstr)[0]
            list9.append(data)
        for i in range((3 + 47 * 4 + 23) * 4, (3 + 47 * 4 + 46) * 4, 4):
            b = ''.join(para[i:i + 4])
            hexstr = bytes.fromhex(b)
            data = struct.unpack('!f', hexstr)[0]
            list10.append(data)
        for i in range((3 + 47 * 5 + 0) * 4, (3 + 47 * 5 + 23) * 4, 4):
            b = ''.join(para[i:i + 4])
            hexstr = bytes.fromhex(b)
            data = struct.unpack('!f', hexstr)[0]
            list11.append(data)
        for i in range((3 + 47 * 5 + 23) * 4, (3 + 47 * 5 + 46) * 4, 4):
            b = ''.join(para[i:i + 4])
            hexstr = bytes.fromhex(b)
            data = struct.unpack('!f', hexstr)[0]
            list12.append(data)
        listall = [tuple(list1), tuple(list2), tuple(list3), tuple(list4), tuple(list5), tuple(list6),
                   tuple(list7), tuple(list8), tuple(list9), tuple(list10), tuple(list11), tuple(list12)]
        return listall

    def get_serial_data1(self, serial_data):
        self.list1.append(serial_data[0])
        self.list2.append(serial_data[1])
        self.list3.append(serial_data[2])
        self.list4.append(serial_data[3])
        self.list5.append(serial_data[4])
        self.list6.append(serial_data[5])
        self.list7.append(serial_data[6])
        self.list8.append(serial_data[7])
        self.list9.append(serial_data[8])
        self.list10.append(serial_data[9])
        self.list11.append(serial_data[10])
        self.list12.append(serial_data[11])
        comName1 = self.comboBox_comName_receive1.currentText()
        print('串口%s正在接收……' % comName1)
        try:
            if len(self.list1) >= 10 and len(self.list2) >= 10 and len(self.list3) >= 10 \
                    and len(self.list4) >= 10 and len(self.list5) >= 10 and len(self.list6) >= 10 \
                    and len(self.list7) >= 10 and len(self.list8) >= 10 and len(self.list9) >= 10 \
                    and len(self.list10) >= 10 and len(self.list11) >= 10 and len(self.list12) >= 10:
                listall = [self.list1, self.list2, self.list3, self.list4, self.list5, self.list6,
                           self.list7, self.list8, self.list9, self.list10, self.list11, self.list12]
                # print(listall)
                self.saveData1(listall)
                print('已存入！')
                del self.list1[0:10]
                del self.list2[0:10]
                del self.list3[0:10]
                del self.list4[0:10]
                del self.list5[0:10]
                del self.list6[0:10]
                del self.list7[0:10]
                del self.list8[0:10]
                del self.list9[0:10]
                del self.list10[0:10]
                del self.list11[0:10]
                del self.list12[0:10]
                self.signal_saveData.emit()
        except:
            print("存入失败")
            traceback.print_exc()

    def saveData1(self, data):
        try:
            serverName = self.database_info[0]
            dbName = self.database_info[1]
            userName = self.database_info[2]
            password = self.database_info[3]
            if len(serverName) != 0 and len(dbName) != 0 and len(userName) != 0 and len(password) != 0:
                pass
            else:
                QMessageBox.warning(self, "Warning:", "请录入完整的数据库信息！")
                return
            db_op = odbc_operate.sqlserver(serverName, dbName, userName, password)
            flag = db_op.checkconnect()
            if flag:
                db_op.insertRawData1(data)
            else:
                QMessageBox.warning(self, "Warning:", "数据库连接失败！")
                # self.saveTimer.stop()
                return
        except:
            print("连接失败")
            logger.exception("Exception Logged")

    def sendData(self, data):
        # data = ' '.join(txData)
        # print(data)
        try:
            if len(data) == 0:
                return
            s = ''.join(data)
            # s = s.upper()
            # print(s)
            if len(s) % 2 == 1:  # 如果16进制不是偶数个字符,去掉最后一个
                QMessageBox.critical(self, '错误', '十六进制数不是偶数个')
                return
            #             pattern = re.compile('[^0-9a-fA-F]')
            #             r = pattern.findall(s)
            #             if len(r) != 0:
            #                 QMessageBox.critical(self, '错误', '包含非十六进制数')
            #                 return

            if not s.isalnum():
                QMessageBox.critical(self, '错误', '包含非十六进制数')
                return
        except:
            traceback.print_exc()

        try:
            hexData = binascii.a2b_hex(s)
            # print(hexData)
        except:
            QMessageBox.critical(self, '错误', '转换编码错误')
            return

        try:
            n = self.com_send.write(hexData)
            # print(n)
            if n == -1:
                print("串口发送数据失败！")
        except:
            QMessageBox.critical(self, '异常', '十六进制发送错误')
            return
