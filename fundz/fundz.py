"""
基金数据管理
@author:Mark Xiang 
"""
import  os
import  xlrd
import  requests
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from turtle import down
from bs4 import BeautifulSoup

# 处理乱码
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family']='sans-serif'
matplotlib.rcParams['axes.unicode_minus'] = False
 
def get_html(code):
    Url = 'http://fund.eastmoney.com/{0}.html'.format(code)
    rsp = requests.get(Url)
    html = rsp.text  
    return html

def deal_excel(path):
    # 打开基金原始表格
    rdBook=xlrd.open_workbook(path)
    rdSheet=rdBook.sheet_by_name('基金数据')
    row_j = 2
    fundCnt=5
    FundList=[]
    for j in range(2,fundCnt+1):
        FundCode=str(int(rdSheet.cell_value(j,1)))
        if len(FundCode)>0:
            FundList.append('0'*(6-len(FundCode))+FundCode)
        else:
            print("基金代码不得为空")
            exit(0)
    return  FundList


def deal_get_fundz(FundList):
    List=FundList
    for value in List:
    # 根据逐个子列表，形成URL
        html=get_html(value)
        soup = BeautifulSoup(html, 'html.parser')
        # 获取总页数
        pattern = re.compile('pages:(.*),')
        print(pattern)
        #result = re.search(pattern, html).group(1)
       # total_page = int(result)
        # 获取表头信息
        heads = []
        for head in soup.findAll("th"):
            heads.append(head.contents[0]) 
    return  

if __name__ == '__main__':
    curr_dir = os.getcwd()
    fund_code_list = deal_excel(curr_dir + '\向氏集团投资跟踪表.xlsm')
    deal_get_fundz(fund_code_list)
    print(fund_code_list)
