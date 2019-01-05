# -*- coding: utf-8 -*-
import locators
from element import BaseInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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

    def click_message_bell(self):
        pass

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
            if len(self.driver.find_elements(*locators.AllContestsLocators.ContestsButton)) > length:
                return False
        return True


#Login
class Login(BasePage):

    def login(self,usr,pwd):
        inputs = self.driver.find_elements(*locators.LoginLocators.Input)
        BaseInput(inputs[0]).input = usr
        BaseInput(inputs[1]).input = pwd
        self.driver.find_element(*locators.LoginLocators.LoginButton).click()
        try:
            WebDriverWait(self.driver, settings.configs['MAX_WAITING_TIME']).until(
                EC.visibility_of_element_located(locators.BaseLocators.NonExist)
            )
        except:
            print('Login Wait')
        return '主页' in self.driver.title

    def click_create_new_account(self):
        self.driver.find_element(*locators.LoginLocators.CreateAccountLink).click()
        return '创建新账户' in self.driver.title


#Register
class Register(BasePage):
    def fill_form(self,eml,usr,pwd):
        forms = self.driver.find_elements(*locators.RegisterLocators.FormInputs)
        BaseInput(forms[0]).input = eml
        BaseInput(forms[1]).input = usr
        BaseInput(forms[2]).input = pwd
        BaseInput(forms[3]).input = pwd

    def click_submit(self):
        self.driver.find_elements(*locators.RegisterLocators.FormButtons)[0].click()
        element = None
        try:
            element = WebDriverWait(self.driver, settings.configs['MAX_WAITING_TIME']).until(
                EC.visibility_of_element_located(locators.RegisterLocators.AlertMessage)
            )
            print('register fail :'+ element.text)
        except:
            print('register success')
        return element or '主页' in self.driver.title

    def click_reset(self):
        self.driver.find_elements(*locators.RegisterLocators.FormButtons)[1].click()


#Personal Center
class PersonalCenter(BasePage):
    def click_menu_contests(self):
        self.driver.find_element(*locators.PersonalCenterLocators.MenuContests).click()

    def click_menu_info(self):
        self.driver.find_element(*locators.PersonalCenterLocators.MenuInfo).click()

    def click_menu_messages(self):
        self.driver.find_element(*locators.PersonalCenterLocators.MenuMessage).click()

    def click_tab_participate(self):
        self.driver.find_element(*locators.PersonalCenterLocators.TabParticipate).click()

    def click_tab_create(self):
        self.driver.find_element(*locators.PersonalCenterLocators.TabCreate).click()

    def click_tab_judge(self):
        self.driver.find_element(*locators.PersonalCenterLocators.TabJudge).click()



#Create a competition
class CreateContest(BasePage):
    def fill_contest_name(self,name):
        BaseInput(self.driver.find_element(*locators.CreateContest.ContestName)).input = name

    def fill_holders(self,names):
        length = len(names)
        for i in range(0,length - 1):
            self.driver.find_element(*locators.CreateContest.HoldersPlus).click()
        elements = self.driver.find_elements(*locators.CreateContest.HoldersInputs)
        for i in range(0,length):
            elements[i].send_keys(names[i])

    def fill_sponsors(self,names):
        length = len(names)
        if length == 0:
            return
        for i in range(0,length):
            self.driver.find_element(*locators.CreateContest.SponsorsPlus).click()
        elements = self.driver.find_elements(*locators.CreateContest.SponsorsInputs)
        for i in range(0,length):
            elements[i].send_keys(names[i])

    def choose_contest_type(self,index):
        self.driver.find_elements(*locators.CreateContest.ContestsType)[index].click()

    def upload_contest_image(self,file_path):
        self.driver.find_element(*locators.CreateContest.ContestsImage).send_keys(file_path)

    def fill_contest_intro(self,brief_intro,detail_intro):
        self.driver.find_element(*locators.CreateContest.BriefIntroduction).send_keys(brief_intro)
        self.driver.find_element(*locators.CreateContest.DetailIntroduction).send_keys(detail_intro)


    #Y-m-d H:min:S
    def fill_enroll_time(self,start_time,end_time):
        self.driver.find_element(*locators.CreateContest.EnrollStartTime).send_key(start_time)
        self.driver.find_element(*locators.CreateContest.EnrollStartTime).send_key(end_time)

    def set_contest_type_person(self):
        self.driver.find_element(*locators.CreateContest.PersonalContestButton).click()

    def set_contest_type_group(self):
        self.driver.find_element(*locators.CreateContest.GroupContestButton).click()

    def fill_person_needed_info(self,info):
        length = len(info)
        if length == 0:
            return
        for i in range(0, length - 1):
            self.driver.find_element(*locators.CreateContest.PersonInfoPlus).click()
        elements = self.driver.find_elements(*locators.CreateContest.PersonInfoInputs)
        for i in range(0, length):
            elements[i].send_keys(info[i])



#pass a competition
class Superadmin(BasePage):
    pass


#Enroll a competition
class Enroll(BasePage):
    pass











