import sqlite3

from pymysql import NULL

 
def  sql_init(name):
    print("sql_init")
    if str(name) != NULL:
         con = sqlite3.connect(name)
    else:
        con = sqlite3.connect("database.db")
    cursor = con.cursor()
    return  cursor

def sql_search(cur,search):
    cur.execute('select*from user')

def sql_test():
    print("Hey, I am a file")



