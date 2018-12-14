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
        #admin创建的比赛
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
        self.contestId_created = contest[0].id

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
            "basicinfo": {
                "name" : "快乐肥宅大赛2",
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
        self.contestId_participant = contest[1].id
        #admin报名
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_participant,
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

    def test_user_profile(self): 
        response = self.c.post('/api/user/profile') 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')
        self.assertEqual(len(response_content['competition']['participated_competition']),1)  
        self.assertEqual(response_content['competition']['participated_competition'][0]['title'],"快乐肥宅大赛2")
        self.assertEqual(len(response_content['competition']['created_competition']),1)  
        self.assertEqual(response_content['competition']['created_competition'][0]['title'],"快乐肥宅大赛")
        self.assertEqual(response_content['person']['university'],'清华大学')

    