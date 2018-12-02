from django.test import TestCase
from django.test import Client
from .models import CCPUser
import json
from django.http import HttpRequest
#import .api_user

# Create your tests here.
#test api_user
class api_user_Test(TestCase):
    def setUp(self):
        CCPUser.objects.create_superuser(username='admin',password='ccp',email='zyj@126.com')
        
    def test_login_successful(self):
        c=Client()
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        response_content = response.content.decode()
        print(response_content)
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_login_failname(self):
        c = Client()
        user_info={                   
            "username": "zyj", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '用户名或密码错误')

    def test_login_failpassword(self):
        c = Client()
        user_info={                       
            "username": "admin", 
            "password": "ccpccp"
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '用户名或密码错误')

    def test_register_successful(self):
        c = Client()
        user_info={      
            "username": "admin2", 
            "password": "ccp",
            "email":"zyj1@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_register_name_repeat(self):
        c = Client()
        user_info={      
            "username": "admin", 
            "password": "ccp",
            "email":"zyj2@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '用户名已存在！')

    def test_register_email_repeat(self):
        c = Client()
        user_info={      
            "username": "admin3", 
            "password": "ccp",
            "email":"zyj@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '邮箱地址已经被注册！')

    #def test_check

    def test_createcompetition_successful(self):
        c = Client()        
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛",
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-30 12:00","2019-12-30 12:00"],
                "mode" : 0,
                "person" : ["1","2","3","4"],
                "group" : ["1","2","3","4"],
            },
            "stageinfo":
                [{"name" : "1",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0}]
        }
        response = c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        print(response_content)
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_createcompetition_lenHolders5_wrong(self):
        c = Client()
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛",
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3","快乐肥宅4"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-30 12:00","2019-12-30 12:00"],
                "mode" : 0,
                "person" : ["1","2","3","4"],
                "group" : ["1","2","3","4"],
            },
            "stageinfo":
                [{"name" : "1",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0}]
        }
        response = c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Too much fields.')

    def test_createcompetition_lenPerson5_wrong(self):
        c = Client()
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛",
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-30 12:00","2019-12-30 12:00"],
                "mode" : 0,
                "person" : ["1","2","3","4","5"],
                "group" : ["1","2","3","4"],
            },
            "stageinfo":
                [{"name" : "1",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0}]
        }
        response = c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Too much fields.')

    def test_createcompetition_lenGroup5_wrong(self):
        c = Client()
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛",
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-30 12:00","2019-12-30 12:00"],
                "mode" : 0,
                "person" : ["1","2","3","4"],
                "group" : ["1","2","3","4","5"],
            },
            "stageinfo":
                [{"name" : "1",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0}]
        }
        response = c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Too much fields.')

    def test_createcompetition_lenstageinfo6_wrong(self):
        c = Client()
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛",
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-30 12:00","2019-12-30 12:00"],
                "mode" : 0,
                "person" : ["1","2","3","4"],
                "group" : ["1","2","3","4"],
            },
            "stageinfo":
                [{"name" : "1",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "6",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0}]
        }
        response = c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Too much fields.')

    def test_createcompetition_lentimenot2_wrong(self):
        c = Client()
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛",
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-30 12:00"],
                "mode" : 0,
                "person" : ["1","2","3","4"],
                "group" : ["1","2","3","4"],
            },
            "stageinfo":
                [{"name" : "1",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "2",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "handTimeEnd" : "2018-12-30 12:00",
                "evaluationTimeEnd" : "2018-12-30 12:00",
                "mode" : 0}]
        }
        response = c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Too much fields.')



