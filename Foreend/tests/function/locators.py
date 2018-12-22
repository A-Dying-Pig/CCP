from selenium.webdriver.common.by import By

class BaseLocators(object):
    NonExist = (By.CLASS_NAME,'not-existed')
    BouncedMessage = (By.CLASS_NAME,'el-message__content')

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

class RegisterLocators(object):
    '''register'''
    FormButtons = (By.CLASS_NAME,'form-btn')
    FormInputs = (By.CLASS_NAME,'el-input__inner')
    AlertMessage = (By.CLASS_NAME,'el-alert__content')


class PersonalCenterLocators(object):
    '''personal center'''
    MenuContests = (By.CSS_SELECTOR,'ul.el-menu li:nth-of-type(1) span')
    MenuInfo = (By.CSS_SELECTOR, 'ul.el-menu li:nth-of-type(2) span')
    MenuMessage = (By.CSS_SELECTOR, 'ul.el-menu li:nth-of-type(3) span')
    TabParticipate = (By.CSS_SELECTOR,'div.el-tabs__nav-scroll div div#tab-1')
    TabCreate = (By.CSS_SELECTOR,'div.el-tabs__nav-scroll div div#tab-2')
    TabJudge = (By.CSS_SELECTOR, 'div.el-tabs__nav-scroll div div#tab-3')
    UploadImageButton = (By.CLASS_NAME,'el-button el-button--text el-button--small')


class CreateContest(object):
    '''create contests'''
    #比赛名称
    ContestName = (By.CSS_SELECTOR,'form#contest-info div.contest-name input')
    #举办方
    HoldersPlus = (By.CSS_SELECTOR,'button.holders-plus')
    HoldersMinus = (By.CSS_SELECTOR,'button.holders-plus')
    HoldersInputs = (By.CSS_SELECTOR,'div.contest-holders input') #s
    #承办方
    SponsorsPlus = (By.CSS_SELECTOR, 'button.sponsors-plus')
    SponsorsMinus = (By.CSS_SELECTOR, 'button.sponsors-plus')
    SponsorsInputs = (By.CSS_SELECTOR, 'div.contest-sponsors input') #s
    #比赛类型
    ContestsType = (By.CSS_SELECTOR,'div.el-radio-group.contest-type label')  #s
    #比赛图片
    ContestsImage = (By.CSS_SELECTOR,'div.avatar-uploader input')
    #比赛介绍
    BriefIntroduction = (By.CSS_SELECTOR,'div.contest-brief-intro textarea')
    DetailIntroduction = (By.CSS_SELECTOR,'div.contest-detail-intro textarea')

    #比赛报名设置
    EnrollStartTime = (By.CSS_SELECTOR,'div.contest-enroll-time input:nth-of-type(1)')
    EnrollEndTime = (By.CSS_SELECTOR,'div.contest-enroll-time input:nth-of-type(2)')

    #个人赛
    PersonalContestButton = (By.CSS_SELECTOR,'div.enroll-type label:nth-of-type(1)')
    PersonInfoPlus = (By.CSS_SELECTOR, 'button.person-info-plus')
    PersonInfoMinus = (By.CSS_SELECTOR, 'button.person-info-minus')
    PersonInfoInputs = (By.CSS_SELECTOR, 'div.contest-person-info input')  # s
    #组队赛
    GroupContestButton = (By.CSS_SELECTOR,'div.enroll-type label:nth-of-type(2)')
    GroupNumberButtons = (By.CSS_SELECTOR,'')
    GroupInfoPlus = (By.CSS_SELECTOR,'button.group-info-plus')
    GroupInfoMinus = (By.CSS_SELECTOR,'button.group-info-minus')
    GroupInfoInputs = (By.CSS_SELECTOR, 'div.contest-group-info input') #s
    #阶段赛信息
    StageAdd = (By.CSS_SELECTOR,'button.stage-plus')
    StageMinus = (By.CSS_SELECTOR,'button.stage-minus')

    StageName = (By.CSS_SELECTOR,'div.stage-name input') #s
    StageDetailInfo = (By.CSS_SELECTOR,'div.stage-info textarea') #s
    StageStartTime = (By.CSS_SELECTOR,'div.stage-start-time input') #s
    StageSubmitEndTime = (By.CSS_SELECTOR,'div.stage-submit-end-time input') #s
    StageJudgeEndTime = (By.CSS_SELECTOR,'div.stage-judge-end-time input') #s
    StageRegion_Unit = (By.CSS_SELECTOR,'div.region-select div.el-radio-group label:nth-of-type(1)') #s
    StageRegion_Province = (By.CSS_SELECTOR,'div.region-select div.el-radio-group label:nth-of-type(2)') #s
    StageRegion_Region = (By.CSS_SELECTOR,'div.region-select div.el-radio-group label:nth-of-type(3)') #s


