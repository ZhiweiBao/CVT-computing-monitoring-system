# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\python3\PyQt\UI_database_setting.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_database_setting(object):
    def setupUi(self, database_setting):
        database_setting.setObjectName("database_setting")
        database_setting.resize(243, 164)
        database_setting.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(database_setting)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_serverName = QtWidgets.QLabel(database_setting)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_serverName.sizePolicy().hasHeightForWidth())
        self.label_serverName.setSizePolicy(sizePolicy)
        self.label_serverName.setObjectName("label_serverName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_serverName)
        self.label_dbName = QtWidgets.QLabel(database_setting)
        self.label_dbName.setObjectName("label_dbName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_dbName)
        self.label_userName = QtWidgets.QLabel(database_setting)
        self.label_userName.setObjectName("label_userName")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_userName)
        self.label_password = QtWidgets.QLabel(database_setting)
        self.label_password.setObjectName("label_password")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_password)
        self.lineEdit_serverName = QtWidgets.QLineEdit(database_setting)
        self.lineEdit_serverName.setObjectName("lineEdit_serverName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_serverName)
        self.lineEdit_dbName = QtWidgets.QLineEdit(database_setting)
        self.lineEdit_dbName.setObjectName("lineEdit_dbName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_dbName)
        self.lineEdit_userName = QtWidgets.QLineEdit(database_setting)
        self.lineEdit_userName.setObjectName("lineEdit_userName")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_userName)
        self.lineEdit_password = QtWidgets.QLineEdit(database_setting)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_password)
        self.pushButton_connect = QtWidgets.QPushButton(database_setting)
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.pushButton_connect)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.retranslateUi(database_setting)
        QtCore.QMetaObject.connectSlotsByName(database_setting)

    def retranslateUi(self, database_setting):
        _translate = QtCore.QCoreApplication.translate
        database_setting.setWindowTitle(_translate("database_setting", "数据库配置"))
        self.label_serverName.setText(_translate("database_setting", "服务器名称"))
        self.label_dbName.setText(_translate("database_setting", "数据库名称"))
        self.label_userName.setText(_translate("database_setting", "用户名"))
        self.label_password.setText(_translate("database_setting", "密码"))
        self.pushButton_connect.setText(_translate("database_setting", "数据库连接"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    database_setting = QtWidgets.QDialog()
    ui = Ui_database_setting()
    ui.setupUi(database_setting)
    database_setting.show()
    sys.exit(app.exec_())

