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
                "mode":0}]
        }
        response = self.c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        contest = Contest.objects.filter()
        self.contestId_personal = contest[0].id

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
            "phone_number": 18001136323,
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
            "phone_number": 18001136323,
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
    def tearDown(self):
        dirs = os.listdir(RESOURCE_BASE_DIR + '/resources/contests')
        for file in dirs:
           shutil.rmtree(RESOURCE_BASE_DIR + '/resources/contests/'+file)
        dirs = os.listdir(RESOURCE_BASE_DIR + '/resources/users')
        for file in dirs:
           shutil.rmtree(RESOURCE_BASE_DIR + '/resources/users/'+file)
 
    def test_judgeprogress_successful(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name":"1"})
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
            "username": 'judge1',
            "id":'1'                 
        }
        response = self.c.post('/api/admin/setjudge',json.dumps(comp_info),content_type="application/json") 
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        contestplayer = ContestPlayer.objects.filter()
        self.contestplayer_id = contestplayer[0].player_id
        submit_info={
            "contestid":self.contestId_personal,
            "userId":self.contestplayer_id,
            "grade":95,
            "phase":"hhhhhhh"            
        }
        response = self.c.post('/api/judge/submit',json.dumps(submit_info),content_type="application/json")
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info={
            "contestid":self.contestId_personal                      
        }
        response = self.c.post('/api/admin/judgeprogress',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(len(response_content['judges']),1)
        self.assertEqual(response_content['judges'][0]['name'],"judge1")
        self.assertEqual(response_content['judges'][0]['finish'],1)

    def test_judgeprogress_notadmin(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name":"1"})
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
        contestplayer = ContestPlayer.objects.filter()
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
        response = self.c.post('/api/admin/judgeprogress',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],"非管理员不能查看评测进度")

    def test_judgeprogress_compnotExist(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name":'1'})
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
        contestplayer = ContestPlayer.objects.filter()
        self.contestplayer_id = contestplayer[0].player_id
        submit_info={
            "contestid":self.contestId_personal,
            "userId":self.contestplayer_id,
            "grade":95,
            "phase":"hhhhhhh"            
        }
        response = self.c.post('/api/judge/submit',json.dumps(submit_info),content_type="application/json")
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info={
            "contestid":self.contestId_group+1                      
        }
        response = self.c.post('/api/admin/judgeprogress',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],"比赛不存在")

    def test_super_setindex_successful(self):
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
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'')

    def test_super_setindex_notsuperadmin(self):
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        comp_info = {
            "slider":[self.contestId_personal], 
            "hot":[self.contestId_personal]
        }
        response = self.c.post('/api/super/setindex',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'Authority denied.')  

    def test_super_setindex_slidernotexist(self):
        user_info={
            "username": "super_admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        comp_info = {
            "slider":[self.contestId_group+1], 
            "hot":[self.contestId_personal]
        }
        response = self.c.post('/api/super/setindex',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'比赛不存在')
    
    def test_super_setindex_hotnotexist(self):
        user_info={
            "username": "super_admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        comp_info = {
            "slider":[self.contestId_personal], 
            "hot":[self.contestId_group+1]
        }
        response = self.c.post('/api/super/setindex',json.dumps(comp_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'比赛不存在')

    def test_super_indexinfo_successful(self):
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
        response = self.c.post('/api/super/indexinfo')
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'')
        self.assertEqual(response_content['contests'][0]["contestid"],self.contestId_personal)
        self.assertEqual(response_content['contests'][0]["is_slider"],1)
        self.assertEqual(response_content['contests'][0]["is_hot"],1)
        self.assertEqual(response_content['contests'][1]["contestid"],self.contestId_group)
        self.assertEqual(response_content['contests'][1]["is_slider"],0)
        self.assertEqual(response_content['contests'][1]["is_hot"],0)

    def test_super_indexinfo_notsuperadmin(self):
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
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        response = self.c.post('/api/super/indexinfo')
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'Authority denied.')

    def test_admin_getsubmitnum_successful(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name":"1"})
        user_info={
            'username':"admin",
            "password":"ccp"
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        submit_info={
            "contestid":self.contestId_personal            
        }
        response = self.c.post('/api/admin/getsubmitnum',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'')
        self.assertEqual(response_content['submitnum'],1)
        self.assertEqual(response_content['allnum'],1)

    def test_admin_getsubmitnum_onePlayerRepeatSubmit(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name":"1"})
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name":"1"})
        user_info={
            'username':"admin",
            "password":"ccp"
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        submit_info={
            "contestid":self.contestId_personal            
        }
        response = self.c.post('/api/admin/getsubmitnum',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'')
        self.assertEqual(response_content['submitnum'],1)
        self.assertEqual(response_content['allnum'],1) 

    def test_admin_getsubmitnum_twoplayerOnesubmit(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name":"1"})
        #个人报名
        user_info={
            "username": "admin3", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "phone_number":18001136323,
            "university" : "清华大学",
            "groupuser" : [],
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        user_info={
            'username':"admin",
            "password":"ccp"
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        submit_info={
            "contestid":self.contestId_personal            
        }
        response = self.c.post('/api/admin/getsubmitnum',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'')
        self.assertEqual(response_content['submitnum'],1)
        self.assertEqual(response_content['allnum'],2)

    def test_admin_getsubmitnum_twoplayerTwosubmit(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name":"1"})
        #个人报名
        user_info={
            "username": "admin3", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info = {
            "contestid": self.contestId_personal,
            "phone_number":18001136323,
            "university" : "清华大学",
            "groupuser" : [],
            "custom_field" : ["1"],
            "custom_value" : ['1'],
            }            
        response = self.c.post('/api/competition/enroll',json.dumps(comp_info),content_type="application/json")
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name":"1"})
        user_info={
            'username':"admin",
            "password":"ccp"
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        submit_info={
            "contestid":self.contestId_personal            
        }
        response = self.c.post('/api/admin/getsubmitnum',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'')
        self.assertEqual(response_content['submitnum'],2)
        self.assertEqual(response_content['allnum'],2)

    def test_admin_getsubmitnum_notadmin(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name":"1"})
        submit_info={
            "contestid":self.contestId_personal            
        }
        response = self.c.post('/api/admin/getsubmitnum',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'当前用户不是本比赛管理员')

    def test_admin_getsubmitnum_compNotexist(self):
        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name":"1"})
        user_info={
            'username':"admin",
            "password":"ccp"
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        submit_info={
            "contestid":self.contestId_group+1            
        }
        response = self.c.post('/api/admin/getsubmitnum',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'比赛不存在')

    def test_admin_setadvanced_successful(self):
        user_info={
            'username':"admin",
            "password":"ccp"
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        comp_info={
            'contestid':self.contestId_personal,
            "target":0,
            "advanced":1
        }
        response = self.c.post('/api/admin/setadvanced',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'')

    def test_admin_setadvanced_notadmin(self):
        comp_info={
            'contestid':self.contestId_personal,
            "target":0,
            "advanced":1
        }
        response = self.c.post('/api/admin/setadvanced',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'非管理员不能设置晋级选手名单')

    def test_admin_setadvanced_compNotexist(self):
        user_info={
            'username':"admin",
            "password":"ccp"
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        comp_info={
            'contestid':self.contestId_group+1,
            "target":0,
            "advanced":1
        }
        response = self.c.post('/api/admin/setadvanced',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'比赛不存在')

    def test_admin_setadvanced_useroverflow(self):
        user_info={
            'username':"admin",
            "password":"ccp"
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        comp_info={
            'contestid':self.contestId_personal,
            "target":0,
            "advanced":2
        }
        response = self.c.post('/api/admin/setadvanced',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'')

    def test_admin_advanced_successful_noset(self):
        user_info={
            'username':"admin",
            "password":"ccp"
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        comp_info={
            "contestid":self.contestId_personal,
            "target": -1            
        }
        response = self.c.post('/api/admin/advanced',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'')
        self.assertEqual(len(response_content['participants']),1)
        self.assertEqual(response_content['participants'][0]['username'],'admin2')
        print('-----advanced---------')
        print(response_content['participants'][0])
        print('---------')
        self.assertEqual(response_content['participants'][0]['university'],"清华大学")

    def test_admin_advanced_Two(self):
        user_info={
            "username": "admin3", 
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
            'username':"admin",
            "password":"ccp"
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        comp_info={
            'contestid':self.contestId_personal,
            "target":0,
            "advanced":2
        }
        response = self.c.post('/api/admin/setadvanced',json.dumps(comp_info),content_type="application/json")
        comp_info={
            "contestid":self.contestId_personal,
            "target": -1            
        }
        response = self.c.post('/api/admin/advanced',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'')
        self.assertEqual(len(response_content['participants']),2)
        self.assertEqual(response_content['participants'][0]['username'],'admin3')
        self.assertEqual(response_content['participants'][1]['username'],'admin2')

    def test_admin_advanced_notadmin(self):
        comp_info={
            "contestid":self.contestId_personal,
            "target": -1            
        }
        response = self.c.post('/api/admin/advanced',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'非管理员不能获取选手名单')

    def test_admin_advanced_compNotexist(self):
        comp_info={
            "contestid":self.contestId_group+1,
            "target":-1         
        }
        response = self.c.post('/api/admin/advanced',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'比赛不存在')