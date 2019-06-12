# -*- coding: utf-8 -*-
import scrapy
import time
from selenium.webdriver import Firefox


class WeiboPostSpider(scrapy.Spider):
    name = 'weibo_post'
    allowed_domains = ['weibo.com']
    start_urls = ['https://weibo.com/']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    def parse(self, response):
        item = {}
        return item

    def __init__(self):
        self.cookies = []

    def get_cookies(self):
        browser = Firefox(executable_path="D:\chromedriver\geckodriver.exe")
        browser.get("http://www.renren.com/")
        time.sleep(30)
        elem_user = browser.find_element_by_xpath('//input[@id="email"]')
        elem_user.send_keys('xxxxxxx')
        elem_pwd = browser.find_element_by_xpath('//input[@id="password"]')
        elem_pwd.send_keys('xxxxxxxx')
        commit = browser.find_element_by_xpath('//input[@id="login"]')
        commit.click()
        time.sleep(20)
        # 人人网，中国领先的实名制SNS社交网络。加入人人网，找到老同学，结识新朋友。
        if "人人网 - 新用户76591" in browser.title:
            self.cookies = browser.get_cookies()
            browser.close()
        else:
            raise Exception("获取cookies失败")

    def start_requests(self):
        try:
            self.get_cookies()
            return [scrapy.Request('http://www.renren.com/969479967',
                                   headers=self.headers,
                                   cookies=self.cookies,
                                   callback=self.parse)]
        except Exception as e:
            print(e)

    def parse(self, response):
        user_name = response.xpath('//a[@class="hd-name"]/@title').extract()
        if user_name and len(user_name) > 0:
            print(user_name)
        else:
            print("Login Failed")
