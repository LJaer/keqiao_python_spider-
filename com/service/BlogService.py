# encoding=utf-8
import logging.config
import threading
import time
from time import sleep

from selenium import webdriver

from com.db.ArticleDao import ArticleDao
from com.db.UserDao import UserDao
from com.entity.Article import Article
from config import Logger

log = Logger('all.log', level='debug').logger


class BlogService:

    def __init__(self):
        self.sem = threading.Semaphore(10)  # 限制线程的最大数量为5个
        self.pre_url = 'http://space.sxedu.org/index.php?r=space/person/blog/index&sid='
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("headless")
        self.driver = webdriver.Chrome(options=self.option)
        self.tab_handles = []

    def get_all_blog(self):
        start_time = time.time()
        users = UserDao.select_all()
        all_blog_threads = []
        for user in users:
            all_blog_threads.append(threading.Thread(target=self.get_single_blog, args=(user.sid,)))

        for thread in all_blog_threads:
            thread.start()
            thread.join()


        end_time = time.time()

        print('get_all_blog 执行耗时 {} 秒'.format((end_time - start_time)))

    def get_current_page_blog(self, sid):
        start_time = time.time()

        cur_page_blogs = self.driver.find_elements_by_xpath(
            '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/ul/li/p[1]/a')

        article_num = 1
        for blog in cur_page_blogs:
            self.get_single_article(sid, blog, article_num)
            article_num = article_num + 1

        end_time = time.time()
        print('get_current_page_blog 执行耗时 {} 秒'.format((end_time - start_time)))

    # 获取单个标题内容
    def get_single_article(self, sid, blog, article_num):
        start_time = time.time()
        article_name = blog.get_attribute('innerHTML')
        article_url = blog.get_attribute('href')

        read_xpath = '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/ul/li[{}]/div[2]/div/span[1]/em'.format(
            article_num)
        article_read = self.driver.find_element_by_xpath(read_xpath).get_attribute('data-count')

        discuss_xpath = '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/ul/li[{}]/div[2]/div/span[2]/em'.format(
            article_num)
        article_discuss = self.driver.find_element_by_xpath(discuss_xpath).get_attribute('data-count')

        spread_xpath = '/html/body/div[2]/div[2]/div/div[2]/div[1]/div/ul/li[{}]/div[2]/div/span[3]/em'.format(
            article_num)
        article_spread = self.driver.find_element_by_xpath(spread_xpath).get_attribute('data-count')
        # str_log = '文章名：{},地址：{}，阅读数：{}，评论数：{}，转发数：{}'.format(article_name, article_url, article_read,article_discuss, article_spread)
        # print(str_log)

        article_id = article_url.split('=')[3]

        article = Article(sid, article_id, article_name, article_url, article_read, article_discuss,
                          article_spread)
        # 查询是否已经插入过
        if ArticleDao.select_by_article_id(article_id) is None:
            ArticleDao.insert(article)
        else:
            ArticleDao.update(article)

        end_time = time.time()
        print('get_single_article 执行耗时 {} 秒'.format((end_time - start_time)))

    # 获取一个空间的所有文章地址
    def get_single_blog(self, sid):
        with self.sem:
            blog_url = self.pre_url + sid
            self.driver.get(blog_url)
            sleep(2)
            page_num = self.driver.find_element_by_class_name('mglr15') \
                .get_attribute('innerHTML').replace('共 ', '').replace(' 页', '')
            page_num = int(page_num)
            logging.info('空间地址：{} ，共 {} 页 \n '.format(blog_url, page_num))

            self.open_tabs(blog_url, page_num)
            self.get_tab_article(sid, page_num)

        self.driver.quit()

    # 获取一页文章列表的文章
    def get_tab_article(self, sid, page_num):
        for i in range(page_num):
            self.driver.switch_to.window(self.driver.window_handles[i])
            self.get_current_page_blog(sid)

    # 打开一个空间所有文章列表
    def open_tabs(self, blog_url, page_num):
        for i in range(page_num):
            if i > 0:
                cur_blog_url = blog_url + '&page=' + str(i + 1)
                js = 'window.open("{}");'.format(cur_blog_url)
                self.driver.execute_script(js)
                self.tab_handles.append(self.driver.current_window_handle)


if __name__ == '__main__':
    blog_service = BlogService()
    blog_service.get_single_blog(str(33355))
