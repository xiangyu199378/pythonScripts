# -*- coding: utf-8 -*-
"""
根据FundList.xls文件中的基金列表，从小熊同学网站API读取基金净值信息，写入到
新净值.xls文件中。
@author: RockyCoder
"""
'''
第一部分：引用
'''
 
import requests
import json
import xlrd
from xlutils.copy import copy
import os
'''
第二部分：函数
'''
# 将长度不定的列表，按照指定长度切割为子列表后，整合成嵌套列表。
 
def LineList(SrcList,LineLen):
    # 新列表，供返回
    NewList=[]
    # 记录源列表长度
    SrcLen=len(SrcList)
 
    # 判断是否需要分行
    if SrcLen<LineLen:
        return SrcList
    else:
        # 若需要分行，计算行数和剩余个数
        LineCnt=int(SrcLen/LineLen)
        LeftLen=SrcLen%LineLen
        # 在行数范围内，通过列表切片方式，获取指定长度的子列表
        for i in range(LineCnt):
            Lines=SrcList[(i*LineLen):(i*LineLen+LineLen):1]
            # 拼接到返回列表中
            NewList.append(Lines)
        # 如果剩余个数大于0，则将剩余部分通过切片方式，以子列表形式拼接到返回列表
        if LeftLen>0:
            NewList.append(SrcList[SrcLen-LeftLen:])
 
        return NewList
 
# 将指定的列表转换为以逗号分隔的字符串
 
def CSVString(SrcList):
    TempString=''
    
    for i in range(len(SrcList)):
        if type(SrcList[i]) is int:
            TempString=TempString+str(SrcList[i])+','
        elif type(SrcList[i]) is str:
            TempString=TempString+SrcList[i]+','
        else:
            print(type(SrcList[i]))
            
    return TempString[:-1]
 
 
'''
第三部分：操作
'''
# 打开基金原始表格
curr_dir = os.getcwd()
rdBook=xlrd.open_workbook( curr_dir + '\FundList.xlsx')
rdSheet=rdBook.sheet_by_name('Sheet1')
# 复制原始表格用于填数
dstb=copy(rdBook)
dstt=dstb.get_sheet(0)
# 初始化基础变量
url="https://api.doctorxiong.club/v1/fund?code="
s=2
 
# 读取完整基金列表

fundCnt=int(rdSheet.cell_value(0,2))
FundList=[]
for j in range(2,fundCnt+1):
    FundCode=str(int(rdSheet.cell_value(j,1)))
    if len(FundCode)>0:
        FundList.append('0'*(6-len(FundCode))+FundCode)
    else:
        print("基金代码不得为空")
        exit(0)
print("基金代码不得为空",rdSheet.cell_value(0,2))        
# 按照20个一组，形成子列表
Lines=[]
Lines=LineList(FundList,20)
 
for l in Lines:
    # 根据逐个子列表，形成URL
    FinalURL=url+CSVString(l)
    strHTML=requests.get(FinalURL)
    contents=json.loads(strHTML.text)
    for k in contents["data"]:
            # 序号
            dstt.write(s,0,str(s-1))
            # 基金代码
            dstt.write(s,1,k['code'])
            # 基金名称
            dstt.write(s,2,k['name'])
            # 单位净值
            dstt.write(s,3,str(k['netWorth']))
            # 单位净值日涨幅
            dstt.write(s,4,k['dayGrowth'])
            # 周涨幅
            dstt.write(s,5,k['lastWeekGrowth'])
            # 月涨幅
            dstt.write(s,6,k['lastMonthGrowth'])
            # 季涨幅
            dstt.write(s,7,k['lastThreeMonthsGrowth'])
            # 半年涨幅
            dstt.write(s,8,k['lastSixMonthsGrowth'])
            # 年涨幅
            dstt.write(s,9,k['lastYearGrowth'])
            # 单位净值更新日期
            dstt.write(s,10,k['netWorthDate'])
            s=s+1
            dstb.save('净值'+k['netWorthDate']+'.xls')