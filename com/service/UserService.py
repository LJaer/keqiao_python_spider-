# encoding=utf-8
# 用户类
from time import sleep

from com.db.UserDao import UserDao
from com.entity.User import User
from com.service.WebDriverService import WebDriverService


class UserService:

    def __init__(self):
        self.teacher_urls = []
        self.webdriver_service = WebDriverService()
        self.driver = self.webdriver_service.driver

    # 获取该年级所有老师空间
    def get_urls(self):

        # 年级
        grades = {"小学": "3", "初中": "4", "高中": "5", }
        # grades = {"高中": "5", }
        for grade in grades.keys():
            # 所有教师空间
            self.driver.get(
                "http://space.sxedu.org/index.php?r=space/index/Spaceindex/search&cls=person_space&type=teacher")
            sleep(2)
            # 点击选择学前教师空间
            self.driver.find_element_by_xpath('//*[@id="grade_item"]/span[1]/p').click()
            sleep(2)
            grade_type = grades.get(grade)
            grade_xpath = '//*[@id="grade_item"]/span[2]/a[%s]' % (grade_type)
            print(grade_xpath)
            self.driver.find_element_by_xpath(grade_xpath).click()
            sleep(2)

            # 获取当前页数
            total_page = self.driver.find_element_by_xpath('//*[@id="loadList"]/div/span[3]').get_attribute("innerHTML")
            total_page = str(total_page).replace('共', '').replace('页', '')
            total_page = int(total_page)

            self.get_cur_urls(grade)

            for i in range(total_page - 1):
                self.driver.find_element_by_class_name('p_right').click()
                sleep(5)
                self.get_cur_urls(grade)

    # 获取当前页老师空间地址
    def get_cur_urls(self, grade):
        # 获取当前页老师链接a
        sleep(2)
        cur_page_teachers = self.driver.find_elements_by_xpath('//*[@id="loadList"]/ul/li/div[2]/a')
        count = 1
        for teacher in cur_page_teachers:
            url = str(teacher.get_attribute('href'))
            url = url.replace('&user_sitecode=330621', '')
            name = self.driver.find_element_by_xpath(
                '//*[@id="loadList"]/ul/li[{}]/div[2]/a'.format(str(count))).get_attribute("innerHTML")
            count = count + 1
            # //*[@id="loadList"]/ul/li[1]/div[2]/a
            # //*[@id="loadList"]/ul/li[38]/div[2]/a
            # 插入数据库
            sid = url[58:]
            user = User(sid, name, grade, url)
            # 查询是否已经插入过
            if UserDao.select_by_sid(sid) is None:
                UserDao.insert(user)
            else:
                print('数据中已存在: name={} sid ={} url={} '.format(user.name, user.sid, user.url))
