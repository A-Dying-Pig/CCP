from django.test import TestCase
from django.test import Client
from .models import *
import json
from django.http import HttpRequest
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
            "username": judge1,
            "id":'1'                 
        }
        response = self.c.post('/api/admin/setjudge',json.dumps(comp_info),content_type="application/json") 

    def test_contestant_submit_successful(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        submit_info={
            "contestid":self.contestId_personal,
            "file": "C:\Users\Administrator\Desktop\1.txt" 
        }
        response = self.c.post('/api/contest/submit',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')  

    def test_contestant_submit_compNotexist(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        submit_info={
            "contestid":self.contestId_personal+1,
            "file": "C:\Users\Administrator\Desktop\1.txt" 
        }
        response = self.c.post('/api/contest/submit',json.dumps(submit_info),content_type="application/json")
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
        submit_info={
            "contestid":self.contestId_personal,
            "file": "C:\Users\Administrator\Desktop\1.txt" 
        }
        response = self.c.post('/api/contest/submit',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'Current user did not attend this contest') 

    def test_contestant_submit_fileNotexist(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        submit_info={
            "contestid":self.contestId_personal,
            "file": "C:\Users\Administrator\Desktop\2.txt" 
        }
        response = self.c.post('/api/contest/submit',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], 'File not found.') 
                
    def test_judge_getone_successful(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        submit_info={
            "contestid":self.contestId_personal,
            "file": "C:\Users\Administrator\Desktop\1.txt" 
        }
        response = self.c.post('/api/contest/submit',json.dumps(submit_info),content_type="application/json")
        contestplayer = contestplayer.objects.filter()
        self.contestplayer_id = contestplayer[0].player_id
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        judge_info={
            "contestid": self.contestId_personal,
            "participantid":self.contestplayer_id
        }
        response = self.c.post('/api/judge/getone',json.dumps(judge_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')  
        self.assertEqual(response_content['files'][0]['isLeaf'],'true')

    def test_judge_getone_notjudge(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        submit_info={
            "contestid":self.contestId_personal,
            "file": "C:\Users\Administrator\Desktop\1.txt" 
        }
        response = self.c.post('/api/contest/submit',json.dumps(submit_info),content_type="application/json")
        contestplayer = contestplayer.objects.filter()
        self.contestplayer_id = contestplayer[0].player_id
        judge_info={
            "contestid": self.contestId_personal,
            "participantid":self.contestplayer_id
        }
        response = self.c.post('/api/judge/getone',json.dumps(judge_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '权限认证失败！')

    def test_judge_getone_playerwrong(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        submit_info={
            "contestid":self.contestId_personal,
            "file": "C:\Users\Administrator\Desktop\1.txt" 
        }
        response = self.c.post('/api/contest/submit',json.dumps(submit_info),content_type="application/json")
        contestplayer = contestplayer.objects.filter()
        self.contestplayer_id = contestplayer[0].player_id
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        judge_info={
            "contestid": self.contestId_personal,
            "participantid":self.contestplayer_id+1
        }
        response = self.c.post('/api/judge/getone',json.dumps(judge_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '所查看选手不存在')

    def test_judge_getone_compwrong(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        submit_info={
            "contestid":self.contestId_personal,
            "file": "C:\Users\Administrator\Desktop\1.txt" 
        }
        response = self.c.post('/api/contest/submit',json.dumps(submit_info),content_type="application/json")
        contestplayer = contestplayer.objects.filter()
        self.contestplayer_id = contestplayer[0].player_id
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        judge_info={
            "contestid": self.contestId_personal+1,
            "participantid":self.contestplayer_id
        }
        response = self.c.post('/api/judge/getone',json.dumps(judge_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '所查看比赛不存在')

    def test_judge_submit_successful(self):
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        contestplayer = contestplayer.objects.filter()
        self.contestplayer_id = contestplayer[0].player_id
        submit_info={
            "contestid":self.contestId_personal,
            "userId":self.contestplayer_id,
            "grade":95,
            "phase":"hhhhhhh"            
        }
        response = self.c.post('/api/judge/submit',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')

    def test_judge_submit_notjudge(self):
        contestplayer = contestplayer.objects.filter()
        self.contestplayer_id = contestplayer[0].player_id
        submit_info={
            "contestid":self.contestId_personal,
            "userId":self.contestplayer_id,
            "grade":95,
            "phase":"hhhhhhh"            
        }
        response = self.c.post('/api/judge/submit',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '权限认证失败！')

    def test_judge_submit_compnotexist(self):
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        contestplayer = contestplayer.objects.filter()
        self.contestplayer_id = contestplayer[0].player_id
        submit_info={
            "contestid":self.contestId_personal+1,
            "userId":self.contestplayer_id,
            "grade":95,
            "phase":"hhhhhhh"            
        }
        response = self.c.post('/api/judge/submit',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '相关信息不存在！')

    def test_judge_submit_playernotexist(self):
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        contestplayer = contestplayer.objects.filter()
        self.contestplayer_id = contestplayer[0].player_id
        submit_info={
            "contestid":self.contestId_personal,
            "userId":self.contestplayer_id+1,
            "grade":95,
            "phase":"hhhhhhh"            
        }
        response = self.c.post('/api/judge/submit',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '相关信息不存在！')    

    def test_judge_finished_emptyplayersubmit(self):
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info={
            "contestid":self.contestId_personal                      
        }
        response = self.c.post('/api/judge/finished',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(len(response_content['grades']),0)

    def test_judge_finished_emptyscored(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        submit_info={
            "contestid":self.contestId_personal,
            "file": "C:\Users\Administrator\Desktop\1.txt" 
        }
        response = self.c.post('/api/contest/submit',json.dumps(submit_info),content_type="application/json")
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info={
            "contestid":self.contestId_personal                      
        }
        response = self.c.post('/api/judge/finished',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(len(response_content['grades']),0)

    def test_judge_finished_successful(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        submit_info={
            "contestid":self.contestId_personal,
            "file": "C:\Users\Administrator\Desktop\1.txt" 
        }
        response = self.c.post('/api/contest/submit',json.dumps(submit_info),content_type="application/json")
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        contestplayer = contestplayer.objects.filter()
        self.contestplayer_id = contestplayer[0].player_id
        submit_info={
            "contestid":self.contestId_personal,
            "userId":self.contestplayer_id,
            "grade":95,
            "phase":"hhhhhhh"            
        }
        response = self.c.post('/api/judge/submit',json.dumps(submit_info),content_type="application/json")
        comp_info={
            "contestid":self.contestId_personal                      
        }
        response = self.c.post('/api/judge/finished',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(len(response_content['grades']),1)
        self.assertEqual(response_content['grades'][0]['participantid'],self.contestplayer_id)
        self.assertEqual(response_content['grades'][0]['grade'],95)

    def test_judge_finished_notjudge(self):
        comp_info={
            "contestid":self.contestId_personal                      
        }
        response = self.c.post('/api/judge/finished',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'Unauthorized')
       
