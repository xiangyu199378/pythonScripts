# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adminAddVaccine.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class AdminAdd(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(673, 488)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(280, 40, 231, 71))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(140, 140, 81, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(140, 190, 81, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(140, 240, 81, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(140, 290, 81, 31))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(120, 340, 101, 31))
        self.label_6.setObjectName("label_6")
        self.vaccineType = QtWidgets.QLineEdit(Dialog)
        self.vaccineType.setGeometry(QtCore.QRect(260, 130, 251, 31))
        self.vaccineType.setObjectName("vaccineType")
        self.vaccineCompany = QtWidgets.QLineEdit(Dialog)
        self.vaccineCompany.setGeometry(QtCore.QRect(260, 190, 251, 31))
        self.vaccineCompany.setObjectName("vaccineCompany")
        self.vaccinePrice = QtWidgets.QLineEdit(Dialog)
        self.vaccinePrice.setGeometry(QtCore.QRect(260, 340, 251, 31))
        self.vaccinePrice.setObjectName("vaccinePrice")
        self.oldMan = QtWidgets.QCheckBox(Dialog)
        self.oldMan.setGeometry(QtCore.QRect(260, 240, 91, 19))
        self.oldMan.setObjectName("oldMan")
        self.youngMan = QtWidgets.QCheckBox(Dialog)
        self.youngMan.setGeometry(QtCore.QRect(360, 240, 91, 19))
        self.youngMan.setObjectName("youngMan")
        self.child = QtWidgets.QCheckBox(Dialog)
        self.child.setGeometry(QtCore.QRect(460, 240, 91, 19))
        self.child.setObjectName("child")
        self.childAge = QtWidgets.QCheckBox(Dialog)
        self.childAge.setGeometry(QtCore.QRect(460, 290, 91, 19))
        self.childAge.setObjectName("childAge")
        self.oldManAge = QtWidgets.QCheckBox(Dialog)
        self.oldManAge.setGeometry(QtCore.QRect(260, 290, 91, 19))
        self.oldManAge.setObjectName("oldManAge")
        self.youngManAge = QtWidgets.QCheckBox(Dialog)
        self.youngManAge.setGeometry(QtCore.QRect(360, 290, 91, 19))
        self.youngManAge.setObjectName("youngManAge")
        self.Yes = QtWidgets.QPushButton(Dialog)
        self.Yes.setGeometry(QtCore.QRect(190, 410, 131, 51))
        self.Yes.setObjectName("Yes")
        self.Quit = QtWidgets.QPushButton(Dialog)
        self.Quit.setGeometry(QtCore.QRect(400, 410, 131, 51))
        self.Quit.setObjectName("Quit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">添加疫苗信息</span></p></body></html>"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:11pt;\">疫苗类型：</span></p></body></html>"))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:11pt;\">疫苗公司：</span></p></body></html>"))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:11pt;\">用户人群：</span></p></body></html>"))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:11pt;\">用户年龄：</span></p></body></html>"))
        self.label_6.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:11pt;\">价格（元）：</span></p></body></html>"))
        self.oldMan.setText(_translate("Dialog", "老人"))
        self.youngMan.setText(_translate("Dialog", "中年"))
        self.child.setText(_translate("Dialog", "儿童"))
        self.childAge.setText(_translate("Dialog", "<18岁"))
        self.oldManAge.setText(_translate("Dialog", ">60岁"))
        self.youngManAge.setText(_translate("Dialog", "18-60岁"))
        self.Yes.setText(_translate("Dialog", "确认"))
        self.Quit.setText(_translate("Dialog", "返回"))
