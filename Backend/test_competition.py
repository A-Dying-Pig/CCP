from django.test import TransactionTestCase,TestCase
from django.test import Client
from .models import *
import json
from django.http import HttpRequest
import os, sys
from .utils import *
import shutil
#import .api_user

class api_user_competiton_Test(TestCase):
    def setUp(self):
        self.c=Client()
        #用户登录和比赛创建
        #CCPUser.objects.create_superuser(username='super_admin',password='ccp',email='zyj@126.com')
        user_info={      
            "username": "super_admin", 
            "password": "ccp",
            "email":"zyj@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        CCPUser.objects.all().update(is_superuser=True)

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
        with open("C:\\Users\\Administrator\\Desktop\\1.jpg", 'rb') as f:
            response=self.c.post('/api/competition/uploadimg',{'file': f})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        url=response_content['url']
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛-个人",
                "img" : url,
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "web开发",
                "judgebegin" : False,
                "briefintroduction":"hhhh",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-10T12:10:00.000Z","2019-12-30T12:10:00.000Z"],
                "mode" : 1,
                "teamnum":5,
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
        contest = Contest.objects.filter(title="快乐肥宅大赛-个人")
        #print(contest[0].id)
        self.contestId_personal = contest[0].id

        #组队赛
        with open("C:\\Users\\Administrator\\Desktop\\1.jpg", 'rb') as f:
            response=self.c.post('/api/competition/uploadimg',{'file': f})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        url=response_content['url']
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛-组队",
                "img" : url,
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "web开发",
                "judgebegin" : 0,
                "briefintroduction":"hhhh",
                "details" : "hhhhhhhh"
                },        
            "signupinfo": {
                "time" : ["2018-12-10T12:10:00.000Z","2019-12-30T12:10:00.000Z"],
                "mode" : 0,
                "teamnum":5,
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
        contest = Contest.objects.filter(title='快乐肥宅大赛-组队')
        self.contestId_group = contest[0].id  

    def tearDown(self):
        dirs = os.listdir(RESOURCE_BASE_DIR + '/resources/contests')
        for file in dirs:
           shutil.rmtree(RESOURCE_BASE_DIR + '/resources/contests/'+file)
        dirs = os.listdir(RESOURCE_BASE_DIR + '/resources/users')
        for file in dirs:
           shutil.rmtree(RESOURCE_BASE_DIR + '/resources/users/'+file)

    def test_enroll_personal(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        comp_info = {
            "contestid": self.contestId_personal,
            "phone_number": 18001136323,
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
            "phone_number": 18001136323,
            "username":"admin2",
            "university" : "清华大学",
            "groupuser" : ["admin3"],
            "groupname":"hhh战队",
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
            "phone_number": 18001136323,
            "region":{
                "province" : "北京",
                "city" : "北京",                
                },
            "university" : "清华大学",
            "groupuser" : [],
            "groupname":"hhh战队",
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
            "phone_number": 18001136323,
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
            "phone_number": 18001136323,
            "region":{
                "province" : "北京",
                "city" : "北京"                
                },
            "university" : "清华大学",
            "groupuser" : ["admin4"],
            "groupname":"hhh战队",
            "custom_field" : ["1","2"],
            "custom_value" : ['1',"2"],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '未知错误') 

    def test_enroll_admin(self):       
        comp_info = {
            "contestid": self.contestId_personal,
            "phone_number": 18001136323,
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
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "phone_number": 18001136323,
            "university" : "清华大学",
            "groupuser" : [],
            "custom_field" : ["1"],
            "custom_value" : ['1']
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '比赛评委不能报名成为比赛选手')

    def test_enroll_repeated(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")           
        comp_info = {
            "contestid": self.contestId_personal,
            "phone_number": 18001136323,
            "university" : "清华大学",
            "groupuser" : [],            
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "phone_number": 18001136323,
            "university" : "清华大学",
            "groupuser" : [],
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '不能重复报名')

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
        comp_info = {
            "contestid": self.contestId_group,
            "pass": 1
            }            
        response = self.c.post('/api/super/submit',json.dumps(comp_info),content_type="application/json")
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "pageNum": 1,
            "type":"web"
            }            
        response = self.c.post('/api/competition/list',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)

        contest = Contest.objects.filter(title='快乐肥宅大赛-个人')        
        self.contest1 = contest[0].checked
        contest = Contest.objects.filter(title='快乐肥宅大赛-组队')        
        self.contest2 = contest[0].checked
        #print("--------比赛列表--------")
        #print(self.contest1)
        #print(self.contest2)
        #print("--------比赛列表--------")

        self.assertEqual(response_content['total_page_num'], 1)
        self.assertEqual(response_content['current_page_num'], 1)
        self.assertEqual(len(response_content['array']), 2)
    

    def test_list_typewrong(self):
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
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "pageNum": 1,
            "type":"1"
            }            
        response = self.c.post('/api/competition/list',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "不存在的比赛类型")


    def test_list_numberOverflow(self):
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
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "pageNum": 2,
            "type":"web",
            }            
        response = self.c.post('/api/competition/list',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['total_page_num'], 1)
        self.assertEqual(response_content['current_page_num'], 2)
        self.assertEqual(len(response_content['array']), 0)

    def test_detail_no_relation(self):        
        #print("test_detail_no_relation")
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
        self.assertEqual(response_content['info']['basicinfo']['name'], "快乐肥宅大赛-个人")
        self.assertEqual(response_content['type'], 0)

    def test_detail_participant(self):
        #print("test_detail_participant")
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")     
        comp_info = {
            "contestid": self.contestId_personal,
            "phone_number": 18001136323,
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
        self.assertEqual(response_content['info']['basicinfo']['name'], "快乐肥宅大赛-个人")
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
        #print("test_detail_admin")
        comp_info = {
            "contestid": self.contestId_personal
            }            
        response = self.c.post('/api/competition/detail',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        #print(response_content)
        self.assertEqual(response_content['info']['basicinfo']['name'], "快乐肥宅大赛-个人")
        self.assertEqual(response_content['type'], 3)

    '''
    def test_detail_wrong(self):
        #print("test_detail_wrong")
        comp_info = {
            "contestid": self.contestId_group+1
            }            
        response = self.c.post('/api/competition/detail',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "未知错误！")
    '''

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
        self.assertEqual(len(response_content['array']), 2)

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

    def test_super_contests_passOne(self):
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
        comp_info = {
            "pageNum": 1
            }            
        response = self.c.post('/api/super/contests',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "")
        self.assertEqual(len(response_content['array']), 1)

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
        #print("test_super_detail_successful")
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
        self.assertEqual(response_content['basicinfo']['name'], "快乐肥宅大赛-组队")

    def test_super_detail_alreadycontest(self):
        #print("test_super_detail_alreadycontest")
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
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "phone_number": 18001136323,
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
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "phone_number": 18001136323,
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
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "phone_number": 18001136323,
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

    def test_competition_enrollnum_logout(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "phone_number": 18001136323,
            "university" : "清华大学",
            "groupuser" : [],
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        response = self.c.post('/logout')        
        comp_info={
            "contestid": self.contestId_personal
        }
        response = self.c.post('/api/competition/enrollnum',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "")
        self.assertEqual(response_content['enrollnum'],1)

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

