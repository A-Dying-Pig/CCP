from django.test import TestCase
from django.test import Client
from .models import *
import json
from django.http import HttpRequest
#import .api_user

# Create your tests here.
#test api_user
class api_message_Test(TestCase):
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
        comp_info = {
            "contestid":self.contestId_personal,
            "title":"初赛时间",
            "content":"hhhhhh",
            "target":{
                "id":-1,
                "type":0
            }           
        }
        response = self.c.post('/api/admin/broadcast',json.dumps(comp_info),content_type="application/json") 
        comp_info = {
            "contestid":self.contestId_personal,
            "title":"复赛时间",
            "content":"hhhhhh",
            "target":{
                "id":-1,
                "type":0
            }           
        }
        response = self.c.post('/api/admin/broadcast',json.dumps(comp_info),content_type="application/json") 
        
    def test_message_getnum(self): 
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        response = self.c.post('/api/message/getnum') 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(len(response_content['num']), 2)
        self.assertEqual(response.status_code,200)

    def test_message_getnum_notplayer(self): 
        response = self.c.post('/api/message/getnum') 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '未知错误！')

    def test_message_getall(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        message_info={
            "pageNum":1
        }
        response = self.c.post('/api/message/getall',json.dumps(message_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['current_page_num'], 1)
        self.assertEqual(len(response_content['array']),2)
        self.assertEqual(response_content['array'][0]['read'],0)

    def test_message_getall_pageoverflow(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        message_info={
            "pageNum":2
        }
        response = self.c.post('/api/message/getall',json.dumps(message_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['current_page_num'], 2)
        self.assertEqual(len(response_content['array']),0)
        
    def test_message_detail_successful(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        message_info={
            "pageNum":1
        }
        response = self.c.post('/api/message/getall',json.dumps(message_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.messageid = response_content['array'][0]['messageId']
        message_info={
            "messageId":self.messageid
        }
        response = self.c.post('/api/message/detail',json.dumps(message_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['title'], "初赛时间")

    def test_message_detail_msgnotexist(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        message_info={
            "pageNum":1
        }
        response = self.c.post('/api/message/getall',json.dumps(message_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.messageid = response_content['array'][0]['messageId']
        message_info={
            "messageId":self.messageid+10
        }
        response = self.c.post('/api/message/detail',json.dumps(message_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '您查找的消息不存在！')

    def test_message_detail_notplayer(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        message_info={
            "pageNum":1
        }
        response = self.c.post('/api/message/getall',json.dumps(message_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.messageid = response_content['array'][0]['messageId']
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        message_info={
            "messageId":self.messageid
        }
        response = self.c.post('/api/message/detail',json.dumps(message_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['title'], '未知错误！')

    def test_message_change(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        message_info={
            "pageNum":1
        }
        response = self.c.post('/api/message/getall',json.dumps(message_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.messageid = response_content['array'][0]['messageId']
        message_info={
            "messageId":self.messageid
        }
        response = self.c.post('/api/message/detail',json.dumps(message_info),content_type="application/json") 
        #未读消息数变为1
        response = self.c.post('/api/message/getnum') 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(len(response_content['num']), 1)
        #全部信息列表发生变化
        message_info={
            "pageNum":1
        }
        response = self.c.post('/api/message/getall',json.dumps(message_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['current_page_num'], 1)
        self.assertEqual(len(response_content['array']),2)
        self.assertEqual(response_content['array'][0]['read'],1)
        self.assertEqual(response_content['array'][1]['read'],0)

