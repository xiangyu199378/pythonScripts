from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
import pymysql
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
from UI.Main_UI import Ui_MainWindow
from UI.Signin_UI import Ui_SigninWindow
from UI.Signin_dialog import SigninError_Dialog, SigninError_Dialog2, SigninError_Dialog3, SigninError_Dialog4, SigninSuccess_Dialog
from UI.Login_dialog import LoginError_Dialog1, LoginError_Dialog2, LoginError_Dialog3
from UI.CommonUser import CommonUserLogin
from UI.Commonuser_Info import CommonuserInfo, Commonuser_Alter, CommonuserBook, BookInfo, BookCancelInfo, CommonuserBadReaction, ReactionInfo
from UI.HomeInfo import HomeInfoManage, DelInfo
from UI.admin import AdminLogin, AdminVaccineManage, AdminAdd, AdminHospital, AdminAddHospital, AdminError1, AdminError2, AdminError3, AddSuccess
from UI.Hospital import Hospital, HospitalInfo, FixSuccess, HospitalBook, AddSuccess, DelSuccess, HospitalError1, Inoculate, HospitalUserInfo, HospitalBadReaction

# 把目前登录的用户id作为全局变量
ID = ''
HomeFlag = False  # 若为True则表明正在添加家庭信息

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
# 返回多条元组
def DBS_operation2(database, content):
    db = pymysql.connect(host="localhost", user="root", port=3306,
                         password="123456", database=database)
    cursor = db.cursor()
    cursor.execute(content)
    data = cursor.fetchall()
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
        global ID
        ID = self.ui.ID.text()
        password = self.ui.password.text()
        # 若输入为空
        if ID == '' or password == '':
            self.ui.ID.clear()
            self.ui.password.clear()
            LoginErrorWindow1.show()
            return

        content = "SELECT password FROM user_info WHERE  id = '%s';" % ID
        data = DBS_operation(database="vaccine_info", content=content)
        # 若还未注册
        if data == None:
            self.ui.ID.clear()
            self.ui.password.clear()
            LoginErrorWindow2.show()
            return
        data = data[0]
        # 若密码错误
        if data != password:
            self.ui.ID.clear()
            self.ui.password.clear()
            LoginErrorWindow3.show()
            return

        # 密码正确
        content = "SELECT role FROM user_info WHERE  id = '%s';" % ID
        role = DBS_operation(database="vaccine_info", content=content)
        role = role[0]
        self.ui.ID.clear()
        self.ui.password.clear()

        if role == 'A':
            # 管理员操作
            AdminLoginWindow.exec()
            pass
        elif role == 'B':
            # 医院操作
            HospitalWindow.exec()
            pass
        elif role == 'C':
            # 普通用户操作
            CommonUserWindow.show()
        return

    def Signin(self):
        # 展示注册子窗口
        SigninWindow.exec()
        return

# 注册界面控制器
class SigninControl():
    def __init__(self, ui, wnd):
        # 设置信号槽
        self.wnd = wnd
        self.ui = ui
        ui.signin_confirm.clicked.connect(self.Confirm)
        ui.signin_return.clicked.connect(self.Return)
        return

    def Confirm(self):
        loginid = self.ui.signin_ID.text()
        password1 = self.ui.signin_password.text()
        password2 = self.ui.signin_password_confirm.text()
        name = self.ui.name.text()
        age = self.ui.age.text()
        phone = self.ui.phone.text()
        IDCard = self.ui.IDCard.text()

        if self.ui.Male.isChecked():
            sex = 'M'
        else:
            sex = 'F'

        # 输入有空的
        if loginid == '' or password1 == '' or password2 == '' or name == '' or age == '' or sex == '' or IDCard == '':
            SigninErrorWindow4.show()
            return

        # 密码小于6位
        if len(password1) < 6:
            self.ui.signin_password.clear()
            self.ui.signin_password_confirm.clear()
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

        # loginid没有重复，可以注册
        if self.CheckRepeat() == None:
            global HomeFlag, ID
            # print("现在的ID是：", ID)
            # role：A->管理员 B->医院 C->普通用户，只有普通用户才能开放注册
            role = 'C'
            content = "INSERT INTO user_info (id, password, role) VALUES ('%s', '%s', '%s');" % (loginid, password1, role)
            DBS_operation(database='vaccine_info', content=content)
            # 把用户信息加入commonuser_info表格中，方便用户管理个人信息
            if HomeFlag and ID != '':
                HomeFlag = False
                content = "SELECT family_code FROM commonuser_info WHERE  id = '%s';" % ID
                fcode = DBS_operation(database="vaccine_info", content=content)
                fcode = fcode[0]
                content = "INSERT INTO commonuser_info (id, family_code, age, sex, name, phone, IDCard) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
                loginid, fcode, age, sex, name, phone, IDCard)
                DBS_operation(database='vaccine_info', content=content)
            else:
                content = "INSERT INTO commonuser_info (id, age, sex, name, phone, IDCard) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (
                loginid, age, sex, name, phone, IDCard)
                DBS_operation(database='vaccine_info', content=content)

            SigninSuccessWindow.show()
            self.ui.signin_ID.clear()
            self.ui.signin_password.clear()
            self.ui.signin_password_confirm.clear()
            self.ui.name.clear()
            self.ui.age.clear()
            self.ui.phone.clear()
            self.ui.IDCard.clear()

            return
        # id重复
        else:
            SigninErrorWindow3.show()
            self.ui.signin_ID.clear()
            return
        return

    def CheckRepeat(self):
        checkid = self.ui.signin_ID.text()
        content = "SELECT * FROM user_info WHERE  id = '%s';" % checkid
        data = DBS_operation(database="vaccine_info", content=content)
        return data

    def Return(self):
        self.ui.signin_ID.clear()
        self.ui.signin_password.clear()
        self.ui.signin_password_confirm.clear()
        self.wnd.close()
        return

# 普通用户界面控制器
class CommonUserControl():
    def __init__(self, ui, wnd):
        # 设置信号槽
        self.wnd = wnd
        self.ui = ui

        ui.personinfo.clicked.connect(self.PersonInfo)
        ui.familyinfo.clicked.connect(self.FamilyInfo)
        ui.appointment.clicked.connect(self.Book)
        ui.reaction.clicked.connect(self.Reaction)
        ui.quit.clicked.connect(self.wnd.close)
        return

    # 个人信息管理 槽函数
    def PersonInfo(self):
        global ID
        content = "SELECT * FROM commonuser_info WHERE  id = '%s';" % ID
        info = DBS_operation(database="vaccine_info", content=content)
        self.cid = 'none' if info[0] == None else info[0]
        self.cname = 'none' if info[1] == None else info[1]
        self.chomeid = 'none' if info[2] == None else info[2]
        self.cage = 'none' if info[3] == None else str(info[3])
        self.csex = 'none' if info[4] == None else info[4]
        self.cphone = 'none' if info[5] == None else info[5]
        self.cIDCard = 'none' if info[6] == None else info[6]

        # 实例化 普通用户个人信息管理
        # 注意，在子窗口中再打开子窗口不要用QWidget而要用QDialog
        # 逻辑：在 个人信息管理 中可以查看个人信息（Dialog），以及修改个人信息（Dialog）
        CommonuserInfoWindow = QDialog()
        CommonUserInfoUI = CommonuserInfo(cid=self.cid, cname=self.cname,
                                          csex=self.csex, cage=self.cage,
                                          chomeid=self.chomeid, cphone=self.cphone,
                                          cIDCard=self.cIDCard)
        CommonUserInfoUI.setupUi(CommonuserInfoWindow)
        # 实例化 个人信息修改 控制器
        CuserInfoAlterController = CuserInfoAlterControl(CommonUserInfoUI, CommonuserInfoWindow)
        CommonuserInfoWindow.exec()
        return

    # 家庭信息管理 槽函数
    def FamilyInfo(self):
        global ID
        # 找出该用户的家庭编号
        content = "SELECT family_code FROM commonuser_info WHERE  id = '%s';" % ID
        fcode = DBS_operation(database="vaccine_info", content=content)
        #print(fcode, type(fcode))
        # 搜索出所有该家庭编号的成员(除了该用户)
        if fcode[0] != None:
            fcode = fcode[0]
            content = "SELECT name,age,sex,phone,IDCard FROM commonuser_info WHERE  family_code = '%s' AND id != '%s';" % (fcode,ID)
            family_info = DBS_operation2(database="vaccine_info", content=content)
            #print(family_info)
        else:
            family_info = None
        #print(len(family_info), family_info[0], family_info[0][1])
        HomeInfoWindow = QDialog()
        HomeInfoUI = HomeInfoManage(family_info)  # 显示家庭信息
        HomeInfoUI.setupUi(HomeInfoWindow)
        # 实例化 家庭信息管理 控制器
        FamilyInfoController = FamilyInfoControl(HomeInfoUI, HomeInfoWindow)
        HomeInfoWindow.exec()

    # 接种预约 槽函数
    def Book(self):
        CommonuserBookWindow.exec()

    # 不良反应反馈 槽函数
    def Reaction(self):
        CommonuserBadReactionWindow.exec()


# 普通用户 家庭信息管理 控制器
class FamilyInfoControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.add1.clicked.connect(self.Add1)
        ui.add2.clicked.connect(self.Add2)
        ui.add3.clicked.connect(self.Add3)
        ui.add4.clicked.connect(self.Add4)
        ui.del1.clicked.connect(self.Del1)
        ui.del2.clicked.connect(self.Del2)
        ui.del3.clicked.connect(self.Del3)
        ui.del4.clicked.connect(self.Del4)
        ui.alter.clicked.connect(self.wnd.close)
        ui.quit.clicked.connect(self.wnd.close)
    # 修改家庭成员信息槽函数
    def Add1(self):
        global HomeFlag
        HomeFlag = True
        SigninWindow.exec()
        return
    def Add2(self):
        global HomeFlag
        HomeFlag = True
        SigninWindow.exec()
        return

    def Add3(self):
        global HomeFlag
        HomeFlag = True
        SigninWindow.exec()
        return

    def Add4(self):
        global HomeFlag
        HomeFlag = True
        SigninWindow.exec()
        return

    def Del1(self):
        global ID
        content = "SELECT family_code FROM commonuser_info WHERE  id = '%s';" % ID
        fcode = DBS_operation(database="vaccine_info", content=content)
        fcode = fcode[0]
        name = self.ui.family_info
        name = name[0][0]
        content = "SELECT id FROM commonuser_info WHERE name = '%s' and family_code = '%s';" % (name, fcode)
        delid = DBS_operation(database="vaccine_info", content=content)
        delid = delid[0]
        #print(fcode, name, delid)
        # 删除commonuser_info 和 user_info中的对应用户信息
        content = "DELETE FROM commonuser_info WHERE name = '%s' and family_code = '%s';" % (name, fcode)
        DBS_operation(database="vaccine_info", content=content)
        content = "DELETE FROM user_info WHERE id = '%s';" % (delid)
        DBS_operation(database="vaccine_info", content=content)
        HomeInfoDelWindow.exec()
        return

    def Del2(self):
        global ID
        content = "SELECT family_code FROM commonuser_info WHERE  id = '%s';" % ID
        fcode = DBS_operation(database="vaccine_info", content=content)
        fcode = fcode[0]
        name = self.ui.family_info
        name = name[1][0]
        content = "SELECT id FROM commonuser_info WHERE name = '%s' and family_code = '%s';" % (name, fcode)
        delid = DBS_operation(database="vaccine_info", content=content)
        delid = delid[0]
        # print(fcode, name, delid)
        # 删除commonuser_info 和 user_info中的对应用户信息
        content = "DELETE FROM commonuser_info WHERE name = '%s' and family_code = '%s';" % (name, fcode)
        DBS_operation(database="vaccine_info", content=content)
        content = "DELETE FROM user_info WHERE id = '%s';" % (delid)
        DBS_operation(database="vaccine_info", content=content)
        HomeInfoDelWindow.exec()
        return

    def Del3(self):
        global ID
        content = "SELECT family_code FROM commonuser_info WHERE  id = '%s';" % ID
        fcode = DBS_operation(database="vaccine_info", content=content)
        fcode = fcode[0]
        name = self.ui.family_info
        name = name[2][0]
        content = "SELECT id FROM commonuser_info WHERE name = '%s' and family_code = '%s';" % (name, fcode)
        delid = DBS_operation(database="vaccine_info", content=content)
        delid = delid[0]
        # print(fcode, name, delid)
        # 删除commonuser_info 和 user_info中的对应用户信息
        content = "DELETE FROM commonuser_info WHERE name = '%s' and family_code = '%s';" % (name, fcode)
        DBS_operation(database="vaccine_info", content=content)
        content = "DELETE FROM user_info WHERE id = '%s';" % (delid)
        DBS_operation(database="vaccine_info", content=content)
        HomeInfoDelWindow.exec()
        return

    def Del4(self):
        global ID
        content = "SELECT family_code FROM commonuser_info WHERE  id = '%s';" % ID
        fcode = DBS_operation(database="vaccine_info", content=content)
        fcode = fcode[0]
        name = self.ui.family_info
        name = name[3][0]
        content = "SELECT id FROM commonuser_info WHERE name = '%s' and family_code = '%s';" % (name, fcode)
        delid = DBS_operation(database="vaccine_info", content=content)
        delid = delid[0]
        # print(fcode, name, delid)
        # 删除commonuser_info 和 user_info中的对应用户信息
        content = "DELETE FROM commonuser_info WHERE name = '%s' and family_code = '%s';" % (name, fcode)
        DBS_operation(database="vaccine_info", content=content)
        content = "DELETE FROM user_info WHERE id = '%s';" % (delid)
        DBS_operation(database="vaccine_info", content=content)
        HomeInfoDelWindow.exec()
        return

#####################   以下是 个人信息修改 部分   ####################################
# 普通用户 个人信息修改 控制器
class CuserInfoAlterControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.alter.clicked.connect(self.AlterInfo)
        ui.quit.clicked.connect(self.wnd.close)

    def AlterInfo(self):
        global ID
        content = "SELECT * FROM commonuser_info WHERE  id = '%s';" % ID
        data = DBS_operation(database="vaccine_info", content=content)
        self.cid, self.cIDCard = data[0], data[6]
        CommonuserInfoAlterWindow = QDialog()
        CommonUserInfoAlterUI = Commonuser_Alter(cid=self.cid, cIDCard=self.cIDCard)
        CommonUserInfoAlterUI.setupUi(CommonuserInfoAlterWindow)
        # 实例化 控制器
        CommonUserAlterController = CommonUserAlterControl(CommonUserInfoAlterUI, CommonuserInfoAlterWindow)
        CommonuserInfoAlterWindow.exec()
        return

class CommonUserAlterControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.Yes.clicked.connect(self.Yes)
        ui.Quit.clicked.connect(self.wnd.close)
        return

    def Yes(self):
        global ID
        self.newName = self.ui.Name.text()
        self.newAge = self.ui.Age.text()
        self.newSex = 'M' if self.ui.Sex.text()=='男' else 'F'
        self.newFamily_code = self.ui.Homeid.text()
        self.newPhone = self.ui.Phone.text()
        content = "UPDATE commonuser_info SET name='%s', age='%s', sex='%s', family_code='%s', phone='%s' WHERE id='%s';" % (self.newName, self.newAge, self.newSex, self.newFamily_code, self.newPhone, ID)
        DBS_operation(database="vaccine_info", content=content)
        self.wnd.close()

# 普通用户 预约接种 控制器
class CommonuserBookControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.yes.clicked.connect(self.Yes)
        ui.cancel.clicked.connect(self.Cancel)
        ui.quit.clicked.connect(self.wnd.close)
        return

    def Yes(self):
        global ID
        year = self.ui.year.text()
        month = self.ui.month.text()
        day = self.ui.day.text()
        time = year + '-' + month + '-' + day
        content = "UPDATE commonuser_info SET is_book='%s',book_time='%s' WHERE id='%s';" % ('Y', time, ID)
        DBS_operation(database='vaccine_info', content=content)
        BookInfoWindow.exec()

    def Cancel(self):
        global ID
        content = "UPDATE commonuser_info SET is_book='%s',book_time='%s' WHERE id='%s';" % ('N', '没预约', ID)
        DBS_operation(database='vaccine_info', content=content)
        BookCancelInfoWindow.exec()

# 普通用户 不良信息反馈 槽函数
class CommonuserReactionControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.yes.clicked.connect(self.Yes)
        ui.quit.clicked.connect(self.wnd.close)
        return

    def Yes(self):
        global ID
        reaction = self.ui.bad_reaction.toPlainText()
        content = "UPDATE commonuser_info SET is_bad_reaction='%s',what_bad_reaction='%s' WHERE id='%s';" % ('Y', reaction, ID)
        DBS_operation(database='vaccine_info', content=content)
        self.ui.bad_reaction.clear()
        ReactionInfoWindow.exec()
        return

# 管理员 登录界面 控制器
class AdminLoginControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.vaccineInfo.clicked.connect(self.VaccineManage)
        ui.addHospital.clicked.connect(self.HospitalManage)
        ui.quit.clicked.connect(self.wnd.close)
        return

    # 疫苗信息管理 槽函数
    def VaccineManage(self):
        content = "SELECT * FROM vaccines_info;"
        info = DBS_operation2(database='vaccine_info', content=content)
        #print(info, type(info), len(info))
        # 实例化 管理员 疫苗信息管理 子窗口
        AdminVaccineManageWindow = QDialog()
        AdminVaccineManageUI = AdminVaccineManage(info)
        AdminVaccineManageUI.setupUi(AdminVaccineManageWindow)
        # 实例化控制器
        AdminVaccineController = AdminVaccineControl(AdminVaccineManageUI, AdminVaccineManageWindow)

        AdminVaccineManageWindow.exec()
        return

    # 社区医院管理 槽函数
    def HospitalManage(self):
        content = "SELECT * FROM hospital_info;"
        info = DBS_operation2(database='vaccine_info', content=content)
        # 实例化 管理员 管理社区医院 子窗口
        AdminHospitalWindow = QDialog()
        AdminHospitalUI = AdminHospital(info)
        AdminHospitalUI.setupUi(AdminHospitalWindow)
        # 实例化 社区医院管理 控制器
        AdminHospitalController = AdminHospitalControl(AdminHospitalUI, AdminHospitalWindow)

        AdminHospitalWindow.exec()
        return

# 管理员 管理疫苗信息 控制器
class AdminVaccineControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.add.clicked.connect(self.Add)
        ui.quit.clicked.connect(self.wnd.close)
        ui.del1.clicked.connect(self.Del1)
        ui.del2.clicked.connect(self.Del2)
        ui.del3.clicked.connect(self.Del3)
        ui.del4.clicked.connect(self.Del4)
        ui.del5.clicked.connect(self.Del5)
        ui.del6.clicked.connect(self.Del6)
        ui.del7.clicked.connect(self.Del7)
        ui.del8.clicked.connect(self.Del8)
        return

    def Add(self):
        AdminAddWindow.exec()
        return

    def Del1(self):
        name = self.ui.vaccine1_type.text()
        content = "DELETE FROM vaccines_info WHERE type = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del2(self):
        name = self.ui.vaccine2_type.text()
        content = "DELETE FROM vaccines_info WHERE type = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del3(self):
        name = self.ui.vaccine3_type.text()
        content = "DELETE FROM vaccines_info WHERE type = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del4(self):
        name = self.ui.vaccine4_type.text()
        content = "DELETE FROM vaccines_info WHERE type = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del5(self):
        name = self.ui.vaccine5_type.text()
        content = "DELETE FROM vaccines_info WHERE type = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del6(self):
        name = self.ui.vaccine6_type.text()
        content = "DELETE FROM vaccines_info WHERE type = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del7(self):
        name = self.ui.vaccine7_type.text()
        content = "DELETE FROM vaccines_info WHERE type = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del8(self):
        name = self.ui.vaccine8_type.text()
        content = "DELETE FROM vaccines_info WHERE type = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

# 管理员 添加疫苗信息 控制器
class AdminAddControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.Yes.clicked.connect(self.Add)
        ui.Quit.clicked.connect(self.wnd.close)
        return

    def Add(self):
        vtype = self.ui.vaccineType.text()
        vcompany = self.ui.vaccineCompany.text()
        vuser = ''
        if self.ui.oldMan.isChecked():
            vuser = vuser + '老人 '
        if self.ui.youngMan.isChecked():
            vuser = vuser + '青年 '
        if self.ui.child.isChecked():
            vuser = vuser + '小孩'
        vage = ''
        if self.ui.oldManAge.isChecked():
            vage = '>60岁'
        elif self.ui.youngManAge.isChecked():
            vage = '18-60岁'
        elif self.ui.childAge.isChecked():
            vage ='<18岁'
        vprice = self.ui.vaccinePrice.text()
        #print(vtype, vcompany, vuser, vage, vprice, type(vcompany))
        # 把数据写入数据库，并添加提示
        content = "INSERT INTO vaccines_info (type, company, user_type, user_age, price) VALUES ('%s', '%s', '%s', '%s', '%s');" % (vtype, vcompany, vuser, vage, vprice)
        DBS_operation(database='vaccine_info', content=content)
        self.ui.vaccineType.clear()
        self.ui.vaccineCompany.clear()
        self.ui.vaccinePrice.clear()

        SigninSuccessWindow.exec()

        return

# 管理员 社区医院管理 控制器
class AdminHospitalControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.Add.clicked.connect(self.Add)
        ui.Quit.clicked.connect(self.wnd.close)
        ui.Del1.clicked.connect(self.Del1)
        ui.Del2.clicked.connect(self.Del2)
        ui.Del3.clicked.connect(self.Del3)
        ui.Del4.clicked.connect(self.Del4)
        ui.Del5.clicked.connect(self.Del5)
        ui.Del6.clicked.connect(self.Del6)
        ui.Del7.clicked.connect(self.Del7)
        ui.Del8.clicked.connect(self.Del8)
        ui.Del9.clicked.connect(self.Del9)
        ui.Del10.clicked.connect(self.Del10)
        return

    # 添加社区医院槽函数
    def Add(self):
        AdminAddHospitalWindow.exec()
        return

    # 删除医院信息
    def Del1(self):
        name = self.ui.label_3.text()
        name = name.split('>')[5][:-6]
        # 获取医院对应id
        content = "SELECT id FROM hospital_info WHERE name = '%s';" % name
        id = DBS_operation(database='vaccine_info', content=content)
        # 删除hospital_info对应信息
        content = "DELETE FROM hospital_info WHERE name = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        # 删除user_info对应信息
        content = "DELETE FROM user_info WHERE id = '%s';" % id
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del2(self):
        name = self.ui.label_4.text()
        name = name.split('>')[5][:-6]
        content = "DELETE FROM hospital_info WHERE name = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del3(self):
        name = self.ui.label_5.text()
        name = name.split('>')[5][:-6]
        content = "DELETE FROM hospital_info WHERE name = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del4(self):
        name = self.ui.label_6.text()
        name = name.split('>')[5][:-6]
        content = "DELETE FROM hospital_info WHERE name = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del5(self):
        name = self.ui.label_10.text()
        name = name.split('>')[5][:-6]
        content = "DELETE FROM hospital_info WHERE name = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del6(self):
        name = self.ui.label_9.text()
        name = name.split('>')[5][:-6]
        content = "DELETE FROM hospital_info WHERE name = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del7(self):
        name = self.ui.label_8.text()
        name = name.split('>')[5][:-6]
        content = "DELETE FROM hospital_info WHERE name = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del8(self):
        name = self.ui.label_7.text()
        name = name.split('>')[5][:-6]
        content = "DELETE FROM hospital_info WHERE name = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del9(self):
        name = self.ui.label_11.text()
        name = name.split('>')[5][:-6]
        content = "DELETE FROM hospital_info WHERE name = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

    def Del10(self):
        name = self.ui.label_12.text()
        name = name.split('>')[5][:-6]
        content = "DELETE FROM hospital_info WHERE name = '%s';" % name
        DBS_operation(database='vaccine_info', content=content)
        HomeInfoDelWindow.exec()
        return

# 管理员 添加社区医院 控制器
class AdminAddHospitalControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.Yes.clicked.connect(self.Yes)
        ui.Quit.clicked.connect(self.wnd.close)
        return

    # 添加社区医院信息
    def Yes(self):
        id = self.ui.Id.text()
        password1 = self.ui.Password1.text()
        password2 = self.ui.Password2.text()
        hospitalname = self.ui.HospitalName.text()
        vaccinenum = self.ui.VaccineNum.text()
        t1 = self.ui.time1.text()
        t2 = self.ui.time2.text()
        t3 = self.ui.time3.text()
        t4 = self.ui.time4.text()
        is_book = '是' if self.ui.YesBook.isChecked() else '否'
        time = t1 + ':' + t2 + '-' + t3 + ':' + t4
        # 有重复
        content = "SELECT * FROM user_info WHERE  id = '%s';" % id
        data = DBS_operation(database="vaccine_info", content=content)
        if data!= None:
            self.Clear()
            AdminError2Window.exec()
            return
        # 两次密码不一致
        if password1!=password2:
            self.Clear()
            AdminError3Window.exec()
            return
        # 输入为空
        if id=='' or password2=='' or password1=='' or hospitalname=='' or vaccinenum=='' or t1=='' or t2=='' or t3=='' or t4=='':
            self.Clear()
            AdminError1Window.exec()
            return
        # 可以注册
        # 添加user_info
        content = "INSERT INTO user_info (id, password, role) VALUES ('%s', '%s', '%s');" % (id, password1, 'B')
        DBS_operation(database='vaccine_info', content=content)
        # 添加hospital_info
        content = "INSERT INTO hospital_info (id, name, num, is_book, time) VALUES ('%s', '%s', '%s', '%s', '%s');" % (id, hospitalname, vaccinenum, is_book, time)
        DBS_operation(database='vaccine_info', content=content)
        self.Clear()
        AddSuccessWindow.exec()
        return

    def Clear(self):
        self.ui.Id.clear()
        self.ui.Password1.clear()
        self.ui.Password2.clear()
        self.ui.HospitalName.clear()
        self.ui.VaccineNum.clear()
        self.ui.time1.clear()
        self.ui.time2.clear()
        self.ui.time3.clear()
        self.ui.time4.clear()

# 社区医院登陆界面 控制器
class HospitalControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.HospitalInfo.clicked.connect(self.HospitalInfoManage)
        ui.UserBook.clicked.connect(self.UserBookManage)
        ui.UserInfo.clicked.connect(self.UserInfoManage)
        ui.BadReaction.clicked.connect(self.BadReactionManage)
        ui.Quit.clicked.connect(self.wnd.close)
        return
    # 社区医院信息管理 槽函数
    def HospitalInfoManage(self):
        global ID
        content = "SELECT * FROM hospital_info WHERE  id = '%s';" % ID
        info = DBS_operation(database="vaccine_info", content=content)
        # 实例化 医院信息管理 界面
        HospitalInfoWindow = QDialog()
        HospitalInfoUI = HospitalInfo(info)
        HospitalInfoUI.setupUi(HospitalInfoWindow)
        # 实例化 医院信息管理 控制器
        HospitalInfoController = HospitalInfoControl(HospitalInfoUI, HospitalInfoWindow)
        HospitalInfoWindow.exec()
        return

    # 社区医院用户预约 槽函数
    def UserBookManage(self):
        content = "SELECT * FROM commonuser_info WHERE  is_book = '%s';" % 'Y'
        info = DBS_operation2(database="vaccine_info", content=content)
        # 医院 预约管理 界面
        HospitalBookWindow = QDialog()
        HospitalBookUI = HospitalBook(info)
        HospitalBookUI.setupUi(HospitalBookWindow)
        # 控制器
        HospitalBookController = HospitalBookControl(HospitalBookUI, HospitalBookWindow)
        HospitalBookWindow.exec()
        return

    # 社区医院接种信息管理 槽函数
    def UserInfoManage(self):
        # 实例化 疫苗信息管理 界面
        InoculateWindow = QDialog()
        InoculateUI = Inoculate()
        InoculateUI.setupUi(InoculateWindow)
        # 实例化 控制器
        InoculateController = InoculateControl(InoculateUI, InoculateWindow)
        InoculateWindow.exec()
        return
    # 社区医院不良反馈 槽函数
    def BadReactionManage(self):
        content = "SELECT * FROM commonuser_info WHERE  is_bad_reaction = '%s';" % 'Y'
        info = DBS_operation2(database="vaccine_info", content=content)
        # 实例化 不良反应 界面
        HospitalBadReactionWindow = QDialog()
        HospitalBadReactionUI = HospitalBadReaction(info)
        HospitalBadReactionUI.setupUi(HospitalBadReactionWindow)
        # 实例化 控制器
        HospitalBadReactionController = HospitalBadReactionControl(HospitalBadReactionUI, HospitalBadReactionWindow)
        HospitalBadReactionWindow.exec()
        return

# 社区医院信息管理 槽函数
class HospitalInfoControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.Yes.clicked.connect(self.Yes)
        ui.Quit.clicked.connect(self.wnd.close)
        return

    def Yes(self):
        newname = self.ui.NewName.text()
        newnum = self.ui.NewNum.text()
        newis_book = '是' if self.ui.YesBook.isChecked() else '否'
        newtime = self.ui.Time1.text() + ':' + self.ui.Time2.text() + '-' + self.ui.Time3.text() + ':' + self.ui.Time4.text()
        content = "UPDATE hospital_info SET name='%s', num='%s', is_book='%s', time='%s' WHERE id='%s';" % (
        newname, newnum, newis_book, newtime, ID)
        DBS_operation(database="vaccine_info", content=content)
        self.ui.NewName.clear()
        self.ui.NewNum.clear()
        self.ui.Time1.clear()
        self.ui.Time2.clear()
        self.ui.Time3.clear()
        self.ui.Time4.clear()
        FixSuccessWindow.exec()
        return

# 社区医院 预约管理 槽函数
class HospitalBookControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.Yes.clicked.connect(self.Yes)
        ui.Del1.clicked.connect(self.Del1)
        ui.Del2.clicked.connect(self.Del2)
        ui.Del3.clicked.connect(self.Del3)
        ui.Del4.clicked.connect(self.Del4)
        ui.Del5.clicked.connect(self.Del5)
        ui.Del6.clicked.connect(self.Del6)
        ui.Del7.clicked.connect(self.Del7)
        ui.Del8.clicked.connect(self.Del8)
        ui.Del9.clicked.connect(self.Del9)
        ui.Del10.clicked.connect(self.Del10)
        ui.Del11.clicked.connect(self.Del11)
        ui.Quit.clicked.connect(self.wnd.close)
        return

    def Yes(self):
        idcard = self.ui.IdCard.text()
        content = "SELECT id FROM commonuser_info WHERE  IDCard = '%s';" % idcard
        cid = DBS_operation(database="vaccine_info", content=content)
        if cid==None:
            self.Clear()
            HospitalError1Window.exec()
            return
        cid = cid[0]
        year = self.ui.Time1.text()
        month = self.ui.Time2.text()
        day = self.ui.Time3.text()
        time = year+'-'+month+'-'+day
        content = "UPDATE commonuser_info SET is_book='%s', book_time='%s' WHERE id='%s';" % ('Y', time, cid)
        DBS_operation(database="vaccine_info", content=content)
        self.Clear()
        HospitalAddSuccussWindow.exec()
        return

    def Clear(self):
        self.ui.IdCard.clear()
        self.ui.Time1.clear()
        self.ui.Time2.clear()
        self.ui.Time3.clear()
        return

    def Del1(self):
        name = self.ui.label_17.text()
        phone = self.ui.label_16.text()
        content = "UPDATE commonuser_info SET is_book='%s', book_time='%s' WHERE name='%s' AND phone='%s';" % ('N', 'NULL', name, phone)
        DBS_operation(database="vaccine_info", content=content)
        HospitalDelSuccussWindow.exec()
        return

    def Del2(self):
        name = self.ui.label_27.text()
        phone = self.ui.label_26.text()
        content = "UPDATE commonuser_info SET is_book='%s', book_time='%s' WHERE name='%s' AND phone='%s';" % (
        'N', 'NULL', name, phone)
        DBS_operation(database="vaccine_info", content=content)
        HospitalDelSuccussWindow.exec()
        return

    def Del3(self):
        name = self.ui.label_18.text()
        phone = self.ui.label_20.text()
        content = "UPDATE commonuser_info SET is_book='%s', book_time='%s' WHERE name='%s' AND phone='%s';" % (
        'N', 'NULL', name, phone)
        DBS_operation(database="vaccine_info", content=content)
        HospitalDelSuccussWindow.exec()
        return

    def Del4(self):
        name = self.ui.label_41.text()
        phone = self.ui.label_34.text()
        content = "UPDATE commonuser_info SET is_book='%s', book_time='%s' WHERE name='%s' AND phone='%s';" % (
        'N', 'NULL', name, phone)
        DBS_operation(database="vaccine_info", content=content)
        HospitalDelSuccussWindow.exec()
        return

    def Del5(self):
        name = self.ui.label_35.text()
        phone = self.ui.label_45.text()
        content = "UPDATE commonuser_info SET is_book='%s', book_time='%s' WHERE name='%s' AND phone='%s';" % (
        'N', 'NULL', name, phone)
        DBS_operation(database="vaccine_info", content=content)
        HospitalDelSuccussWindow.exec()
        return

    def Del6(self):
        name = self.ui.label_28.text()
        phone = self.ui.label_47.text()
        content = "UPDATE commonuser_info SET is_book='%s', book_time='%s' WHERE name='%s' AND phone='%s';" % (
        'N', 'NULL', name, phone)
        DBS_operation(database="vaccine_info", content=content)
        HospitalDelSuccussWindow.exec()
        return

    def Del7(self):
        name = self.ui.label_29.text()
        phone = self.ui.label_42.text()
        content = "UPDATE commonuser_info SET is_book='%s', book_time='%s' WHERE name='%s' AND phone='%s';" % (
        'N', 'NULL', name, phone)
        DBS_operation(database="vaccine_info", content=content)
        HospitalDelSuccussWindow.exec()
        return

    def Del8(self):
        name = self.ui.label_50.text()
        phone = self.ui.label_66.text()
        content = "UPDATE commonuser_info SET is_book='%s', book_time='%s' WHERE name='%s' AND phone='%s';" % (
        'N', 'NULL', name, phone)
        DBS_operation(database="vaccine_info", content=content)
        HospitalDelSuccussWindow.exec()
        return

    def Del9(self):
        name = self.ui.label_61.text()
        phone = self.ui.label_53.text()
        content = "UPDATE commonuser_info SET is_book='%s', book_time='%s' WHERE name='%s' AND phone='%s';" % (
        'N', 'NULL', name, phone)
        DBS_operation(database="vaccine_info", content=content)
        HospitalDelSuccussWindow.exec()
        return

    def Del10(self):
        name = self.ui.label_57.text()
        phone = self.ui.label_48.text()
        content = "UPDATE commonuser_info SET is_book='%s', book_time='%s' WHERE name='%s' AND phone='%s';" % (
        'N', 'NULL', name, phone)
        DBS_operation(database="vaccine_info", content=content)
        HospitalDelSuccussWindow.exec()
        return

    def Del11(self):
        name = self.ui.label_59.text()
        phone = self.ui.label_56.text()
        content = "UPDATE commonuser_info SET is_book='%s', book_time='%s' WHERE name='%s' AND phone='%s';" % (
        'N', 'NULL', name, phone)
        DBS_operation(database="vaccine_info", content=content)
        HospitalDelSuccussWindow.exec()
        return

# 社区医院 接种信息管理 控制器
class InoculateControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.Yes.clicked.connect(self.Yes)
        ui.Search.clicked.connect(self.Search)
        ui.Quit.clicked.connect(self.wnd.close)
        return

    # 添加用户接种信息 槽函数
    def Yes(self):
        idcard = self.ui.IdCard.text()
        vtype = self.ui.VaccineType.text()
        t1, t2, t3 = self.ui.Time1.text(), self.ui.Time2.text(), self.ui.Time3.text()
        time = t1 + '-' + t2 + '-' + t3
        print(idcard, vtype, time)
        # 若输入为空
        if idcard=='' or vtype=='':
            self.Clear()
            LoginErrorWindow1.exec()
            return
        # 若该用户未注册
        content = "SELECT id FROM commonuser_info WHERE  IDCard = '%s';" % idcard
        cid = DBS_operation(database="vaccine_info", content=content)
        if cid == None:
            self.Clear()
            HospitalError1Window.exec()
            return
        # 若该用户已注册
        cid = cid[0]
        print('cid:', cid)
        # 若该用户是第一次添加接种信息
        content = "SELECT * FROM inoculate_info WHERE  id = '%s';" % cid
        info = DBS_operation(database="vaccine_info", content=content)
        print('info:', info, type(info))
        if info==None:
            content = "INSERT INTO inoculate_info (id, vaccine_type, time) VALUES ('%s', '%s', '%s');" % (cid, vtype, time)
            DBS_operation(database='vaccine_info', content=content)
        else:
            newtype = info[1] + ',' + vtype
            newtime = info[2] + ',' + time
            content = "UPDATE inoculate_info SET vaccine_type='%s', time='%s' WHERE id='%s';" % (newtype, newtime, cid)
            DBS_operation(database="vaccine_info", content=content)
        self.Clear()
        HospitalAddSuccussWindow.exec()
        return

    # 查找用户接种信息 槽函数
    def Search(self):
        idcard = self.ui.IdCard_2.text()
        self.ui.IdCard_2.clear()
        # 若该用户未注册
        content = "SELECT id FROM commonuser_info WHERE  IDCard = '%s';" % idcard
        cid = DBS_operation(database="vaccine_info", content=content)
        if cid == None:
            self.Clear()
            HospitalError1Window.exec()
            return
        cid = cid[0]
        content = "SELECT * FROM inoculate_info WHERE  id = '%s';" % cid
        info = DBS_operation(database="vaccine_info", content=content)
        info = info[1:]
        # 实例化 查看接种信息 子界面
        HospitalUserInfoWindow = QDialog()
        HospitalUserInfoUI = HospitalUserInfo(info)
        HospitalUserInfoUI.setupUi(HospitalUserInfoWindow)
        # 实例化 控制器
        HospitalUserInfoController = HospitalUserInfoControl(HospitalUserInfoUI, HospitalUserInfoWindow)

        HospitalUserInfoWindow.exec()
        return

    def Clear(self):
        self.ui.IdCard.clear()
        self.ui.VaccineType.clear()
        self.ui.Time1.clear()
        self.ui.Time2.clear()
        self.ui.Time3.clear()
        return

class HospitalUserInfoControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.Quit.clicked.connect(self.wnd.close)
        return

class HospitalBadReactionControl():
    def __init__(self, ui, wnd):
        self.wnd = wnd
        self.ui = ui
        # 设置信号槽
        ui.pushButton.clicked.connect(self.wnd.close)
        return

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
    SigninWindow = QDialog()
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
    # 实例化登录dialog（提醒输入为空）
    LoginErrorWindow1 = QDialog()
    LoginErrorUI1 = LoginError_Dialog1()
    LoginErrorUI1.setupUi(LoginErrorWindow1)
    # 实例化登录dialog（提醒密码错误）
    LoginErrorWindow2 = QDialog()
    LoginErrorUI2 = LoginError_Dialog2()
    LoginErrorUI2.setupUi(LoginErrorWindow2)
    # 实例化登录dialog（提醒还未注册）
    LoginErrorWindow3 = QDialog()
    LoginErrorUI3 = LoginError_Dialog3()
    LoginErrorUI3.setupUi(LoginErrorWindow3)
    # 实例化普通用户子窗口
    CommonUserWindow = QWidget()
    CommonUserUI = CommonUserLogin()
    CommonUserUI.setupUi(CommonUserWindow)
    # 实例化 删除家庭信息（提示删除成功）
    HomeInfoDelWindow = QDialog()
    HomeInfoDelUI = DelInfo()
    HomeInfoDelUI.setupUi(HomeInfoDelWindow)
    # 实例化 普通用户 预约接种 子窗口
    CommonuserBookWindow = QDialog()
    CommonuserBookUI = CommonuserBook()
    CommonuserBookUI.setupUi(CommonuserBookWindow)
    # 实例化 预约成功 dialog
    BookInfoWindow = QDialog()
    BookInfoUI = BookInfo()
    BookInfoUI.setupUi(BookInfoWindow)
    # 实例化 取消成功 dialog
    BookCancelInfoWindow = QDialog()
    BookCancelInfoUI = BookCancelInfo()
    BookCancelInfoUI.setupUi(BookCancelInfoWindow)
    # 实例化 普通用户 不良反应 子窗口
    CommonuserBadReactionWindow = QDialog()
    CommonuserBadReactionUI = CommonuserBadReaction()
    CommonuserBadReactionUI.setupUi(CommonuserBadReactionWindow)
    # 实例化 普通用户 反馈成功 dialog
    ReactionInfoWindow = QDialog()
    ReactionInfoUI = ReactionInfo()
    ReactionInfoUI.setupUi(ReactionInfoWindow)
    # 实例化 管理员 登录 子窗口
    AdminLoginWindow = QDialog()
    AdminLoginUI = AdminLogin()
    AdminLoginUI.setupUi(AdminLoginWindow)
    # 实例化 管理员 添加疫苗信息 子窗口
    AdminAddWindow = QDialog()
    AdminAddUI = AdminAdd()
    AdminAddUI.setupUi(AdminAddWindow)
    # 实例化 管理员 添加社区医院 子窗口
    AdminAddHospitalWindow = QDialog()
    AdminAddHospitalUI = AdminAddHospital()
    AdminAddHospitalUI.setupUi(AdminAddHospitalWindow)
    # 实例化 注册医院 时的提醒dialog
    AdminError1Window = QDialog()
    AdminError1UI = AdminError1()
    AdminError1UI.setupUi(AdminError1Window)

    AdminError2Window = QDialog()
    AdminError2UI = AdminError2()
    AdminError2UI.setupUi(AdminError2Window)

    AdminError3Window = QDialog()
    AdminError3UI = AdminError3()
    AdminError3UI.setupUi(AdminError3Window)

    AddSuccessWindow = QDialog()
    AddSuccessUI = AddSuccess()
    AddSuccessUI.setupUi(AddSuccessWindow)
    # 实例化 医院 登录界面
    HospitalWindow = QDialog()
    HospitalUI = Hospital()
    HospitalUI.setupUi(HospitalWindow)
    # 实例化 修改成功 dialog
    FixSuccessWindow = QDialog()
    FixSuccessUI = FixSuccess()
    FixSuccessUI.setupUi(FixSuccessWindow)
    # 实例化 医院dialog
    HospitalAddSuccussWindow = QDialog()
    HospitalAddSuccussUI = AddSuccess()
    HospitalAddSuccussUI.setupUi(HospitalAddSuccussWindow)

    HospitalDelSuccussWindow = QDialog()
    HospitalDelSuccussUI = DelSuccess()
    HospitalDelSuccussUI.setupUi(HospitalDelSuccussWindow)

    HospitalError1Window = QDialog()
    HospitalError1UI = HospitalError1()
    HospitalError1UI.setupUi(HospitalError1Window)



    # 实例化控制器
    MainController = MainControl(MainUI)
    SigninController = SigninControl(SigninUI, SigninWindow)
    CommonUserController = CommonUserControl(CommonUserUI, CommonUserWindow)
    CommonuserBookController = CommonuserBookControl(CommonuserBookUI, CommonuserBookWindow)
    CommonuserReactionController = CommonuserReactionControl(CommonuserBadReactionUI, CommonuserBadReactionWindow)
    AdminLoginController = AdminLoginControl(AdminLoginUI, AdminLoginWindow)
    AdminAddController = AdminAddControl(AdminAddUI, AdminAddWindow)
    AdminAddHospitalController = AdminAddHospitalControl(AdminAddHospitalUI, AdminAddHospitalWindow)
    HospitalController = HospitalControl(HospitalUI, HospitalWindow)

    MainWindow.show()
    sys.exit(app.exec_())


