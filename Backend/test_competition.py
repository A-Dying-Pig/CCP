from django.test import TransactionTestCase,TestCase
from django.test import Client
from .models import *
import json
from django.http import HttpRequest
#import .api_user

class api_user_competiton_Test(TestCase):
    def setUp(self):
        self.c=Client()
        #用户登录和比赛创建
        CCPUser.objects.create_superuser(username='super_admin',password='ccp',email='zyj@126.com')
        user_info={      
            "username": "admin", 
            "password": "ccp",
            "email":"zyj123@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={      
            "username": "admin2", 
            "password": "ccp",
            "email":"zyj2@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={      
            "username": "admin3", 
            "password": "ccp",
            "email":"zyj3@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        modify_info={      
            "university": "清华大学", 
            "region":{
                "province":"北京",
                "city":"北京"
            }
        }
        response = self.c.post('/api/user/modify',json.dumps(modify_info),content_type="application/json")
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛-个人",
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-30T12:10:00.000Z","2019-12-30T12:10:00.000Z"],
                "mode" : 1,
                "person" : ["1","2","3","4"],
                "group" : ["1","2","3","4"],
            },
            "stageinfo":
                [{"name" : "1",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode":0}]
        }
        response = self.c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        contest = Contest.objects.filter()
        self.contestId_personal = contest[0].id

        #组队赛
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛-组队",
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-30T12:10:00.000Z","2019-12-30T12:10:00.000Z"],
                "mode" : 0,
                "person" : ["1","2","3","4"],
                "group" : ["1","2","3","4"],
            },
            "stageinfo":
                [{"name" : "1",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0}]
        }
        response = self.c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        contest = Contest.objects.filter()
        self.contestId_group = contest[1].id
        '''
        print('-------------------------------')
        print('id='+str(contest[0].id))
        print('len(contests)='+str(len(contest)))
        '''        
    def test_enroll_personal(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        comp_info = {
            "contestid": self.contestId_personal,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : [],            
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_enroll_group(self): 
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_group,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : ["admin3"],
            "custom_field" : ["1","2"],
            "custom_value" : ['1',"2"],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_enroll_group_onePerson(self): 
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_group,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : [],
            "custom_field" : ["1","2"],
            "custom_value" : ['1',"2"],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_enroll_personal_twoPeople(self): 
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : ["admin3"],
            "custom_field" : ["1","2"],
            "custom_value" : ['1',"2"],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_enroll_group_membernotexist(self): 
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_group,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : ["admin4"],
            "custom_field" : ["1","2"],
            "custom_value" : ['1',"2"],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '参赛队员不存在') 

    def test_enroll_admin(self):       
        comp_info = {
            "contestid": self.contestId_personal,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : [],
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '比赛主办方不能报名成为比赛选手')

    def test_enroll_judge(self):
        user_info={      
            "username": "judge1", 
            "password": "ccp",
            "email":"judge1@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_personal, 
            "type":0,
            "username": "judge1",
            "id":'1'                 
        }
        response = self.c.post('/api/admin/setjudge',json.dumps(comp_info),content_type="application/json") 
        comp_info = {
            "contestid": self.contestId_personal,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : [],
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '比赛评委不能报名成为比赛选手')

    def test_enroll_super(self):
        user_info={
            "username": "super_admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : [],
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '超级管理员不能报名成为比赛选手')

    def test_neededinfo_successful(self):
        contest = Contest.objects.filter()
        comp_info = {
            "contestid": self.contestId_personal
            }            
        response = self.c.post('/api/competition/neededinfo',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_neededinfo_wrong(self):
        comp_info = {
            "contestid": self.contestId_group+1
            }            
        response = self.c.post('/api/competition/neededinfo',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '您所要查找的信息不存在！')    

    def test_list_successful(self):
        comp_info = {
            "pageNum": 1,
            "type":"趣味比赛"
            }            
        response = self.c.post('/api/competition/list',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['total_page_num'], 1)
        self.assertEqual(response_content['current_page_num'], 1)
        self.assertEqual(len(response_content['array']), 1)
    

    def test_list_typewrong(self):
        comp_info = {
            "pageNum": 1,
            "type":"1"
            }            
        response = self.c.post('/api/competition/list',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['total_page_num'], 0)
        self.assertEqual(response_content['current_page_num'], 0)
        self.assertEqual(len(response_content['array']), 0)


    def test_list_numberOverflow(self):
        comp_info = {
            "pageNum": 2,
            "type":"趣味比赛"
            }            
        response = self.c.post('/api/competition/list',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['total_page_num'], 1)
        self.assertEqual(response_content['current_page_num'], 2)
        self.assertEqual(len(response_content['array']), 0)

    def test_detail_no_relation(self):        
        user_info={      
            "username": "admin2", 
            "password": "ccp",
            "email":"zyj2@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")     
        comp_info = {
            "contestid": self.contestId_personal
            }            
        response = self.c.post('/api/competition/detail',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['info']['basicinfo']['name'], "快乐肥宅大赛")
        self.assertEqual(response_content['type'], 0)

    def test_detail_participant(self):
        user_info={      
            "username": "admin2", 
            "password": "ccp",
            "email":"zyj1@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")     
        comp_info = {
            "contestid": self.contestId_personal,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : [],
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal
            }            
        response = self.c.post('/api/competition/detail',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['info']['basicinfo']['name'], "快乐肥宅大赛")
        self.assertEqual(response_content['type'], 1)

    '''
    def test_detail_judge(self):
        user_info={      
            "username": "admin2", 
            "password": "ccp",
            "email":"zyj1@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")     
        comp_info = {
            "contestid": self.contestId,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : ["admin"],
            "comp_type" : 1,
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId
            }            
        response = self.c.post('/api/competition/detail',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        print(response_content)
        self.assertEqual(response_content['info']['basicinfo']['name'], "快乐肥宅大赛")
        self.assertEqual(response_content['type'], 2)
    '''

    def test_detail_admin(self):
        comp_info = {
            "contestid": self.contestId_personal
            }            
        response = self.c.post('/api/competition/detail',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['info']['basicinfo']['name'], "快乐肥宅大赛")
        self.assertEqual(response_content['type'], 3)

    def test_detail_wrong(self):
        comp_info = {
            "contestid": self.contestId_group+1
            }            
        response = self.c.post('/api/competition/detail',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "未知错误！")

    def test_super_contests_successful(self):
        user_info={
            "username": "super_admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "pageNum": 1
            }            
        response = self.c.post('/api/super/contests',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "")
        self.assertEqual(len(response_content['array']), 1)

    def test_user_contests_wrong(self):
        comp_info = {
            "pageNum": 1
            }            
        response = self.c.post('/api/super/contests',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "Authority denied.")

    def test_super_contests_pageNumOverflow(self):
        user_info={
            "username": "super_admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "pageNum": 2
            }            
        response = self.c.post('/api/super/contests',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "")
        self.assertEqual(len(response_content['array']), 0)

    def test_super_submit_pass(self):
        user_info={
            "username": "super_admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "pass": 1
            }            
        response = self.c.post('/api/super/submit',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "")

    def test_super_submit_notpass(self):
        user_info={
            "username": "super_admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "pass": 0
            }            
        response = self.c.post('/api/super/submit',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "")
        
    def test_super_detail_successful(self):
        user_info={
            "username": "super_admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_group
            }            
        response = self.c.post('/api/super/detail',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "")
        self.assertEqual(response_content['basicinfo']['name'], "快乐肥宅大赛")

    def test_super_detail_alreadycontest(self):
        user_info={
            "username": "super_admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_group,
            "pass": 1
            }            
        response = self.c.post('/api/super/submit',json.dumps(comp_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_group
            }            
        response = self.c.post('/api/super/detail',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "该比赛不是未审核状态")

    def test_competition_enrollnum_admin(self):
        user_info={      
            "username": "admin2", 
            "password": "ccp",
            "email":"zyj2@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : [],
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")        
        comp_info={
            "contestid": self.contestId_personal
        }
        response = self.c.post('/api/competition/enrollnum',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "")
        self.assertEqual(response_content['enrollnum'],1)

    def test_competition_enrollnum_player(self):
        user_info={      
            "username": "admin2", 
            "password": "ccp",
            "email":"zyj2@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : [],
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        comp_info={
            "contestid": self.contestId_personal
        }
        response = self.c.post('/api/competition/enrollnum',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "")
        self.assertEqual(response_content['enrollnum'],1)

    def test_competition_enrollnum_user(self):
        user_info={      
            "username": "admin2", 
            "password": "ccp",
            "email":"zyj2@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : [],
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        user_info={
            "username": "admin3", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info={
            "contestid": self.contestId_personal
        }
        response = self.c.post('/api/competition/enrollnum',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "")
        self.assertEqual(response_content['enrollnum'],1)

    def test_competition_enrollnum_nobodyEnroll(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")        
        comp_info={
            "contestid": self.contestId_personal
        }
        response = self.c.post('/api/competition/enrollnum',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "")
        self.assertEqual(response_content['enrollnum'],0)

    def test_competition_enrollnum_compNotexist(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")        
        comp_info={
            "contestid": self.contestId_group+1
        }
        response = self.c.post('/api/competition/enrollnum',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "比赛不存在")

    def test_slider_0(self):
        response = self.c.post('/api/competition/slider')     
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(len(response_content['array']), 0)
    
    def test_slider_1(self):
        user_info={
            "username": "super_admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        comp_info = {
            "slider":[self.contestId_personal], 
            "hot":[self.contestId_personal]
        }
        response = self.c.post('/api/super/setindex',json.dumps(comp_info),content_type="application/json") 
        response = self.c.post('/api/competition/slider')     
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(len(response_content['array']), 1)    

    def test_hot_0(self):
        response = self.c.post('/api/competition/hot')     
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(len(response_content['array']), 0)

    def test_hot_1(self):
        user_info={
            "username": "super_admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        comp_info = {
            "slider":[self.contestId_personal], 
            "hot":[self.contestId_personal]
        }
        response = self.c.post('/api/super/setindex',json.dumps(comp_info),content_type="application/json") 
        response = self.c.post('/api/competition/hot')     
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(len(response_content['array']), 1)    

class api_user_competiton_Test(TransactionTestCase):
    def setUp(self):
        self.c=Client()
        #用户登录和比赛创建
        CCPUser.objects.create_superuser(username='super_admin',password='ccp',email='zyj@126.com')
        user_info={      
            "username": "admin", 
            "password": "ccp",
            "email":"zyj123@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={      
            "username": "admin2", 
            "password": "ccp",
            "email":"zyj2@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={      
            "username": "admin3", 
            "password": "ccp",
            "email":"zyj3@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        modify_info={      
            "university": "清华大学", 
            "region":{
                "province":"北京",
                "city":"北京"
            }
        }
        response = self.c.post('/api/user/modify',json.dumps(modify_info),content_type="application/json")
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛-个人",
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-30T12:10:00.000Z","2019-12-30T12:10:00.000Z"],
                "mode" : 1,
                "person" : ["1","2","3","4"],
                "group" : ["1","2","3","4"],
            },
            "stageinfo":
                [{"name" : "1",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode":0}]
        }
        response = self.c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        contest = Contest.objects.filter()
        self.contestId_personal = contest[0].id

    def test_competition_adddiscussion_admin(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_competition_adddiscussion_player(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        comp_info = {
            "contestid": self.contestId_personal,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : [],            
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        comp_info={
            "contestid":self.contestId_personal,
            "title":"提问",
            "content":"hhhhh"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_competition_adddiscussion_user(self):
        user_info={
            "username": "admin3", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        comp_info={
            "contestid":self.contestId_personal,
            "title":"提问",
            "content":"hhhhh"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_competition_adddiscussion_compNotexist(self):
        comp_info={
            "contestid":self.contestId_personal+1,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '未知错误')

    def test_competition_adddiscussion_emptycontent(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"",
            "content":""
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '发帖内容不能为空')

    def test_competition_discussionreply_admin(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        discussion = Post.objects.filter()
        self.contestId_discussionid = discussion[0].id
        comp_info={
            "contestid":self.contestId_personal,
            "discussionid":self.contestId_discussionid,
            "content":"大家注意初赛时间",
            "replytime":"2018-12-30T12:10:00.000Z"
        }
        response = self.c.post('/api/competition/discussionreply',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_competition_discussionreply_player(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        comp_info = {
            "contestid": self.contestId_personal,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : [],            
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        discussion = Post.objects.filter()
        self.contestId_discussionid = discussion[0].id
        comp_info={
            "contestid":self.contestId_personal,
            "discussionid":self.contestId_discussionid,
            "content":"大家注意初赛时间",
            "replytime":"2018-12-30T12:10:00.000Z"
        }
        response = self.c.post('/api/competition/discussionreply',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_competition_discussionreply_user(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        user_info={
            "username": "admin3", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        discussion = Post.objects.filter()
        self.contestId_discussionid = discussion[0].id
        comp_info={
            "contestid":self.contestId_personal,
            "discussionid":self.contestId_discussionid,
            "content":"大家注意初赛时间",
            "replytime":"2018-12-30T12:10:00.000Z"
        }
        response = self.c.post('/api/competition/discussionreply',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_competition_discussionreply_compNotexist(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        discussion = Post.objects.filter()
        self.contestId_discussionid = discussion[0].id
        comp_info={
            "contestid":self.contestId_personal+1,
            "discussionid":self.contestId_discussionid,
            "content":"大家注意初赛时间",
            "replytime":"2018-12-30T12:10:00.000Z"
        }
        response = self.c.post('/api/competition/discussionreply',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '比赛不存在')

    def test_competition_discussionreply_discussNotexist(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        discussion = Post.objects.filter()
        self.contestId_discussionid = discussion[0].id
        comp_info={
            "contestid":self.contestId_personal,
            "discussionid":self.contestId_discussionid+1,
            "content":"大家注意初赛时间",
            "replytime":"2018-12-30T12:10:00.000Z"
        }
        response = self.c.post('/api/competition/discussionreply',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '主题帖不存在')

    def test_competition_discussionreply_empty(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        discussion = Post.objects.filter()
        self.contestId_discussionid = discussion[0].id
        comp_info={
            "contestid":self.contestId_personal,
            "discussionid":self.contestId_discussionid,
            "content":"",
            "replytime":"2018-12-30T12:10:00.000Z"
        }
        response = self.c.post('/api/competition/discussionreply',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '回复内容不能为空')

    def test_competition_discussionlist_admin(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        comp_info={
            "pageNum":1,
            "contestid":self.contestId_personal            
        }
        response = self.c.post('/api/competition/discussionlist',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')
        self.assertEqual(response_content['array'][0]['title'],'初赛时间')

    def test_competition_discussionlist_player(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        comp_info = {
            "contestid": self.contestId_personal,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : [],            
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        comp_info={
            "pageNum":1,
            "contestid":self.contestId_personal            
        }
        response = self.c.post('/api/competition/discussionlist',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')
        self.assertEqual(response_content['array'][0]['title'],'初赛时间')

    def test_competition_discussionlist_user(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        user_info={
            "username": "admin3", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        comp_info={
            "pageNum":1,
            "contestid":self.contestId_personal            
        }
        response = self.c.post('/api/competition/discussionlist',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')
        self.assertEqual(response_content['array'][0]['title'],'初赛时间')

    def test_competition_discussionlist_compNotexist(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        user_info={
            "username": "admin3", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        comp_info={
            "pageNum":1,
            "contestid":self.contestId_personal+1            
        }
        response = self.c.post('/api/competition/discussionlist',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '未知错误')

    def test_competition_discussion_admin(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        print("++++++++++++++")
        print(response_content['msg'])
        print("++++++++++++++")
        discussion = Post.objects.filter()
        print("===========")
        print(self.contestId_discussionid)   
        print("===========") 
        self.contestId_discussionid = discussion[0].id   
        comp_info={
            "contestid":self.contestId_personal,
            "discussionid":self.contestId_discussionid,
            "pageNum":1            
        }
        response = self.c.post('/api/competition/discussion',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')
        self.assertEqual(response_content['title'],'初赛时间')
        self.assertEqual(len(response_content['array']),0)

    def test_competition_discussion_player(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        comp_info = {
            "contestid": self.contestId_personal,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : [],            
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        discussion = Post.objects.filter()
        self.contestId_discussionid = discussion[0].id        
        comp_info={
            "contestid":self.contestId_personal,
            "discussionid":self.contestId_discussionid,
            "pageNum":1            
        }
        response = self.c.post('/api/competition/discussion',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')
        self.assertEqual(response_content['title'],'初赛时间')
        self.assertEqual(len(response_content['array']),0)

    def test_competition_discussion_user(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        user_info={
            "username": "admin3", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        discussion = Post.objects.filter()
        self.contestId_discussionid = discussion[0].id        
        comp_info={
            "contestid":self.contestId_personal,
            "discussionid":self.contestId_discussionid,
            "pageNum":1            
        }
        response = self.c.post('/api/competition/discussion',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')
        self.assertEqual(response_content['title'],'初赛时间')
        self.assertEqual(len(response_content['array']),0)

    def test_competition_discussionlist_compNotexist(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        user_info={
            "username": "admin3", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        discussion = Post.objects.filter()
        self.contestId_discussionid = discussion[0].id        
        comp_info={
            "contestid":self.contestId_personal+1,
            "discussionid":self.contestId_discussionid,
            "pageNum":1            
        }
        response = self.c.post('/api/competition/discussion',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '比赛与主题帖不匹配')

    def test_competition_discussionlist_discussNotexist(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"大家注意初赛时间"
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        user_info={
            "username": "admin3", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        discussion = Post.objects.filter()
        self.contestId_discussionid = discussion[0].id        
        comp_info={
            "contestid":self.contestId_personal,
            "discussionid":self.contestId_discussionid+1,
            "pageNum":1            
        }
        response = self.c.post('/api/competition/discussion',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '主题帖不存在')

    '''
    def test_competition_worksname(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        comp_info = {
            "contestid": self.contestId_personal,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : [],            
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        submit_info={
            "contestid":self.contestId_personal,
            "file": "C:\\Users\\Administrator\\Desktop\\1.txt" 
        }
        response = self.c.post('/api/contestant/submit',json.dumps(submit_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal
        }
        response = self.c.post('/api/competition/worksname',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')
        self.assertEqual(response_content['filename'])
    '''









