# -*- coding: utf-8 -*-
import sys
import MySQLdb as mdb
import MySQLdb.cursors
import time

reload(sys)
sys.setdefaultencoding("utf-8")

# 主机地址: localhost ；用户名: root ，密码:new_password ;  数据库的名称: bookinfo  也可以使用字典进行连接参数的管理
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': 'new_password',
    'db': 'bookinfo',
    'charset': 'utf8'
}


def create_db(db_name):
    conn = mdb.connect(**config)
    cursor = conn.cursor()
    try:
        # 创建数据库

        cursor.execute('DROP DATABASE IF EXISTS %s' % db_name)
        cursor.execute('CREATE DATABASE IF NOT EXISTS %s' % db_name)
        conn.select_db(db_name)
    except:
        import traceback
        traceback.print_exc()
        # 发生错误时会滚
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def execute_sql(sql, paramater):
    status_code = 0
    conn = mdb.connect(**config)

    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    try:
        cursor.execute(sql, paramater)
        conn.commit()
    except mdb.Error, e:
        status_code = -1
        # import traceback
        # traceback.print_exc()
        # 发生错误时会滚
        # conn.rollback()
        print "Error %d: %s" % (e.args[0], e.args[1])
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    finally:
        if conn:
            cursor.close()
            conn.close()
        return status_code



# 查询操作
def select(sql):
    conn = mdb.connect('localhost', 'root', 'new_password', 'bookinfo', charset="utf8",
                       cursorclass=MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    # example:   cursor.execute('select type from bookType')
    cursor.execute(sql)

    result = cursor.fetchall()


    type  = result[0]['type']
    print type
    return result

# 查询操作
def select_url(sql):
    conn = mdb.connect('localhost', 'root', 'new_password', 'bookinfo', charset="utf8",
                       cursorclass=MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    # example:   cursor.execute('select type from bookType')
    cursor.execute(sql)

    result = cursor.fetchall()


    return result

#
def select_one_hundred():
    status_code = 0
    conn = mdb.connect(**config)

    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    # sql = " SELECT url FROM bookForQidian WHERE id>={start_num} AND id<={end_num}".format(start_num = start_num,end_num = start_num+100)
    # sql = " SELECT url FROM bookForQidian ORDER by recommend DESC A LIMIT {start_num} , {end_num} ".format(start_num = start_num,end_num = start_num+99)
    sql = " SELECT url FROM bookForQidian ORDER by recommend DESC "
    try:
        cursor.execute(sql)
        conn.commit()
        urls = cursor.fetchall()

    except mdb.Error, e:
        status_code = -1
        # import traceback
        # traceback.print_exc()
        # 发生错误时会滚
        # conn.rollback()
        print "Error %d: %s" % (e.args[0], e.args[1])
        print
    finally:
        if conn:
            cursor.close()
            conn.close()
        return urls


if __name__ == '__main__':
    # create_db('book')
    # select_one_hundred(1)
    pass