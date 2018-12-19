# -*- coding: utf-8 -*-
import locators
from element import BaseInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import settings

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver

#Index Page
class IndexPage(BasePage):
    """CCP Index page action methods come here."""

    def is_title_matches(self):
        """Verifies that the hardcoded text "主页" appears in page title"""
        return "主页" in self.driver.title

    def click_slider_image(self):
        length = len(self.driver.find_elements(*locators.IndexLocators.Slider))
        for i in range(0,length):
            self.driver.find_elements(*locators.IndexLocators.Slider)[i].click()
            if "CCP大学生竞赛平台" not in self.driver.title:
                return False
            self.driver.back()
        return True

    def click_hot_contests(self):
        length = len(self.driver.find_elements(*locators.IndexLocators.HotContests))
        for i in range(0,length):
            self.driver.find_elements(*locators.IndexLocators.HotContests)[i].click()
            if "CCP大学生竞赛平台" not in self.driver.title:
                return False
            self.driver.back()
        return True

    def click_about_know_us(self):
        self.driver.find_element(*locators.IndexLocators.KnowUs).click()
        return '信息' in self.driver.title

    def click_about_services(self):
        self.driver.find_element(*locators.IndexLocators.Services).click()
        return '信息' in self.driver.title

#NavagationBar
class NavigationBar(BasePage):

    def is_login(self):
        return self.driver.find_element(*locators.NavigationBarLocators.RightButton).text != '登录'

    def click_index(self):
        self.driver.find_elements(*locators.NavigationBarLocators.LeftButton)[0].click()
        return '主页' in self.driver.title

    def click_all_contests(self):
        self.driver.find_elements(*locators.NavigationBarLocators.LeftButton)[1].click()
        return '比赛列表' in self.driver.title

    def click_personal_center(self):
        self.driver.find_elements(*locators.NavigationBarLocators.LeftButton)[2].click()
        if self.is_login():
            return '个人中心' in self.driver.title
        else:
            return '登录' in self.driver.title

    def click_create_contest(self):
        self.driver.find_elements(*locators.NavigationBarLocators.LeftButton)[3].click()
        if self.is_login():
            return '创建比赛' in self.driver.title
        else:
            return '登录' in self.driver.title

    def click_login(self):
        self.driver.find_elements(*locators.NavigationBarLocators.RightButton)[0].click()
        if not self.is_login():
            return '登录' in self.driver.title
        else:
            return '个人中心' in self.driver.title

    def click_register(self):
        self.driver.find_elements(*locators.NavigationBarLocators.RightButton)[1].click()
        if not self.is_login():
            return '创建新账户' in self.driver.title
        else:
            return '主页' in self.driver.title

    def click_all_btns(self):
        return self.click_index() and self.click_all_contests() and self.click_personal_center() \
               and self.click_create_contest() and self.click_login() and self.click_register()


#Contests List
class AllContests(BasePage):
    def click_current_page(self):
        length = len(self.driver.find_elements(*locators.AllContestsLocators.ContestsButton))
        for i in range(0,length):
            self.driver.find_elements(*locators.AllContestsLocators.ContestsButton)[i].click()
            if "CCP大学生竞赛平台" not in self.driver.title:
                return False
            self.driver.back()
        return True

    def click_next_page(self):
        self.driver.find_element(*locators.AllContestsLocators.NextPageButton).click()
        return '比赛列表' in self.driver.title

    def click_prev_page(self):
        self.driver.find_element(*locators.AllContestsLocators.PrevPageButton).click()
        return '比赛列表' in self.driver.title

    def click_type(self):
        length = len(self.driver.find_elements(*locators.AllContestsLocators.ContestsButton))
        elements = self.driver.find_elements(*locators.AllContestsLocators.TypeSelector)
        for element in elements:
            element.click()
            if(len(self.driver.find_elements(*locators.AllContestsLocators.ContestsButton)) > length):
                return False
        return True


#Login

class Login(BasePage):

    def login(self,usr,pwd):
        inputs = self.driver.find_elements(*locators.LoginLocators.Input)
        username = BaseInput(inputs[0])
        password = BaseInput(inputs[1])
        username.input = usr
        password.input = pwd
        self.driver.find_element(*locators.LoginLocators.LoginButton).click()
        try:
            WebDriverWait(self.driver, settings.configs['MAX_WAITING_TIME']).until(
                EC.visibility_of_element_located(locators.LoginLocators.NonExist)
            )
        except:
            print('Login Wait')
        return '主页' in self.driver.title

    def click_create_new_account(self):
        self.driver.find_element(*locators.LoginLocators.CreateAccountLink).click()
        return '创建新账户' in self.driver.title

