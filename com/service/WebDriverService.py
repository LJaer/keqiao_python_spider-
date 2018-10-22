# encoding=utf-8
# webdriver service
import os
from selenium import webdriver


class WebDriverService:

    def __init__(self):
        self.chromedriver = "E:\soft\Python\Python37\chromedriver"
        # chromedriver = "/usr/local/Cellar/python3/3.6.1/chromedriver"
        os.environ["webdriver.chrome.driver"] = self.chromedriver
        self.driver = webdriver.Chrome(self.chromedriver)

    # 无界面
    @staticmethod
    def get_driver_background():
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        driver = webdriver.Chrome(options=option)
        return driver


if __name__ == '__main__':
    WebDriverService().driver.get("http://www.baidu.com")
