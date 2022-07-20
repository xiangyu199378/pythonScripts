import sqlite3
 
from sqlite3 import Error
from this import s
 
def sql_table(con):
 
    cursorObj = con.cursor()
 
    cursorObj.execute("CREATE TABLE employees(id integer PRIMARY KEY, name text, salary real, department text, position text, hireDate text)")
 
    con.commit()

def sql_insert(con, entities):
 
    cursorObj = con.cursor()
   
#    entities = (2, 'Andrew', 800, 'IT', 'Tech', '2018-02-06') 
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
 
def sql_table_fundz(con):
 
    cursorObj = con.cursor()
 
    entities = (123, 'Andrew', 800, 'IT', 'Tech', '2018-02-06')
    #cursorObj.execute("CREATE TABLE fundz(code integer PRIMARY KEY, name text, salary real, department text, position text, Date text)")
    cursorObj.execute('INSERT INTO fundz(code, name, salary, department, position, Date) VALUES(?, ?, ?, ?, ?, ?)', entities)
    con.commit()


def sql_table_fund(data):
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()
    entities = (123, 'Andrew', 800, 'IT', 'Tech', '2018-02-06')
    #cursorObj.execute("CREATE TABLE fundz(code integer PRIMARY KEY, name text, salary real, department text, position text, Date text)")
    cursorObj.execute('INSERT INTO fundz(code, name, salary, department, position, Date) VALUES(?, ?, ?, ?, ?, ?)', entities)
    con.commit()