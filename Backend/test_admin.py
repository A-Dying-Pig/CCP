from django.test import TestCase
from django.test import Client
from .models import *
import json
from django.http import HttpRequest
#import .api_user

# Create your tests here.
#test api_user
class api_user_competiton_Test(TestCase):
    def setUp(self):
        self.c=Client()
        #用户登录和比赛创建 比赛报名
        CCPUser.objects.create_superuser(username='super_admin',password='ccp',email='zyj@126.com')
        user_info={      
            "username": "admin", 
            "password": "ccp",
            "email":"zyj123@126.com"
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
                "name" : "快乐肥宅大赛",
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-30T12:10:00.000Z","2019-12-30T12:10:00.000Z"],
                "mode" : 1,
                "person" : ["1","2","3","4"],
                "group" : [],
            },
            "stageinfo":
                [{"name" : "1",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0}]
        }
        response = self.c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        contest = Contest.objects.filter()
        self.contestId_personal = contest[0].id

        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛",
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-30T12:10:00.000Z","2019-12-30T12:10:00.000Z"],
                "mode" : 0,
                "person" : [],
                "group" : ["1","2","3","4"],
            },
            "stageinfo":
                [{"name" : "1",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0}]
        }
        response = self.c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        contest = Contest.objects.filter()
        self.contestId_group = contest[1].id

        #个人报名
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

        #组队报名
        user_info={      
            "username": "admin3", 
            "password": "ccp",
            "email":"zyj3@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={      
            "username": "admin4", 
            "password": "ccp",
            "email":"zyj4@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "admin3", 
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
        '''
        print('-------------------------------')
        print('id='+str(contest[0].id))
        print('len(contests)='+str(len(contest)))
        '''
        
    def test_participants_personal(self): 
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        comp_info = {
            "contestid":self.contestId_personal,
            "pageNum": 1
        }
        response = self.c.post('/api/admin/participants',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        print(response_content)
        self.assertEqual(response_content['mode'], 1)  
        self.assertEqual(len(response_content['array']),1)
        self.assertEqual(response_content['array'][0]['username'],'admin')

    def test_participants_group(self):   
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json") 
        comp_info = {
            "contestid":self.contestId_group,
            "pageNum": 1
        }
        response = self.c.post('/api/admin/participants',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['mode'], 0)  
        self.assertEqual(len(response_content['array']),1)
        self.assertEqual(response_content['array']['captainName'],'admin2')
        self.assertEqual(len(response_content['array'][0]['group']),2)

    def test_participants_notadmin(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_personal,
            "pageNum": 1
        }
        response = self.c.post('/api/admin/participants',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Current user is not the admin of this contest')  
       
    def test_participants_overflow(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_personal,
            "pageNum": 2
        }
        response = self.c.post('/api/admin/participants',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['mode'], 0)  
        self.assertEqual(len(response_content['array']),0)
        self.assertEqual(response_content['current_page_num'],2)

    def test_participants_notexist(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_group+1,
            "pageNum": 1
        }
        response = self.c.post('/api/admin/participants',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Contest does not exist.')

    def test_detail_personal(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_personal            
        }
        response = self.c.post('/api/admin/detail',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['basicinfo']['name'], "快乐肥宅大赛")  
        self.assertEqual(response_content['basicinfo']['comtype'],1)

    def test_detail_group(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_group            
        }
        response = self.c.post('/api/admin/detail',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['basicinfo']['name'], "快乐肥宅大赛")  
        self.assertEqual(response_content['basicinfo']['comtype'],0)

    def test_detail_notexist(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_group+1            
        }
        response = self.c.post('/api/admin/detail',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Contest does not exist.')  

    def test_detail_notadmin(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_personal            
        }
        response = self.c.post('/api/admin/detail',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Current user is not the admin of this contest')

    def test_modify_personal(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_personal,   
            "basicinfo": {
                "name" : "快乐肥宅大赛1",
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-30T12:10:00.000Z","2019-12-30T12:10:00.000Z"],
                "mode" : 1,
                "person" : ["1","2","3","4"],
                "group" : [],
            },
            "stageinfo":
                [{"name" : "1",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0}]         
        }
        response = self.c.post('/api/admin/modify',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "") 

    def test_modify_group(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_group,   
            "basicinfo": {
                "name" : "快乐肥宅大赛",
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-30T12:10:00.000Z","2019-12-30T12:10:00.000Z"],
                "mode" : 0,
                "person" : ["1","2","3","4"],
                "group" : ["1","2","3"],
            },
            "stageinfo":
                [{"name" : "1",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0}]         
        }
        response = self.c.post('/api/admin/modify',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "")   

    def test_modify_groupToPersonal(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_group,   
            "basicinfo": {
                "name" : "快乐肥宅大赛",
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
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0}]         
        }
        response = self.c.post('/api/admin/modify',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "不能修改比赛类型")  

    def test_modify_notadmin(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_personal,   
            "basicinfo": {
                "name" : "快乐肥宅大赛",
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
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0}]         
        }
        response = self.c.post('/api/admin/modify',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], "Current user is not the admin of this contest") 

    def test_modify_notexist(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_group+1,  
            "basicinfo": {
                "name" : "快乐肥宅大赛",
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
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0}]         
        }
        response = self.c.post('/api/admin/modify',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Contest does not exist.') 

    def test_modify_lenStageinfo6(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_group,   
            "basicinfo": {
                "name" : "快乐肥宅大赛",
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
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0},
                {"name" : "6",
                "details" : "details",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "mode" : 0}]         
        }
        response = self.c.post('/api/admin/modify',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Too much fields.')   

    def test_upload_successful(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_personal,
            "file": "C:\Users\Administrator\Desktop\1.txt" 
        }
        response = self.c.post('/api/admin/upload',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '') 

    def test_upload_compNotexist(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_group+1,
            "file": "C:\Users\Administrator\Desktop\1.txt" 
        }
        response = self.c.post('/api/admin/upload',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Contest does not exist.') 

    def test_upload_Notadmin(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_group,
            "file": "C:\Users\Administrator\Desktop\1.txt" 
        }
        response = self.c.post('/api/admin/upload',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Current user is not the admin of this contest') 

    def test_upload_filenotexist(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid":self.contestId_group,
            "file": "C:\Users\Administrator\Desktop\2.txt" 
        }
        response = self.c.post('/api/admin/upload',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'File not found.') 

    





  


       







