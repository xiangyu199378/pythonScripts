# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CommonUserLogin.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class CommonUserLogin(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1026, 864)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(390, 110, 231, 101))
        self.label.setObjectName("label")
        self.personinfo = QtWidgets.QPushButton(Form)
        self.personinfo.setGeometry(QtCore.QRect(370, 250, 241, 51))
        self.personinfo.setObjectName("personinfo")
        self.familyinfo = QtWidgets.QPushButton(Form)
        self.familyinfo.setGeometry(QtCore.QRect(370, 330, 241, 51))
        self.familyinfo.setObjectName("familyinfo")
        self.appointment = QtWidgets.QPushButton(Form)
        self.appointment.setGeometry(QtCore.QRect(370, 410, 241, 51))
        self.appointment.setObjectName("appointment")
        self.reaction = QtWidgets.QPushButton(Form)
        self.reaction.setGeometry(QtCore.QRect(370, 490, 241, 51))
        self.reaction.setObjectName("reaction")
        self.quit = QtWidgets.QPushButton(Form)
        self.quit.setGeometry(QtCore.QRect(370, 570, 241, 51))
        self.quit.setObjectName("quit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">欢迎您！</span></p></body></html>"))
        self.personinfo.setText(_translate("Form", "个人信息管理"))
        self.familyinfo.setText(_translate("Form", "家庭信息管理"))
        self.appointment.setText(_translate("Form", "接种预约"))
        self.reaction.setText(_translate("Form", "不良反应反馈"))
        self.quit.setText(_translate("Form", "退出登录"))
