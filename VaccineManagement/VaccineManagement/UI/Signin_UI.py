# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Signin_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SigninWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Form")
        Dialog.resize(881, 877)
        self.signin_confirm = QtWidgets.QPushButton(Dialog)
        self.signin_confirm.setGeometry(QtCore.QRect(310, 800, 111, 51))
        self.signin_confirm.setObjectName("signin_confirm")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(280, 230, 71, 41))
        self.label.setObjectName("label")
        self.signin_password_confirm = QtWidgets.QLineEdit(Dialog)
        self.signin_password_confirm.setGeometry(QtCore.QRect(360, 370, 221, 41))
        self.signin_password_confirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signin_password_confirm.setObjectName("signin_password_confirm")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(600, 300, 101, 41))
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(270, 130, 61, 51))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("../assets/smile1.png"))
        self.label_6.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(340, 120, 251, 61))
        self.label_5.setObjectName("label_5")
        self.signin_return = QtWidgets.QPushButton(Dialog)
        self.signin_return.setGeometry(QtCore.QRect(500, 800, 111, 51))
        self.signin_return.setObjectName("signin_return")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(270, 300, 71, 41))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(230, 370, 111, 41))
        self.label_3.setObjectName("label_3")
        self.signin_ID = QtWidgets.QLineEdit(Dialog)
        self.signin_ID.setGeometry(QtCore.QRect(360, 230, 221, 41))
        self.signin_ID.setObjectName("signin_ID")
        self.signin_password = QtWidgets.QLineEdit(Dialog)
        self.signin_password.setGeometry(QtCore.QRect(360, 300, 221, 41))
        self.signin_password.setAutoFillBackground(False)
        self.signin_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signin_password.setObjectName("signin_password")
        self.name = QtWidgets.QLineEdit(Dialog)
        self.name.setGeometry(QtCore.QRect(360, 440, 221, 41))
        self.name.setObjectName("name")
        self.name_1 = QtWidgets.QLabel(Dialog)
        self.name_1.setGeometry(QtCore.QRect(280, 440, 71, 41))
        self.name_1.setObjectName("name_1")
        self.name_2 = QtWidgets.QLabel(Dialog)
        self.name_2.setGeometry(QtCore.QRect(280, 510, 71, 41))
        self.name_2.setObjectName("name_2")
        self.age = QtWidgets.QLineEdit(Dialog)
        self.age.setGeometry(QtCore.QRect(360, 510, 221, 41))
        self.age.setObjectName("age")
        self.name_3 = QtWidgets.QLabel(Dialog)
        self.name_3.setGeometry(QtCore.QRect(280, 720, 71, 41))
        self.name_3.setObjectName("name_3")
        self.Male = QtWidgets.QRadioButton(Dialog)
        self.Male.setGeometry(QtCore.QRect(370, 730, 115, 19))
        self.Male.setObjectName("Male")
        self.Female = QtWidgets.QRadioButton(Dialog)
        self.Female.setGeometry(QtCore.QRect(510, 730, 115, 19))
        self.Female.setObjectName("Female")
        self.phone = QtWidgets.QLineEdit(Dialog)
        self.phone.setGeometry(QtCore.QRect(360, 580, 221, 41))
        self.phone.setObjectName("phone")
        self.name_4 = QtWidgets.QLabel(Dialog)
        self.name_4.setGeometry(QtCore.QRect(280, 580, 71, 41))
        self.name_4.setObjectName("name_4")
        self.name_5 = QtWidgets.QLabel(Dialog)
        self.name_5.setGeometry(QtCore.QRect(280, 650, 71, 41))
        self.name_5.setObjectName("name_5")
        self.IDCard = QtWidgets.QLineEdit(Dialog)
        self.IDCard.setGeometry(QtCore.QRect(360, 650, 221, 41))
        self.IDCard.setObjectName("IDCard")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.signin_confirm.setText(_translate("Form", "确认"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">账号：</span></p></body></html>"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p>（不小于6位）</p></body></html>"))
        self.label_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">欢迎注册</span></p></body></html>"))
        self.signin_return.setText(_translate("Form", "返回"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">密码：</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">确认密码：</span></p></body></html>"))
        self.name_1.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">姓名：</span></p></body></html>"))
        self.name_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">年龄：</span></p></body></html>"))
        self.name_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">性别：</span></p></body></html>"))
        self.Male.setText(_translate("Form", "男"))
        self.Female.setText(_translate("Form", "女"))
        self.name_4.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">手机号：</span></p></body></html>"))
        self.name_5.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt;\">身份证：</span></p></body></html>"))