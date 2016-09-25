# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from threading import Thread
import random

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException


class AutoHomeRobot(Thread):
    
    MAX_FORUM_PAGE = 1

    NAV_PARSER_MAP = [
        ('参数配置', 'parse_config'), 
        ('图片实拍', 'parse_picture'),
        ('报价', 'parse_price'),
        # ('口碑', 'parse_koubei'),
        ('车型详解', 'parse_detail'),
        ('文章', 'parse_topic'),
        ('视频', 'parse_video'),
        ('二手车', 'parse_used'), 
        ('知道', 'parse_question'), 
        # ('车主价格', 'parse_nothing'),
        ('论坛', 'parse_forum'),
    ]

    def __init__(self, start_url, *args, **kwargs):
        super(AutoHomeRobot, self).__init__(*args, **kwargs)
        self.start_url = start_url

    def init_driver(self):
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub', 
            desired_capabilities=webdriver.DesiredCapabilities.CHROME.copy()
        )
        # self.driver.implicitly_wait(10)
        self.driver.get(self.start_url)

    def fini_driver(self):
        self.driver.quit()

    def run(self):
        # 线程开始时随机休眠几秒钟
        self._random_sleep(0, 10)
        self.init_driver()
        self.parse_home()
        self.fini_driver()

    def parse_config(self):
        pass

    def parse_picture(self):
        pass

    def parse_price(self):
        pass

    def parse_koubei(self):
        pass

    def parse_detail(self):
        pass
    
    def parse_topic(self):
        pass

    def parse_video(self):
        pass

    def parse_used(self):
        pass

    def parse_question(self):
        pass

    def _random_sleep(self, x=5, y=10):
        i = random.randint(x, y)
        time.sleep(i)

    def _click_element(self, element, callback, *args, **kwargs):
        parent_window_handle = self.driver.current_window_handle

        try:
            element.click()
        except ElementNotVisibleException as e:
            print e
            return

        is_new_window = self.driver.window_handles[-1] != parent_window_handle 

        if is_new_window:
            self.driver.switch_to.window(self.driver.window_handles[-1])

        callback(*args, **kwargs)

        self._random_sleep()

        if is_new_window:
            self.driver.close()
            self.driver.switch_to.window(parent_window_handle)

    def parse_home(self):
        xpath_template = '//li[@class="nav-item"]/a[text()="{nav}"]'

        for nav, parser in self.NAV_PARSER_MAP:
            try:
                elem = self.driver.find_element_by_xpath(xpath_template.format(nav=nav))
            except NoSuchElementException as e:
                print e, 'nav=<{0}>, parser=<{1}>'.format(nav, parser)
            parse_method = getattr(self, parser)
            self._click_element(elem, parse_method)


    def parse_forum(self, page=1):
        # print self.driver.title
        # print self.driver.current_url

        # 限制最大访问的页面数
        if page > self.MAX_FORUM_PAGE:
            return

        # 获取所有帖子链接
        elems = self.driver.find_elements_by_xpath('//a[@class="a_topic"]')
        forum_window_handle = self.driver.current_window_handle
        for elem in elems:
            # 访问帖子
            self._click_element(elem, self.parse_thread)

        # 达到最后一页
        try:
            elem = self.driver.find_element_by_xpath('//a[@class="afpage"]')
        except NoSuchElementException:
            return

        # 访问下一页
        self._click_element(elem, self.parse_forum, page+1)

    def parse_thread(self):
        print self.driver.title


MAX_THREAD_NUM = 2
target_url = 'http://www.autohome.com.cn/692/'


if __name__ == '__main__':
    workers = []
    for i in range(MAX_THREAD_NUM):
        ahr = AutoHomeRobot(target_url, name='Robot-{0}'.format(i))
        workers.append(ahr)
        ahr.start()

    for worker in workers:
        worker.join()
