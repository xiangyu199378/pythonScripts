import sqlite3
 
from sqlite3 import Error
 
def sql_table(con):
 
    cursorObj = con.cursor()
 
    cursorObj.execute("CREATE TABLE employees(id integer PRIMARY KEY, name text, salary real, department text, position text, hireDate text)")
 
    con.commit()

def sql_insert(con, entities):
 
    cursorObj = con.cursor()
    
    cursorObj.execute('INSERT INTO employees(id, name, salary, department, position, hireDate) VALUES(?, ?, ?, ?, ?, ?)', entities)
    
    con.commit()
 



def sql_fetch(con):
 
    cursorObj = con.cursor()
 
    cursorObj.execute('SELECT * FROM employees')
 
    rows = cursorObj.fetchall()
 
    for row in rows:
 
        print(row)
 

def sql_update(con):
 
    cursorObj = con.cursor()
 
    cursorObj.execute('UPDATE employees SET name = "Rogers" where id = 2')
 
    con.commit()

 
def sql_delete(con):
 
    cursorObj = con.cursor()
 
    cursorObj.execute('DROP table if exists employees')
 
    con.commit()
 

if __name__ == '__main__':
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()
    sql_fetch(con)