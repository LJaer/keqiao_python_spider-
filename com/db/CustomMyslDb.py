# encoding=utf-8
# 数据库连接
import pymysql


class CustomMyslDb(object):

    def __init__(self):
        # 数据库连接
        self.db = pymysql.connect(host="localhost", user="root", password="root", db="keqiao",
                                          charset="utf8mb4")
        self.cursor = self.db.cursor()

    def get_cusor(self):
        return self.cursor

if __name__ == '__main__':
    mysqldb = CustomMyslDb()
    cursor = mysqldb.cursor
