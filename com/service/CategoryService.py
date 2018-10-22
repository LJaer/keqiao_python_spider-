# encoding=utf-8
import threading
import time

from com.db.UserDao import UserDao
from com.db.FirstCategoryDao import FirstCategoryDao
from com.db.SecondCategoryDao import SecondCategoryDao
from com.entity.Category import FirstCategory
from com.entity.Category import SecondCategory
from selenium import webdriver
from time import sleep


class CategoryService:

    def __init__(self):
        self.sem = threading.Semaphore(10)  # 限制线程的最大数量为5个
        self.category_types = []
        self.second_category_types = []
        self.cur_num = 1  # 当前爬取到第几个空间

    def get_all_category_type(self):
        start_time = time.time()
        users = UserDao.select_all()
        threads = []
        for user in users:
            threads.append(threading.Thread(target=self.get_single_category_type, args=(user,)))
        for t in threads:
            t.start()
            t.join()
        end_time = time.time()
        print('get_all_category_type 执行耗时 {} 秒'.format((end_time - start_time)))

    def get_single_category_type(self, user):
        space_url = user.url
        sid = user.sid
        with self.sem:
            str_log = '';
            # chromedriver = "E:\soft\Python\Python37\chromedriver"
            # chromedriver = "/usr/local/Cellar/python3/3.6.1/chromedriver"
            # os.environ["webdriver.chrome.driver"] = chromedriver
            option = webdriver.ChromeOptions()
            option.add_argument("headless")
            driver = webdriver.Chrome(options=option)

            # 进入个人空间
            driver.get(space_url)
            sleep(2)
            # 获取一级分类
            str_log = str_log + space_url + '  第 ' + str(self.cur_num) + '  个' + '\n'
            self.cur_num = self.cur_num + 1
            category_type_elements = driver.find_elements_by_xpath(
                '/html/body/div[2]/div[2]/div/div/div[2]/div/div/dl/dt');
            # /html/body/div[2]/div[2]/div[3]/div[2]/div[2]/div/div/dl[2]/dt
            cur_category_types = []
            for category in category_type_elements:
                category_txt = category.get_attribute("innerHTML")
                if ('全部成果' not in category_txt and 'index.php' not in category_txt):
                    cur_category_types.append(category_txt)
                    self.category_types.append(category_txt)
            str_log = str_log + str(cur_category_types) + '\n'

            # 获取二级分类
            second_category_type_elements = driver.find_elements_by_xpath(
                '/html/body/div[2]/div[2]/div/div/div[2]/div/div/dl/dd/span[1]/a');
            #    /html/body/div[2]/div[2]/div[1]/div[12]/div[2]/div/div/dl[8]/dd[1]/span[1]/a
            #    /html/body/div[2]/div[2]/div[1]/div[12]/div[2]/div/div/dl[5]/dd[3]/span[1]/a
            #    /html/body/div[2]/div[2]/div[1]/div[12]/div[2]/div/div/dl[5]/dd[2]/span[1]/a
            #    /html/body/div[2]/div[2]/div[1]/div[2]/div[2]/div/div/dl[4]/dd[2]/span[1]/a
            #    /html/body/div[2]/div[2]/div[3]/div[2]/div[2]/div/div/dl[2]/dd[1]/span[1]/a
            cur_second_category_types = []
            for second_category in second_category_type_elements:
                second_category_txt = second_category.get_attribute("innerHTML")
                self.second_category_types.append(second_category_txt)
                cur_second_category_types.append(second_category_txt)
            str_log = str_log + str(cur_second_category_types) + '\n'
            print(str_log)
            # 插入数据库
            if FirstCategoryDao.select_by_sid(sid) is None:
                FirstCategoryDao.insert(FirstCategory(sid, str(cur_category_types)))
            else:
                print('数据中已存在: sid ={} first_category={} '.format(sid, str(cur_category_types)))

            if SecondCategoryDao.select_by_sid(sid) is None:
                SecondCategoryDao.insert(SecondCategory(sid, str(cur_second_category_types)))
            else:
                print(
                    '数据中已存在: sid ={} second_category={} '.format(sid, str(cur_second_category_types)))
            # driver.quit()
