from selenium.webdriver.common.by import By

class IndexLocators(object):
    """index page locators."""

    Slider = (By.CLASS_NAME,'slider-image')
    SliderButton = (By.CLASS_NAME,'el-carousel__button')
    HotContests = (By.CLASS_NAME,'card_image')
    KnowUs = (By.LINK_TEXT,'了解我们')
    Services = (By.LINK_TEXT, '服务协议')


class NavigationBarLocators(object):
    '''navigation '''
    RightButton = (By.CLASS_NAME,'navi_btn_right')
    LeftButton = (By.CLASS_NAME,'navi_btn_left')


class AllContestsLocators(object):
    '''all contests'''
    ContestsButton = (By.CLASS_NAME,'super-button')
    NextPageButton = (By.CLASS_NAME,'btn-next')
    PrevPageButton = (By.CLASS_NAME,'btn-prev')
    TypeSelector = (By.CLASS_NAME,'el-radio__label')


class LoginLocators(object):
    '''login'''
    Input = (By.CLASS_NAME,'el-input__inner')
    LoginButton = (By.CLASS_NAME,'form-btn')
    CreateAccountLink = (By.CLASS_NAME,'login_register')
    NonExist = (By.CLASS_NAME,'not-existed')