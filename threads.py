from PyQt5 import QtCore, QtWidgets
import threading
from odbc import odbc_operate
import time
from datetime import datetime, timedelta
import struct
import binascii
import os
import logging
import re
import matlab
import traceback
import mlab_exec
mlab_process = mlab_exec.initialize()


# lock = threading.Lock()

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

class sample_data(QtCore.QThread):
    signal_sendRawData = QtCore.pyqtSignal(list)
    signal_insert_mlab = QtCore.pyqtSignal()
    signal_sample_count = QtCore.pyqtSignal()

    def __int__(self, parent=None):
        super(sample_data, self).__init__(parent)

    def setValue(self, database_info, date_time):
        self.serverName = database_info[0]
        self.dbName = database_info[1]
        self.userName = database_info[2]
        self.password = database_info[3]
        self.datetime = date_time
        # print(database_info)

    def run(self):
        # lock.acquire()
        print('数据采样并发送……')
        db_op = odbc_operate.sqlserver(self.serverName, self.dbName, self.userName, self.password)
        flag = db_op.checkconnect()
        if flag:
            # TODO
            data = db_op.getrawdata(self.datetime)
            # print(self.datetime)
            # data = db_op.getrawdata('2018-06-21 00:00:00')
            # for i in range(len(data)):
            #     print(data[i])
            if data == []:
                print('无数据，采样失败！')

                # lock.release()
                return
        else:
            print("数据库连接失败！")
            # lock.release()
            return

        try:
            '''采样数据存储'''
            sampleData = []
            for i in range(len(data)):
                sampleData.append(data[i][1:])
            n = db_op.insertSampleData(sampleData)
            if n == False:
                print('采样数据存储失败！')
                # lock.release()
                return
        except:
            print('数据采样出错！')
            logger.exception("Exception Logged")
            # lock.release()

        try:
            '''算法预处理'''
            execData = db_op.get_sample_data()
            n = db_op.insert_mlab_exec_data(execData)
            if n == False:
                print('预处理数据存储失败！')
                # lock.release()
                return
            self.signal_insert_mlab.emit()
        except:
            print('算法预处理出错！')
            logger.exception("Exception Logged")
            # lock.release()

        try:
            '''采样数据发送'''
            fildata = []
            fildata.extend(data[0][0:3])
            fildata.append(data[0][3][5:])
            # if len(data) > 12:
            #     fildata.append(data[12][2][4:])
            for i in range(len(data)):
                fildata.extend(data[i][4:])
            for i in range(0, 2):
                # timeStamp = time.mktime(fildata[i].timetuple())
                # fildata[i] = str(datetime.strftime(fildata[i], "%Y-%m-%d %H:%M:%S"))
                fildata[i] = fildata[i].strftime("%Y-%m-%d %H:%M:%S")
            # exec_Time = str(fildata[0][0:4]) + str(fildata[0][5:7]) + str(fildata[0][8:10]) + \
            #             str(fildata[0][11:13]) + str(fildata[0][14:16]) + str(fildata[0][17:])
            gpsTime = str(fildata[1][0:4]) + str(fildata[1][5:7]) + str(fildata[1][8:10]) + \
                      str(fildata[1][11:13]) + str(fildata[1][14:16]) + str(fildata[1][17:])
            binlist = []
            for i in range(4, len(fildata)):
                binstr = struct.pack('!f', fildata[i])
                try:
                    binlist.append(binstr)
                except:
                    logger.exception("Exception Logged")
            hexlist = []
            hexlist.append('aa55aa55')
            # hexlist.append(exec_Time)
            hexlist.append(gpsTime)
            hexlist.append(data[0][2])
            if data[0][3][5:] == '' or data[0][3][5:] == 'GPS时间格式错误':
                hexlist.append('bf')
            elif data[0][3][5:] == '无GPS信号':
                hexlist.append('3f')
            else:
                hexlist.append(data[0][3][5:])

            for i in range(len(binlist)):
                a = binascii.b2a_hex(binlist[i]).decode('ascii')
                pattern = re.compile('.{2,2}')
                hexlist.append(pattern.findall(a))
            for i in range(4, len(hexlist)):
                hexlist[i] = ''.join(hexlist[i])

            hexlist.append('aaffaaff')
            self.signal_sendRawData.emit(hexlist)
            self.signal_sample_count.emit()
            # lock.release()
        except:
            print('原始数据发送失败！')
            logger.exception("Exception Logged")
        #     lock.release()


class mlab_exec(QtCore.QThread):
    signal_mlab_result = QtCore.pyqtSignal()
    signal_sendResultData = QtCore.pyqtSignal(list)
    signal_mlab_count = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(mlab_exec, self).__init__(parent)


    def setValue(self, database_info, execNum, initialNum, pass_num):
        self.serverName = database_info[0]
        self.dbName = database_info[1]
        self.userName = database_info[2]
        self.password = database_info[3]
        self.execNum = execNum
        self.initialNum = initialNum
        self.pass_num = pass_num

    def run(self):
        try:
            db_op = odbc_operate.sqlserver(self.serverName, self.dbName, self.userName, self.password)
            flag = db_op.checkconnect()
            if flag:
                data = db_op.get_mlab_exec_data(self.initialNum)
                matrixdata = []
                for i in range(len(data)):
                    # TODO，算法数据格式
                    matrixdata.append(data[i][2:self.pass_num+2])
                if len(matrixdata) != self.initialNum:
                    print("数据量不足！")
                    return
                elif len(matrixdata[0]) != self.pass_num:
                    print("数据格式不正确！")
                    # self.signal_mlab_result.emit()
                    return
                print('开始计算')
                mlab_result = mlab_process.test4pas2H2L(matlab.double(matrixdata))
                # mlab_result = [[60 for col in range(48)] for row in range(self.initialNum)]
                # TODO
                if mlab_result == []:
                    # self.signal_mlab_result.emit()
                    print("无结果数据！")
                    return
                result = []
                for i in range(len(data)):
                    m_result = []
                    m_result.append(data[i][0])
                    m_result.append(data[i][1])
                    # TODO，算法数据格式
                    m_result.extend(mlab_result[i][:self.pass_num])
                    m_result.extend([0 for k in range(36-self.pass_num)])
                    m_result.extend(mlab_result[i][-self.pass_num:])
                    m_result.extend([0 for k in range(36-self.pass_num)])
                    result.append(m_result)
                result_flag = db_op.insertResultData(result, self.execNum, self.initialNum)
                if result_flag == True:
                    print("计算结束，结果数据存储成功！")
                # self.signal_mlab_result.emit()

                # n = db_op.getResultCount()
                # hexlist = []
                # if n <= self.initialNum:
                #     result_data = db_op.getInitialResultData(self.initialNum)
                #     hexlist.append('aa11aa11')
                # else:
                #     result_data = db_op.getResultData(self.execNum)
                #     hexlist.append('aa33aa33')
                # for i in range(len(result_data)):
                #     result_data[i] = list(result_data[i])
                #     date = str(result_data[i][0])[0:4] + str(result_data[i][0])[5:7] + str(result_data[i][0])[8:10] + \
                #             str(result_data[i][0])[11:13] + str(result_data[i][0])[14:16] + str(result_data[i][0])[17:19]
                #     binlist = []
                #     for j in range(2, len(result_data[i])):
                #         binstr = struct.pack('!f', float(result_data[i][j]))
                #         binlist.append(binstr)
                #     hexlist.append(date)
                #     hexlist.append(result_data[i][1])
                #     for k in range(len(binlist)):
                #         a = binascii.b2a_hex(binlist[k]).decode('ascii')
                #         pattern = re.compile('.{2,2}')
                #         a_list = pattern.findall(a)
                #         hexlist.append(''.join(a_list))
                # if n <= self.initialNum:
                #     hexlist.append('aabbaabb')
                # else:
                #     hexlist.append('aaddaadd')

                # self.signal_sendResultData.emit(hexlist)
                # self.signal_mlab_count.emit()
            else:
                return
        except:
            print("Matlab计算出错!!!")
            logger.exception("Exception Logged")
