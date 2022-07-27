from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
from UI.Main_UI import Ui_MainWindow
from UI.Signin_UI import Ui_SigninWindow
from UI.Signin_dialog import SigninError_Dialog, SigninError_Dialog2, SigninError_Dialog3, SigninError_Dialog4, SigninSuccess_Dialog


# 数据库通用操作
def DBS_operation(database, content):
    db = pymysql.connect(host="localhost", user="root", port=3306,
                         password="123456", database=database)
    cursor = db.cursor()
    cursor.execute(content)
    data = cursor.fetchone()
    db.commit()
    db.close()
    return data

# 主界面控制器
class MainControl:
    def __init__(self, ui):
        # 设置信号槽
        self.ui = ui
        ui.login.clicked.connect(self.Login)
        ui.signin.clicked.connect(self.Signin)
        return

    def Login(self):

        return

    def Signin(self):
        # 展示注册子窗口
        SigninWindow.show()
        return

# 注册界面控制器
class SigninControl():
    def __init__(self, ui, wnd):
        # 设置信号槽
        self.wnd = wnd
        self.ui = ui
        ui.signin_confirm.clicked.connect(self.Confirm)
        ui.signin_return.clicked.connect(self.wnd.close)
        return

    def Confirm(self):
        id = self.ui.signin_ID.text()
        password1 = self.ui.signin_password.text()
        password2 = self.ui.signin_password_confirm.text()
        # 输入有空的
        if id == '' or password1 == '' or password2 == '':
            SigninErrorWindow4.show()
            return
        # 身份单选按钮，注册时不需要（因为只用普通用户开放注册），所以暂时去掉这部分代码
        if self.ui.administrator.isChecked():
            role = 'A'
        elif self.ui.hospital.isChecked():
            role = 'B'
        elif self.ui.common_user.isChecked():
            role = 'C'
        else:
            SigninErrorWindow2.show()
            return
        # 两次输入密码不一致，报错提醒
        if password1 != password2:
            # 清空密码框
            self.ui.signin_password.clear()
            self.ui.signin_password_confirm.clear()
            # 显示错误信息
            SigninErrorWindow.show()
            return

        # id没有重复，可以注册
        if self.CheckRepeat() == None:
            content = "INSERT INTO user_info (id, password, role) VALUES ('%s', '%s', '%s');" % (id, password1, role)
            DBS_operation(database='vaccine_info', content=content)
            SigninSuccessWindow.show()
            self.ui.signin_ID.clear()
            self.ui.signin_password.clear()
            self.ui.signin_password_confirm.clear()
            return
        # id重复
        else:
            SigninErrorWindow3.show()
            self.ui.signin_ID.clear()
            return
        return

    def CheckRepeat(self):
        id = self.ui.signin_ID.text()
        content = "SELECT * FROM user_info WHERE  id = '%s';" % id
        data = DBS_operation(database="vaccine_info", content=content)
        return data


if __name__ == '__main__':
    # 连接数据库
    connection = pymysql.connect(host='localhost',
                                 port=3306,
                                 user='root',
                                 password='123456',
                                 db='vaccine_info',
                                 charset='utf8')

    app = QApplication(sys.argv)
    # 实例化主窗口
    MainWindow = QMainWindow()
    MainUI = Ui_MainWindow()
    MainUI.setupUi(MainWindow)
    # 实例化注册子窗口
    SigninWindow = QWidget()
    SigninUI = Ui_SigninWindow()
    SigninUI.setupUi(SigninWindow)
    # 实例化注册dialog（提醒两次输入密码不一致）
    SigninErrorWindow = QDialog()
    SigninErrorUI = SigninError_Dialog()
    SigninErrorUI.setupUi(SigninErrorWindow)
    # 实例化注册dialog（提醒没有选择身份）
    SigninErrorWindow2 = QDialog()
    SigninErrorUI2 = SigninError_Dialog2()
    SigninErrorUI2.setupUi(SigninErrorWindow2)
    # 实例化注册dialog（提醒没有账号重复）
    SigninErrorWindow3 = QDialog()
    SigninErrorUI3 = SigninError_Dialog3()
    SigninErrorUI3.setupUi(SigninErrorWindow3)
    # 实例化注册dialog（提醒没有账号重复）
    SigninErrorWindow4 = QDialog()
    SigninErrorUI4 = SigninError_Dialog4()
    SigninErrorUI4.setupUi(SigninErrorWindow4)
    # 实例化注册dialog（提醒注册成功）
    SigninSuccessWindow = QDialog()
    SigninSuccessUI = SigninSuccess_Dialog()
    SigninSuccessUI.setupUi(SigninSuccessWindow)
    # 实例化控制器
    MainController = MainControl(MainUI)
    SigninController = SigninControl(SigninUI, SigninWindow)

    MainWindow.show()
    sys.exit(app.exec_())
