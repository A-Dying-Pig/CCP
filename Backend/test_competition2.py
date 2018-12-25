from django.test import TransactionTestCase,TestCase
from django.test import Client
from .models import *
import json
from django.http import HttpRequest
import os, sys
from .utils import *
import shutil
#import .api_user

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
                "judgebegin" : False,
                "briefintroduction":"hhhh",
                "details" : "hhhhhhhh"
                },
            "signupinfo": {
                "time" : ["2018-12-10T12:10:00.000Z","2018-12-30T12:10:00.000Z"],
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
                "stageTimeBegin": "2018-12-30T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "3",
                "details" : "details",
                "stageTimeBegin": "2018-12-30T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "4",
                "details" : "details",
                "stageTimeBegin": "2018-12-30T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode" : 0},
                {"name" : "5",
                "details" : "details",
                "stageTimeBegin": "2018-12-30T12:10:00.000Z",
                "handTimeEnd" : "2018-12-30T12:10:00.000Z",
                "evaluationTimeEnd" : "2018-12-30T12:10:00.000Z",
                "zone":0,
                "mode":0}]
        }
        response = self.c.post('/api/competition/create',json.dumps(comp_info),content_type="application/json")
        contest = Contest.objects.filter()
        self.contestId_personal = contest[0].id

    def tearDown(self):
        dirs = os.listdir(RESOURCE_BASE_DIR + '/resources/contests')
        for file in dirs:
           shutil.rmtree(RESOURCE_BASE_DIR + '/resources/contests/'+file)
        dirs = os.listdir(RESOURCE_BASE_DIR + '/resources/users')
        for file in dirs:
           shutil.rmtree(RESOURCE_BASE_DIR + '/resources/users/'+file)

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
            "phone_number": 18001136323,
            "username":"admin2",
            "university" : "清华大学",
            "groupuser" : ["admin3"],
            "custom_field" : ["1","2"],
            "custom_value" : ['1',"2"],
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

    def test_competition_adddiscussion_emptytitle(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"",
            "content":""
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '发帖主题不能为空！')

    def test_competition_adddiscussion_emptycontent(self):
        comp_info={
            "contestid":self.contestId_personal,
            "title":"1",
            "content":""
        }
        response = self.c.post('/api/competition/adddiscussion',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '发帖内容不能为空！')

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
            "phone_number": 18001136323,
            "username":"admin2",
            "university" : "清华大学",
            "groupuser" : ["admin3"],
            "custom_field" : ["1","2"],
            "custom_value" : ['1',"2"],
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
        self.assertEqual(response_content['msg'], '主题帖不存在')

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
        self.assertEqual(response_content['msg'], '发帖内容不能为空！')

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
            "phone_number": 18001136323,
            "username":"admin2",
            "university" : "清华大学",
            "groupuser" : ["admin3"],
            "custom_field" : ["1","2"],
            "custom_value" : ['1',"2"],
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
        #print("++++++++++++++")
        #print(response_content['msg'])
        #print("++++++++++++++")
        discussion = Post.objects.filter()
        #print("===========")
        #print(self.contestId_discussionid)   
        #print("===========") 
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
            "phone_number": 18001136323,
            "username":"admin2",
            "university" : "清华大学",
            "groupuser" : ["admin3"],
            "custom_field" : ["1","2"],
            "custom_value" : ['1',"2"],
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

    def test_competition_worksname(self):
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
        #修改数据库时间
        Contest.objects.filter(title="快乐肥宅大赛-个人").update(enroll_end="2018-12-21T12:10:00.000Z")
        with open("C:\\Users\\Administrator\\Desktop\\1.zip", 'rb') as f:
            response=self.c.post('/api/contestant/submit',{"contestid":self.contestId_personal,'file': f,"name": "1"})
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        contestplayer = ContestPlayer.objects.filter()
        self.ContestPlayer_id = contestplayer[0].player_id
        
        '''
        cur_dir = RESOURCE_BASE_DIR + "/resources/contests/" + str(self.contestId_personal) + '/playerFiles/' + str(self.ContestPlayer_id) + '/compress/'
        dirs = os.listdir(cur_dir)
        for dir in dirs:
            print('--------------')
            print(dir)
            print('------------') 
        self.assertEqual(response_content['msg'], '')
        '''
        comp_info = {
            "contestid": self.contestId_personal
        }
        response = self.c.post('/api/competition/worksname',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')
        self.assertEqual(response_content['filename'],'1.zip')

    def test_competition_worksname_nowork(self):
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
        comp_info = {
            "contestid": self.contestId_personal
        }
        response = self.c.post('/api/competition/worksname',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')
        self.assertEqual(response_content['filename'],'')
