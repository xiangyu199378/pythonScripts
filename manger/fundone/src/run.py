import  os
import  sys
from  module  import  sqlm


if __name__ == '__main__':
    curr_dir = os.getcwd()
    print(curr_dir)
    sqlm.sql_init(curr_dir)
