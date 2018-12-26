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
class api_judge_Test(TestCase):
    def setUp(self):
        self.c=Client()
        #用户登录和比赛创建,比赛报名。管理员设置比赛评委
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
                "comtype" : "web",
                "briefintroduction":"hhhh",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-10T12:10:00.000Z","2018-12-25T11:10:00.000Z"],
                "mode" : 1,
                "teamnum":5,
                "person" : ["1","2","3","4"],
                "group" : ["1","2","3","4"],
                },
            "stageinfo":
                [{"name" : "phase1",
                "details" : "details",
                "stageTimeBegin": "2018-12-25T12:10:00.000Z",
                "handTimeEnd" : "2018-12-26T01:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0}]
        }
        response = self.c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        contest = Contest.objects.filter()
        self.contestId_personal = contest[0].id
        
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
            "phone_number": 18001136323,
            "username":"admin2",
            "university" : "清华大学",
            "groupuser" : ["admin3"],
            "custom_field" : ["1","2"],
            "custom_value" : ['1',"2"],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        user_info={      
            "username": "judge1", 
            "password": "ccp",
            "email":"judge1@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        
        #修改数据库
        Contest.objects.filter(title="快乐肥宅大赛-个人").update(enroll_end="2018-12-21T12:10:00.000Z",
                                                                phase_start_time1="2018-12-25T02:10:00.000Z",
                                                                phase_hand_end_time1="2018-12-26T15:10:00.000Z",
                                                                phase_evaluate_end_time1="2018-12-27T06:10:00.000Z")

    def tearDown(self):
        dirs = os.listdir(RESOURCE_BASE_DIR + '/resources/contests')
        for file in dirs:
           shutil.rmtree(RESOURCE_BASE_DIR + '/resources/contests/'+file)
        dirs = os.listdir(RESOURCE_BASE_DIR + '/resources/users')
        for file in dirs:
           shutil.rmtree(RESOURCE_BASE_DIR + '/resources/users/'+file)

    def test_contestant_submit_successful(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name": "1"})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        contestplayer = ContestPlayer.objects.filter()
        self.ContestPlayer_id = contestplayer[0].player_id
        
        cur_dir = RESOURCE_BASE_DIR + "/resources/contests/" + str(self.contestId_personal) + '/playerFiles/' + str(self.ContestPlayer_id) + '/compress/'
        dirs = os.listdir(cur_dir)
        for dir in dirs:
            print('--------------')
            print(dir)
            print('------------')
            self.assertEqual(dir,'1.zip') 
        self.assertEqual(response_content['msg'], '') 

    def test_contestant_submit_inenrolltime(self):
        #修改数据库
        Contest.objects.filter(title="快乐肥宅大赛-个人").update(enroll_end="2018-12-26T20:10:00.000Z",
                                                                phase_start_time1="2018-12-26T21:10:00.000Z",
                                                                phase_hand_end_time1="2018-12-26T22:10:00.000Z",
                                                                phase_evaluate_end_time1="2018-12-27T06:10:00.000Z")
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name": "1"})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '当前比赛仍在报名阶段，不能提交作品')    

    def test_contestant_submit_submitend(self):
        #修改数据库
        Contest.objects.filter(title="快乐肥宅大赛-个人").update(enroll_end="2018-12-21T12:10:00.000Z",
                                                                phase_start_time1="2018-12-25T02:10:00.000Z",
                                                                phase_hand_end_time1="2018-12-25T03:10:00.000Z",
                                                                phase_evaluate_end_time1="2018-12-27T06:10:00.000Z")
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name": "1"})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '比赛当前阶段的提交已经截止')  

    def test_contestant_submit_compNotexist(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal+1,'file': f,"name": "1"})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Contest does not exist.')
    
    def test_contestant_submit_notenroll(self):
        user_info={      
            "username": "admin3", 
            "password": "ccp",
            "email":"zyj3@126.com"
        }
        response = self.c.post('/api/user/register',json.dumps(user_info),content_type="application/json")
        user_info={
            "username": "admin3", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name": "1"})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Current user did not attend this contest') 

    '''
    def test_contestant_submit_fileNotexist(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        with open("C:\\Users\\Administrator\\Desktop\\2.jpg", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name": "1"})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'File not found.') 
    '''

    def test_user_check(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        user_info={
            "contestid": self.contestId_personal,
            "username": "admin2"
        }
        response = self.c.post('/api/user/check',json.dumps(user_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '不能重复报名')

    def test_user_checknotmatch(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        user_info={
            "contestid": self.contestId_personal+10,
            "username": "admin2"
        }
        response = self.c.post('/api/user/check',json.dumps(user_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertNotEqual(response_content['msg'], '')      

    def test_user_check_logout(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        response = self.c.post('/logout')
        user_info={
            "contestid": self.contestId_personal,
            "username": "admin2"
        }
        response = self.c.post('/api/user/check',json.dumps(user_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '不能重复报名')          
    
    def test_user_check_admin(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        user_info={
            "contestid": self.contestId_personal,
            "username": "admin"
        }
        response = self.c.post('/api/user/check',json.dumps(user_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '比赛管理员不能报名')  
