# 参考文章http://www.cppcns.com/jiaoben/python/482171.html

import pymysql


stand_db = {
    "host":"localhost","port":3306,
    "user":"root","pwd":"Myroot123!","name":"fund_data",
}

# 标准库数据库连接
std_db = pymysql.connect(host=stand_db["host"],port=stand_db["port"],database=stand_db["name"],
                        charset="utf8",user=stand_db["user"],passwd=stand_db["pwd"])

# search deal
def query_data(sql):
    cursor=std_db.cursor()
    cursor.execute(sql)
    rslt=cursor.fetchall()
    cursor.close()
    return rslt

# save data

def save_data(sql):
    cursor=std_db.cursor()
    cursor.execute(sql)
    cursor.close()
    std_db.commit()
