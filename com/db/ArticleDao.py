# encoding=utf-8


import pymysql

from com.entity.Article import Article
from config import Logger

log = Logger('all.log', level='debug').logger

class ArticleDao:

    # 查找数据
    @staticmethod
    def select_by_article_id(article_id):
        db = pymysql.connect(host="localhost", user="root", password="root", db="keqiao",
                             charset="utf8mb4")
        cursor = db.cursor()
        select_sql = "select sid, article_id, name, url, read_count, discuss_count, spread_count from keqiao_article where article_id = '{}' ".format(
            article_id)
        try:
            cursor.execute(select_sql)
            result = cursor.fetchone()
            if result is None:
                return None
            else:
                sid = result[0]
                article_id = result[1]
                name = result[2]
                url = result[3]
                read_count = result[4]
                discuss_count = result[5]
                spread_count = result[6]
                return Article(sid, article_id, name, url, read_count, discuss_count, spread_count)
        except Exception as e:
            log.error(str(e))

    # 插入数据
    @staticmethod
    def insert(article):
        db = pymysql.connect(host="localhost", user="root", password="root", db="keqiao",
                             charset="utf8mb4")
        cursor = db.cursor()
        sql_insert = 'insert into keqiao_article (sid, article_id, name, url, read_count, discuss_count, spread_count) values("{}","{}","{}","{}","{}","{}","{}")'.format(
            article.sid, article.article_id, article.name, article.url, article.read_count,
            article.discuss_count,
            article.spread_count)
        try:
            cursor.execute(sql_insert)
            # 提交
            db.commit()
        except Exception as e:
            # 错误回滚
            log.error(str(e))
            db.rollback()

        log.info('插入数据为：{}'.format(article.to_string()))

    # 更新数据
    @staticmethod
    def update(article):
        db = pymysql.connect(host="localhost", user="root", password="root", db="keqiao",
                             charset="utf8mb4")
        cursor = db.cursor()
        sql_update = 'update keqiao_article set read_count={}, discuss_count={}, spread_count={} where article_id={}'.format(
            article.read_count, article.discuss_count, article.spread_count, article.article_id)
        try:
            cursor.execute(sql_update)
            # 提交
            db.commit()
        except Exception as e:
            # 错误回滚
            log.error(str(e))
            db.rollback()

        log.info('更新数据为：{}'.format(article.to_string()))
