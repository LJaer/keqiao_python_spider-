# encoding=utf-8
# userdao
from com.db.CustomMyslDb import CustomMyslDb
from com.entity.User import User

curtom_mysqldb = CustomMyslDb()
db = curtom_mysqldb.db
cursor = curtom_mysqldb.cursor


class UserDao:

    # 查询所有数据
    @staticmethod
    def select_all():
        select_sql = "select sid,name,grade,url from keqiao_user limit 500"
        try:
            cursor.execute(select_sql)
            results = cursor.fetchall()
            users = []
            for result in results:
                sid = result[0]
                name = result[1]
                grade = result[2]
                url = result[3]
                user = User(sid, name, grade, url)
                users.append(user)

            return users
        except Exception as e:
            raise e

    # 根据 sid 查询数据
    @staticmethod
    def select_by_sid(sid):
        select_sql = "select sid,name,grade,url from keqiao_user where sid = '{}' ".format(sid)
        try:
            cursor.execute(select_sql)
            result = cursor.fetchone()
            if result is None:
                return None
            else:
                sid = result[0]
                name = result[1]
                grade = result[2]
                url = result[3]
                return User(sid, name, grade, url)
        except Exception as e:
            raise e

    # 插入数据
    @staticmethod
    def insert(user):
        sql_insert = "insert into keqiao_user(name,sid,grade,url) values('{}','{}','{}','{}')".format(user.name,
                                                                                                      user.sid,
                                                                                                      user.grade,
                                                                                                      user.url)
        try:
            cursor.execute(sql_insert)
            # 提交
            db.commit()
        except Exception as e:
            # 错误回滚
            print(str(e))
            db.rollback()
        print('插入的数据为: name={} sid ={} url={} '.format(user.name, user.sid, user.url))


if __name__ == '__main__':
    print(UserDao.select_by_sid('123455'))
    print(UserDao.select_by_sid('136482'))
