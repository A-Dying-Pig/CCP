# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
import page
import settings


# class TestIndexPage(unittest.TestCase):
#     '''测试了主页功能'''
#
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(settings.configs['MAX_WAITING_TIME'])  # seconds
#         self.driver.get(settings.configs['BASE_URL'])
#         self.index_page = page.IndexPage(self.driver)
#         self.navigation_bar = page.NavigationBar(self.driver)
#
#     def test_index_page(self):
#         '''访问:主页'''
#         assert self.index_page.is_title_matches(), "CCP-主页-访问失败"
#
#     def test_about_page_know_us(self):
#         '''访问:了解我们'''
#         assert self.index_page.click_about_know_us(), "CCP-了解我们-访问失败"
#
#     def test_about_page_services(self):
#         '''访问:服务协议'''
#         assert self.index_page.click_about_services(), "CCP-服务协议-访问失败"
#
#     def test_slider(self):
#         '''测试轮播图'''
#         assert self.index_page.click_slider_image(), "CCP-主页-轮播图点击错误"
#
#     def test_hot_contests(self):
#         '''测试热门比赛'''
#         assert self.index_page.click_hot_contests(), "CCP-主页-热门比赛点击错误"
#
#     def test_navigation_bar(self):
#         assert self.navigation_bar.click_all_btns(), "CCP-导航栏错误"
#
#     def tearDown(self):
#         self.driver.close()
#

# class TestAllCompetition(unittest.TestCase):
#     '''测试比赛列表'''
#
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(settings.configs['MAX_WAITING_TIME'])  # seconds
#         self.driver.get(settings.configs['BASE_URL'])
#         self.navigation_bar = page.NavigationBar(self.driver)
#         self.contests = page.AllContests(self.driver)
#         self.navigation_bar.click_all_contests()
#
#
#     def test_contests_list(self):
#         '''点击当前页面所有比赛'''
#         assert self.contests.click_type(),"CCP-全部比赛-选择比赛类型出错"
#         assert self.contests.click_current_page(),"CCP-全部比赛-某些比赛查看详情失败"
#         assert self.contests.click_next_page(), "CCP-全部比赛-下一页错误"
#         assert self.contests.click_current_page(), "CCP-全部比赛-某些比赛查看详情失败"
#         assert self.contests.click_prev_page(), "CCP-全部比赛-上一页错误"
#         assert self.contests.click_current_page(), "CCP-全部比赛-某些比赛查看详情失败"
#
#     def tearDown(self):
#         self.driver.close()


class TestLogin(unittest.TestCase):
    '''测试登录比赛'''

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(settings.configs['MAX_WAITING_TIME'])  # seconds
        self.driver.get(settings.configs['BASE_URL'])
        self.login_page = page.Login(self.driver)
        self.navigation_bar = page.NavigationBar(self.driver)
        if self.navigation_bar.is_login():
            self.navigation_bar.click_register()
        self.navigation_bar.click_login()

    def test_user_login(self):
        assert self.login_page.login(settings.configs['PARTICIPANT_USERNAME'],settings.configs['PARTICIPANT_PASSWORD']),\
                "CCP-用户登录失败"
        self.driver.get(settings.configs['SUPERADMIN_URL'])
        assert "信息" in self.driver.title, "CCP-普通用户权限出错-可以进入超级管理员页面"

    def test_superadmin_login(self):
        self.login_page.login(settings.configs['SUPERUSER_USERNAME'],settings.configs['SUPERUSER_PASSWORD']),
        self.driver.get(settings.configs['SUPERADMIN_URL'])
        assert "超级管理员" in self.driver.title, "CCP-超级管理员权限出错-无法进入超级管理员页面"

    def test_create_new_account(self):
        assert self.login_page.click_create_new_account(), "CCP-登录-创建新账户链接错误"

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
