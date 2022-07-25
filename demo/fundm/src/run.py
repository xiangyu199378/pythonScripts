import  os
import  sys
import  xlrd
import  requests
from  module  import  sqlm


if __name__ == '__main__':
    curr_dir = os.getcwd()
   #book = deal_excel(curr_dir + '\向氏集团投资跟踪表.xlsx')
    print(curr_dir)
    print(sys.path)
    sqlm.sql_test()
