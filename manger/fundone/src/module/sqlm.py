import sqlite3

from pymysql import NULL

 
def  sql_init(path):
    if path != NULL:
        lpath=path+"\database.db"
    else:
        lpath="database.db"
    print(lpath)
    con = sqlite3.connect("vaccine_info.db")
    return  con

def sql_search(cur,search):
    cur.execute('select*from user')

def sql_test():
    print("Hey, I am a file")



