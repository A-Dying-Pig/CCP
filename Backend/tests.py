from django.test import TestCase
from django.test import Client
from .models import *
import json
from django.http import HttpRequest
import os, sys
from .utils import *
import shutil
#import .api_user

# Create your tests here.
#test api_user
class api_user_competiton_start_Test(TestCase):
    def setUp(self):
        c = Client()
        user_info={      
            "username": "super_admin", 
            "password": "ccp",
            "email":"zyj@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        CCPUser.objects.all().update(is_superuser=True)

    def tearDown(self):
        dirs = os.listdir(RESOURCE_BASE_DIR + '/resources/contests')
        for file in dirs:
           shutil.rmtree(RESOURCE_BASE_DIR + '/resources/contests/'+file)
        dirs = os.listdir(RESOURCE_BASE_DIR + '/resources/users')
        for file in dirs:
           shutil.rmtree(RESOURCE_BASE_DIR + '/resources/users/'+file)

    def test_register_successful(self):
        c = Client()
        user_info={      
            "username": "admin", 
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
            "username": "super_admin", 
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
            "username": "admin2", 
            "password": "ccp",
            "email":"zyj@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '邮箱地址已经被注册！')
            
    def test_login_superuser_successful(self):
        c=Client()
        user_info={
            "username": "super_admin", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_login_user_successful(self):
        c=Client()
        user_info={      
            "username": "user", 
            "password": "ccp",
            "email":"zyj123@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "user", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        response_content = response.content.decode()
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
            "username": "super_admin", 
            "password": "ccpccp"
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '用户名或密码错误')

    def test_modify_successful(self):
        c=Client()
        user_info={      
            "username": "user", 
            "password": "ccp",
            "email":"zyj1@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "user", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        modify_info={      
            "university": "清华大学", 
            "region":{
                "province":"北京",
                "city":"北京"
            }
        }
        response = c.post('/api/user/modify',json.dumps(modify_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_modify_empty(self):
        c=Client()
        user_info={      
            "username": "user", 
            "password": "ccp",
            "email":"zyj1@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "user", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        modify_info={      
            "university": "", 
            "region":{
                "province":"",
                "city":""
            }
        }
        response = c.post('/api/user/modify',json.dumps(modify_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '') 


    def test_competition_uploadimg_notlogin(self):
        c = Client()
        with open("C:\\Users\\Administrator\\Desktop\\1.jpg", 'rb') as f:
                response=c.post('/api/competition/uploadimg',{'file': f})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'请先登录')

    def test_competition_uploadimg(self):
        c = Client()
        user_info={      
            "username": "user", 
            "password": "ccp",
            "email":"zyj1@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "user", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")        
        with open("C:\\Users\\Administrator\\Desktop\\1.jpg", 'rb') as f:
            response=c.post('/api/competition/uploadimg',{'file': f})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'')

    def test_createcompetition_group_successful(self):
        c = Client()
        user_info={      
            "username": "user", 
            "password": "ccp",
            "email":"zyj1@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "user", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")        
        with open("C:\\Users\\Administrator\\Desktop\\1.jpg", 'rb') as f:
            response=c.post('/api/competition/uploadimg',{'file': f})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        url=response_content["url"]
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛-组队",
                "img" : url,
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
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
        response = c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

        contest = Contest.objects.filter()
        self.contestId_group = contest[0].id
        work_path=RESOURCE_BASE_DIR + '/resources/contests/' + str(self.contestId_group)
        #print(work_path)
        dirs = os.listdir(work_path)
        self.assertNotEqual(dirs,'')

    def test_createcompetition_personal_successful(self):
        c = Client()
        user_info={      
            "username": "user", 
            "password": "ccp",
            "email":"zyj1@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "user", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")        
        with open("C:\\Users\\Administrator\\Desktop\\1.jpg", 'rb') as f:
                response=c.post('/api/competition/uploadimg',{'file': f})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        url=response_content["url"]
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛-组队",
                "img" : url,
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "judgebegin" : 0,
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
                "mode" : 0}]
        }
        response = c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_createcompetition_lenHolders5_wrong(self):
        c = Client()
        user_info={      
            "username": "user", 
            "password": "ccp",
            "email":"zyj1@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "user", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")        
        with open("C:\\Users\\Administrator\\Desktop\\1.jpg", 'rb') as f:
            response=c.post('/api/competition/uploadimg',{'file': f})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        url=response_content["url"]
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛-组队",
                "img" : url,
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3","快乐肥宅4"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "judgebegin" : 0,
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
                "mode" : 0}]
        }
        response = c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Too much fields.')

    def test_createcompetition_lenPerson5_wrong(self):
        c = Client()
        user_info={      
            "username": "user", 
            "password": "ccp",
            "email":"zyj1@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "user", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")        
        with open("C:\\Users\\Administrator\\Desktop\\1.jpg", 'rb') as f:
            response=c.post('/api/competition/uploadimg',{'file': f})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        url=response_content["url"]
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛-组队",
                "img" : url,
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "judgebegin" : 0,
                "briefintroduction":"hhhh",
                "details" : "hhhhhhhh"
                },        
            "signupinfo": {
                "time" : ["2018-12-10T12:10:00.000Z","2019-12-30T12:10:00.000Z"],
                "mode" : 1,
                "teamnum":5,
                "person" : ["1","2","3","4","5"],
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
        response = c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Too much fields.')

    def test_createcompetition_lenGroup5_wrong(self):
        c = Client()
        user_info={      
            "username": "user", 
            "password": "ccp",
            "email":"zyj1@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "user", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")        
        with open("C:\\Users\\Administrator\\Desktop\\1.jpg", 'rb') as f:
                response=c.post('/api/competition/uploadimg',{'file': f})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        url=response_content["url"]
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛-组队",
                "img" : url,
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "judgebegin" : 0,
                "briefintroduction":"hhhh",
                "details" : "hhhhhhhh"
                },        
            "signupinfo": {
                "time" : ["2018-12-10T12:10:00.000Z","2019-12-30T12:10:00.000Z"],
                "mode" : 1,
                "teamnum":5,
                "person" : ["1","2","3","4"],
                "group" : ["1","2","3","4","5"],
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
        response = c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Too much fields.')

    def test_createcompetition_lenstageinfo6_wrong(self):
        c = Client()
        user_info={      
            "username": "user", 
            "password": "ccp",
            "email":"zyj1@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "user", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")        
        with open("C:\\Users\\Administrator\\Desktop\\1.jpg", 'rb') as f:
                response=c.post('/api/competition/uploadimg',{'file': f})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        url=response_content["url"]
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛-组队",
                "img" : url,
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "judgebegin" : 0,
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
                "mode" : 0},
                {"name" : "6",
                "details" : "details",
                "stageTimeBegin": "2018-12-20T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,     
                "mode" : 0}]
        }
        response = c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Too much fields.')

    def test_createcompetition_lentimenot2_wrong(self):
        c = Client()
        user_info={      
            "username": "user", 
            "password": "ccp",
            "email":"zyj1@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "user", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")        
        with open("C:\\Users\\Administrator\\Desktop\\1.jpg", 'rb') as f:
                response=c.post('/api/competition/uploadimg',{'file': f})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        url=response_content["url"]
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛-组队",
                "img" : url,
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "judgebegin" : 0,
                "briefintroduction":"hhhh",
                "details" : "hhhhhhhh"
                },        
            "signupinfo": {
                "time" : ["2018-12-10T12:10:00.000Z"],
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
                "mode" : 0}]
        }
        response = c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Too much fields.')

    '''
    def test_createcompetition_group_Superuser(self):
        c = Client()
        user_info={
            "username": "super_admin", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")        
        with open("C:\\Users\\Administrator\\Desktop\\1.jpg", 'rb') as f:
                response=c.post('/api/competition/uploadimg',{'file': f})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        url=response_content["url"]
        comp_info = {
            "basicinfo": {
                "name" : "快乐肥宅大赛-组队",
                "img" : url,
                "holders" : ["快乐肥宅","快乐肥宅1","快乐肥宅2","快乐肥宅3"],
                "sponsors" : [],
                "comtype" : "趣味比赛",
                "judgebegin" : 0,
                "briefintroduction":"hhhh",
                "details" : "hhhhhhhh"
                },        
            "signupinfo": {
                "time" : ["2018-12-10T12:10:00.000Z","2019-12-30T12:10:00.000Z"],
                "mode" : 1,
                "teamnum":[1,10],
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
        response = c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '超级用户不能创建比赛')
    '''

    def test_user_uploadimg(self):
        c=Client()
        user_info={
            "username": "user", 
            "password": "ccp",
            "email":"zyj123@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "user", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        with open("C:\\Users\\Administrator\\Desktop\\1.jpg", 'rb') as f:
            response=c.post('/api/user/uploadimg',{'file': f})        
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    '''
    def test_user_uploadimg_imgnotexist(self):
        c=Client()
        user_info={
            "username": "user", 
            "password": "ccp",
            "email":"zyj123@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "user", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        with open("C:\\Users\\Administrator\\Desktop\\1.jpg", 'rb') as f:
            response=c.post('/api/user/uploadimg',{'file': f})        
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'File not found.')
    '''

    def test_info_about_successful(self):
        c=Client()
        user_info={
            "username": "user", 
            "password": "ccp",
            "email":"zyj123@126.com"
        }
        response = c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "user", 
            "password": "ccp"            
        }
        response = c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        response = c.post('/api/info/about')
        response_content = response.content.decode()
        #print(response_content)
        self.assertEqual(response.status_code,200)

    def test_info_about_notlogin(self):
        c=Client()
        response = c.post('/api/info/about')
        self.assertEqual(response.status_code,200)



