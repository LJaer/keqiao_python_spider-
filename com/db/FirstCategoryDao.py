# encoding=utf-8
# userdao
from com.db.CustomMyslDb import CustomMyslDb
from com.entity.Category import FirstCategory

curtom_mysqldb = CustomMyslDb()
db = curtom_mysqldb.db
cursor = curtom_mysqldb.cursor


class FirstCategoryDao:

    # 根据 sid 查询数据
    @staticmethod
    def select_by_sid(sid):
        select_sql = "select sid,first_category from keqiao_first_category where sid = '{}' ".format(sid)
        try:
            cursor.execute(select_sql)
            result = cursor.fetchone()
            if result is None:
                return None
            else:
                sid = result[0]
                first_category = result[1]
                return FirstCategory(sid, first_category)
        except Exception as e:
            print(str(e))

    # 插入数据
    @staticmethod
    def insert(first_category):
        sql_insert = 'insert into keqiao_first_category(sid,first_category) values("{}","{}")'.format(
            first_category.sid,
            first_category.first_category)
        try:
            cursor.execute(sql_insert)
            # 提交
            db.commit()
        except Exception as e:
            # 错误回滚
            print(str(e))
            db.rollback()
        print('插入的数据为: sid={} first_category ={} '.format(first_category.sid,
                                                              first_category.first_category))


