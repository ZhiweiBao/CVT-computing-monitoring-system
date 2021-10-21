# -*- coding: utf-8 -*-

import pyodbc
import traceback

class sqlserver(object):

    def __init__(self, serverName='', databaseName='', userName='', password=''):
        self.serverName = serverName
        self.databaseName = databaseName
        self.userName = userName
        self.password = password

    def checkconnect(self):
        try:
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
                         SERVER=self.serverName,
                         DATABASE=self.databaseName,
                         UID=self.userName,
                         PWD=self.password)
            cur = cnxn.cursor()
            cur.close()
            cnxn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def getheaders(self, tableName):
        try:
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
                         SERVER=self.serverName,
                         DATABASE=self.databaseName,
                         UID=self.userName,
                         PWD=self.password)
            cur = cnxn.cursor()
            cmd_write = "SELECT name FROM sys.syscolumns where id=object_id('%s') order by colid" % tableName
            cur.execute(cmd_write)
            rows = cur.fetchall()
            cur.close()
            cnxn.close()
            return rows
        except Exception as e:
            print(e)
            return []

    def getseldata(self, headers, tableName):
        try:
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
                         SERVER=self.serverName,
                         DATABASE=self.databaseName,
                         UID=self.userName,
                         PWD=self.password)
            cur = cnxn.cursor()
            cmd_write = "SELECT top 1000 %s FROM %s order by [GPS时间信号] desc" % (headers, tableName)
            cur.execute(cmd_write)
            rows = cur.fetchall()
            # print(rows)
            cur.close()
            cnxn.close()
            return rows
        except Exception as e:
            print(e)
            return []

    def insertRawData1(self, listall):
        try:
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
                                  SERVER=self.serverName,
                                  DATABASE=self.databaseName,
                                  UID=self.userName,
                                  PWD=self.password)
            # print cnxn
            cur = cnxn.cursor()
            # cmd_write ="SELECT TOP 1000 [id],[name],[score],[age],[height] FROM [test_0].[dbo].[student_info]"
            # cmd_write = "SELECT %s FROM %s " % (headers, self.table)
            # cmd_write = "INSERT INTO [dbo].[pretreatdata] VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
            try:
                # print(listall)
                sql1 = "INSERT INTO [dbo].[cvt01] VALUES (" \
                       "?,?,?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?)"
                sql2 = "INSERT INTO [dbo].[cvt02] VALUES (" \
                       "?,?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?)"
                sql3 = "INSERT INTO [dbo].[cvt03] VALUES (" \
                       "?,?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?)"
                sql4 = "INSERT INTO [dbo].[cvt04] VALUES (" \
                       "?,?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?)"
                sql5 = "INSERT INTO [dbo].[cvt05] VALUES (" \
                       "?,?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?)"
                sql6 = "INSERT INTO [dbo].[cvt06] VALUES (" \
                       "?,?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?)"
                sql7 = "INSERT INTO [dbo].[cvt07] VALUES (" \
                       "?,?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?)"
                sql8 = "INSERT INTO [dbo].[cvt08] VALUES (" \
                       "?,?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?)"
                sql9 = "INSERT INTO [dbo].[cvt09] VALUES (" \
                       "?,?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?)"
                sql10 = "INSERT INTO [dbo].[cvt10] VALUES (" \
                       "?,?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?)"
                sql11 = "INSERT INTO [dbo].[cvt11] VALUES (" \
                       "?,?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?)"
                sql12 = "INSERT INTO [dbo].[cvt12] VALUES (" \
                       "?,?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?," \
                       "?,?,?,?,?)"
                # 批量插入
                cur.executemany(sql1, listall[0])
                cur.executemany(sql2, listall[1])
                cur.executemany(sql3, listall[2])
                cur.executemany(sql4, listall[3])
                cur.executemany(sql5, listall[4])
                cur.executemany(sql6, listall[5])
                cur.executemany(sql7, listall[6])
                cur.executemany(sql8, listall[7])
                cur.executemany(sql9, listall[8])
                cur.executemany(sql10, listall[9])
                cur.executemany(sql11, listall[10])
                cur.executemany(sql12, listall[11])
                cnxn.commit()
            except Exception as e:
                print(e)
                cnxn.rollback()
            cur.close()
            cnxn.close()
            return True
        except Exception as e:
            print(e)
            return False


    def getrawdata(self, date_time):
        try:
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
                         SERVER=self.serverName,
                         DATABASE=self.databaseName,
                         UID=self.userName,
                         PWD=self.password)
            cur = cnxn.cursor()
            sql1 = "SELECT top 1 * FROM [dbo].[cvt01] where [接收时间] >= '%s' order by [接收时间]" % date_time
            sql2 = "SELECT top 1 * FROM [dbo].[cvt02] where [接收时间] >= '%s' order by [接收时间]" % date_time
            sql3 = "SELECT top 1 * FROM [dbo].[cvt03] where [接收时间] >= '%s' order by [接收时间]" % date_time
            sql4 = "SELECT top 1 * FROM [dbo].[cvt04] where [接收时间] >= '%s' order by [接收时间]" % date_time
            sql5 = "SELECT top 1 * FROM [dbo].[cvt05] where [接收时间] >= '%s' order by [接收时间]" % date_time
            sql6 = "SELECT top 1 * FROM [dbo].[cvt06] where [接收时间] >= '%s' order by [接收时间]" % date_time
            sql7 = "SELECT top 1 * FROM [dbo].[cvt07] where [接收时间] >= '%s' order by [接收时间]" % date_time
            sql8 = "SELECT top 1 * FROM [dbo].[cvt08] where [接收时间] >= '%s' order by [接收时间]" % date_time
            sql9 = "SELECT top 1 * FROM [dbo].[cvt09] where [接收时间] >= '%s' order by [接收时间]" % date_time
            sql10 = "SELECT top 1 * FROM [dbo].[cvt10] where [接收时间] >= '%s' order by [接收时间]" % date_time
            sql11 = "SELECT top 1 * FROM [dbo].[cvt11] where [接收时间] >= '%s' order by [接收时间]" % date_time
            sql12 = "SELECT top 1 * FROM [dbo].[cvt12] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql13 = "SELECT top 1 * FROM [dbo].[cvt01] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql14 = "SELECT top 1 * FROM [dbo].[cvt02] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql15 = "SELECT top 1 * FROM [dbo].[cvt03] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql16 = "SELECT top 1 * FROM [dbo].[cvt04] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql17 = "SELECT top 1 * FROM [dbo].[cvt05] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql18 = "SELECT top 1 * FROM [dbo].[cvt06] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql19 = "SELECT top 1 * FROM [dbo].[cvt07] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql20 = "SELECT top 1 * FROM [dbo].[cvt08] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql21 = "SELECT top 1 * FROM [dbo].[cvt09] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql22 = "SELECT top 1 * FROM [dbo].[cvt10] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql23 = "SELECT top 1 * FROM [dbo].[cvt11] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql24 = "SELECT top 1 * FROM [dbo].[cvt12] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # print(sql1)
            # sql13 = "SELECT top 1 * FROM [dbo].[cvt13] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql14 = "SELECT top 1 * FROM [dbo].[cvt14] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql15 = "SELECT top 1 * FROM [dbo].[cvt15] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql16 = "SELECT top 1 * FROM [dbo].[cvt16] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql17 = "SELECT top 1 * FROM [dbo].[cvt17] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql18 = "SELECT top 1 * FROM [dbo].[cvt18] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql19 = "SELECT top 1 * FROM [dbo].[cvt19] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql20 = "SELECT top 1 * FROM [dbo].[cvt20] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql21 = "SELECT top 1 * FROM [dbo].[cvt21] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql22 = "SELECT top 1 * FROM [dbo].[cvt22] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql23 = "SELECT top 1 * FROM [dbo].[cvt23] where [接收时间] >= '%s' order by [接收时间]" % date_time
            # sql24 = "SELECT top 1 * FROM [dbo].[cvt24] where [接收时间] >= '%s' order by [接收时间]" % date_time
            rows = []
            cur.execute(sql1)
            data=cur.fetchall()
            if data != []:
                row = list(data[0])
                row[3] = 'cvt01'+row[3]
                rows.append(row)
            cur.execute(sql2)
            data = cur.fetchall()
            if data != []:
                row = list(data[0])
                row.insert(3, 'cvt02')
                rows.append(row)
            cur.execute(sql3)
            data = cur.fetchall()
            if data != []:
                row = list(data[0])
                row.insert(3, 'cvt03')
                rows.append(row)
            cur.execute(sql4)
            data = cur.fetchall()
            if data != []:
                row = list(data[0])
                row.insert(3, 'cvt04')
                rows.append(row)
            cur.execute(sql5)
            data = cur.fetchall()
            if data != []:
                row = list(data[0])
                row.insert(3, 'cvt05')
                rows.append(row)
            cur.execute(sql6)
            data = cur.fetchall()
            if data != []:
                row = list(data[0])
                row.insert(3, 'cvt06')
                rows.append(row)
            cur.execute(sql7)
            data = cur.fetchall()
            if data != []:
                row = list(data[0])
                row.insert(3, 'cvt07')
                rows.append(row)
            cur.execute(sql8)
            data = cur.fetchall()
            if data != []:
                row = list(data[0])
                row.insert(3, 'cvt08')
                rows.append(row)
            cur.execute(sql9)
            data = cur.fetchall()
            if data != []:
                row = list(data[0])
                row.insert(3, 'cvt09')
                rows.append(row)
            cur.execute(sql10)
            data=cur.fetchall()
            if data != []:
                row = list(data[0])
                row.insert(3, 'cvt10')
                rows.append(row)
            cur.execute(sql11)
            data = cur.fetchall()
            if data != []:
                row = list(data[0])
                row.insert(3, 'cvt11')
                rows.append(row)
            cur.execute(sql12)
            data = cur.fetchall()
            if data != []:
                row = list(data[0])
                row.insert(3, 'cvt12')
                rows.append(row)
            # cur.execute(sql13)
            # data = cur.fetchall()
            # if data != []:
            #     row = list(data[0])
            #     row[2] = 'cvt13' + row[2]
            #     rows.append(row)
            # cur.execute(sql14)
            # data = cur.fetchall()
            # if data != []:
            #     row = list(data[0])
            #     row.insert(2, 'cvt14')
            #     rows.append(row)
            # cur.execute(sql15)
            # data = cur.fetchall()
            # if data != []:
            #     row = list(data[0])
            #     row.insert(2, 'cvt15')
            #     rows.append(row)
            # cur.execute(sql16)
            # data = cur.fetchall()
            # if data != []:
            #     row = list(data[0])
            #     row.insert(2, 'cvt16')
            #     rows.append(row)
            # cur.execute(sql17)
            # data = cur.fetchall()
            # if data != []:
            #     row = list(data[0])
            #     row.insert(2, 'cvt17')
            #     rows.append(row)
            # cur.execute(sql18)
            # data = cur.fetchall()
            # if data != []:
            #     row = list(data[0])
            #     row.insert(2, 'cvt18')
            #     rows.append(row)
            # cur.execute(sql19)
            # data = cur.fetchall()
            # if data != []:
            #     row = list(data[0])
            #     row.insert(2, 'cvt19')
            #     rows.append(row)
            # cur.execute(sql20)
            # data = cur.fetchall()
            # if data != []:
            #     row = list(data[0])
            #     row.insert(2, 'cvt20')
            #     rows.append(row)
            # cur.execute(sql21)
            # data = cur.fetchall()
            # if data != []:
            #     row = list(data[0])
            #     row.insert(2, 'cvt21')
            #     rows.append(row)
            # cur.execute(sql22)
            # data = cur.fetchall()
            # if data != []:
            #     row = list(data[0])
            #     row.insert(2, 'cvt22')
            #     rows.append(row)
            # cur.execute(sql23)
            # data = cur.fetchall()
            # if data != []:
            #     row = list(data[0])
            #     row.insert(2, 'cvt23')
            #     rows.append(row)
            # cur.execute(sql24)
            # data = cur.fetchall()
            # if data != []:
            #     row = list(data[0])
            #     row.insert(2, 'cvt24')
            #     rows.append(row)
            cur.close()
            cnxn.close()
            return rows
        except Exception as e:
            print(e)
            return []

    def insertSampleData(self, sample_data):
        try:
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
                                  SERVER=self.serverName,
                                  DATABASE=self.databaseName,
                                  UID=self.userName,
                                  PWD=self.password)
            # print cnxn
            cur = cnxn.cursor()
            # cmd_write ="SELECT TOP 1000 [id],[name],[score],[age],[height] FROM [test_0].[dbo].[student_info]"
            # cmd_write = "SELECT %s FROM %s " % (headers, self.table)
            # cmd_write = "INSERT INTO [dbo].[pretreatdata] VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
            try:

                sql = "INSERT INTO [dbo].[sample_data] VALUES (" \
                      "?,?,?,?,?,?," \
                      "?,?,?,?,?," \
                      "?,?,?,?,?," \
                      "?,?,?,?,?," \
                      "?,?,?,?,?)"
                cur.executemany(sql, sample_data)
                cnxn.commit()
            except Exception as e:
                print(e)
                cnxn.rollback()
            cur.close()
            cnxn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def get_sample_data(self):
        try:
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
                         SERVER=self.serverName,
                         DATABASE=self.databaseName,
                         UID=self.userName,
                         PWD=self.password)
            cur = cnxn.cursor()
            sql1 = "SELECT top 1 [GPS时间信号],[站号],[采集a基波幅值],[采集b基波幅值],[采集c基波幅值] " \
                   "FROM [dbo].[sample_data] where [信号类型] like 'cvt01%' order by [GPS时间信号] desc"
            sql2 = "SELECT top 1 [采集a基波幅值],[采集b基波幅值],[采集c基波幅值] " \
                   "FROM [dbo].[sample_data] where [信号类型] = 'cvt02' order by [GPS时间信号] desc"
            sql3 = "SELECT top 1 [采集a基波幅值],[采集b基波幅值],[采集c基波幅值] " \
                   "FROM [dbo].[sample_data] where [信号类型] = 'cvt03' order by [GPS时间信号] desc"
            sql4 = "SELECT top 1 [采集a基波幅值],[采集b基波幅值],[采集c基波幅值] " \
                   "FROM [dbo].[sample_data] where [信号类型] = 'cvt04' order by [GPS时间信号] desc"
            sql5 = "SELECT top 1 [采集a基波幅值],[采集b基波幅值],[采集c基波幅值] " \
                   "FROM [dbo].[sample_data] where [信号类型] = 'cvt05' order by [GPS时间信号] desc"
            sql6 = "SELECT top 1 [采集a基波幅值],[采集b基波幅值],[采集c基波幅值] " \
                   "FROM [dbo].[sample_data] where [信号类型] = 'cvt06' order by [GPS时间信号] desc"
            sql7 = "SELECT top 1 [采集a基波幅值],[采集b基波幅值],[采集c基波幅值] " \
                   "FROM [dbo].[sample_data] where [信号类型] = 'cvt07' order by [GPS时间信号] desc"
            sql8 = "SELECT top 1 [采集a基波幅值],[采集b基波幅值],[采集c基波幅值] " \
                   "FROM [dbo].[sample_data] where [信号类型] = 'cvt08' order by [GPS时间信号] desc"
            sql9 = "SELECT top 1 [采集a基波幅值],[采集b基波幅值],[采集c基波幅值] " \
                   "FROM [dbo].[sample_data] where [信号类型] = 'cvt09' order by [GPS时间信号] desc"
            sql10 = "SELECT top 1 [采集a基波幅值],[采集b基波幅值],[采集c基波幅值] " \
                   "FROM [dbo].[sample_data] where [信号类型] = 'cvt10' order by [GPS时间信号] desc"
            sql11 = "SELECT top 1 [采集a基波幅值],[采集b基波幅值],[采集c基波幅值] " \
                   "FROM [dbo].[sample_data] where [信号类型] = 'cvt11' order by [GPS时间信号] desc"
            sql12 = "SELECT top 1 [采集a基波幅值],[采集b基波幅值],[采集c基波幅值] " \
                   "FROM [dbo].[sample_data] where [信号类型] = 'cvt12' order by [GPS时间信号] desc"
            rows = []
            cur.execute(sql1)
            rows.extend(list(cur.fetchall()[0]))
            cur.execute(sql2)
            rows.extend(list(cur.fetchall()[0]))
            cur.execute(sql3)
            rows.extend(list(cur.fetchall()[0]))
            cur.execute(sql4)
            rows.extend(list(cur.fetchall()[0]))
            cur.execute(sql5)
            rows.extend(list(cur.fetchall()[0]))
            cur.execute(sql6)
            rows.extend(list(cur.fetchall()[0]))
            cur.execute(sql7)
            rows.extend(list(cur.fetchall()[0]))
            cur.execute(sql8)
            rows.extend(list(cur.fetchall()[0]))
            cur.execute(sql9)
            rows.extend(list(cur.fetchall()[0]))
            cur.execute(sql10)
            rows.extend(list(cur.fetchall()[0]))
            cur.execute(sql11)
            rows.extend(list(cur.fetchall()[0]))
            cur.execute(sql12)
            rows.extend(list(cur.fetchall()[0]))
            cur.close()
            cnxn.close()
            return rows
        except Exception as e:
            print(e)
            return []

    def insert_mlab_exec_data(self, list_exec):
        try:
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
                                  SERVER=self.serverName,
                                  DATABASE=self.databaseName,
                                  UID=self.userName,
                                  PWD=self.password)
            # print cnxn
            cur = cnxn.cursor()
            # cmd_write ="SELECT TOP 1000 [id],[name],[score],[age],[height] FROM [test_0].[dbo].[student_info]"
            # cmd_write = "SELECT %s FROM %s " % (headers, self.table)
            # cmd_write = "INSERT INTO [dbo].[pretreatdata] VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
            try:

                sql = "INSERT INTO [dbo].[mlab_exec] VALUES (?,?," \
                      "?,?,?,?,?,?,?,?,?,?,?,?," \
                      "?,?,?,?,?,?,?,?,?,?,?,?," \
                      "?,?,?,?,?,?,?,?,?,?,?,?)"
                cur.execute(sql, list_exec)
                cnxn.commit()
            except Exception as e:
                print(e)
                cnxn.rollback()
            cur.close()
            cnxn.close()
            return True
        except Exception as e:
            print(e)
            return False

    def get_mlab_exec_data(self, initial_num):
        try:
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
                                  SERVER=self.serverName,
                                  DATABASE=self.databaseName,
                                  UID=self.userName,
                                  PWD=self.password)
            # print cnxn
            cur = cnxn.cursor()
            sql = "SELECT * FROM [dbo].[mlab_exec] order by [GPS时间信号]"
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            cnxn.close()
            mlab_list = []
            if len(rows) < initial_num:
                for i in range(len(rows)):
                    mlab_list.append(list(rows[i]))
            else:
                for i in range(len(rows) - initial_num, len(rows)):
                    mlab_list.append(list(rows[i]))
            return mlab_list
        except Exception as e:
            print(e)
            return []

    def insertMlabData(self, list_result):
        try:
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
                                  SERVER=self.serverName,
                                  DATABASE=self.databaseName,
                                  UID=self.userName,
                                  PWD=self.password)
            # print cnxn
            cur = cnxn.cursor()
            # cmd_write ="SELECT TOP 1000 [id],[name],[score],[age],[height] FROM [test_0].[dbo].[student_info]"
            # cmd_write = "SELECT %s FROM %s " % (headers, self.table)
            # cmd_write = "INSERT INTO [dbo].[pretreatdata] VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
            try:
                sql_insert = "INSERT INTO [dbo].[mlab_exec] VALUES (?,?," \
                             "?,?,?,?,?,?,?,?,?,?,?,?," \
                             "?,?,?,?,?,?,?,?,?,?,?,?," \
                             "?,?,?,?,?,?,?,?,?,?,?,?)"
                cur.executemany(sql_insert, list_result)
                cnxn.commit()
                flag = True
            except Exception as e:
                print(e)
                flag = False
                cnxn.rollback()
            cur.close()
            cnxn.close()
            return flag
        except:
            traceback.print_exc()
            return False

    def insertResultData(self, list_result, execNum, intial_num):
        try:
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
                                  SERVER=self.serverName,
                                  DATABASE=self.databaseName,
                                  UID=self.userName,
                                  PWD=self.password)
            # print cnxn
            cur = cnxn.cursor()
            # cmd_write ="SELECT TOP 1000 [id],[name],[score],[age],[height] FROM [test_0].[dbo].[student_info]"
            # cmd_write = "SELECT %s FROM %s " % (headers, self.table)
            # cmd_write = "INSERT INTO [dbo].[pretreatdata] VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
            try:
                sql_select = "SELECT * FROM [dbo].[mlab_result]"
                sql_insert = "INSERT INTO [dbo].[mlab_result] VALUES (?,?," \
                             "?,?,?,?,?,?,?,?,?,?,?,?," \
                             "?,?,?,?,?,?,?,?,?,?,?,?," \
                             "?,?,?,?,?,?,?,?,?,?,?,?," \
                             "?,?,?,?,?,?,?,?,?,?,?,?," \
                             "?,?,?,?,?,?,?,?,?,?,?,?," \
                             "?,?,?,?,?,?,?,?,?,?,?,?)"
                cur.execute(sql_select)
                if len(cur.fetchall()) < intial_num:
                    cur.executemany(sql_insert, list_result)
                else:
                    cur.executemany(sql_insert, list_result[-execNum:])
                cnxn.commit()
                flag = True
            except Exception as e:
                print(e)
                flag = False
                cnxn.rollback()
            cur.close()
            cnxn.close()
            return flag
        except:
            traceback.print_exc()
            return False

    def getResultCount(self):
        try:
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
                         SERVER=self.serverName,
                         DATABASE=self.databaseName,
                         UID=self.userName,
                         PWD=self.password)
            cur = cnxn.cursor()
            sql = "SELECT count(1) from [dbo].[mlab_result]"
            cur.execute(sql)
            num = int(cur.fetchall()[0][0])
            cur.close()
            cnxn.close()
            return num
        except:
            traceback.print_exc()
            return 0

    def getInitialResultData(self, initial_num):
        try:
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
                         SERVER=self.serverName,
                         DATABASE=self.databaseName,
                         UID=self.userName,
                         PWD=self.password)
            cur = cnxn.cursor()
            sql = "SELECT top %s * FROM [dbo].[mlab_result] order by [GPS时间信号]" % initial_num
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getResultData(self, execNum):
        try:
            cnxn = pyodbc.connect(DRIVER='{SQL SERVER}',
                         SERVER=self.serverName,
                         DATABASE=self.databaseName,
                         UID=self.userName,
                         PWD=self.password)
            cur = cnxn.cursor()
            sql = "SELECT top %s * FROM [dbo].[mlab_result] order by [GPS时间信号] desc" % execNum
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []


