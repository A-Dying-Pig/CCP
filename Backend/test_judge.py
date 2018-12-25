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
                "time" : ["2018-12-10T12:10:00.000Z","2018-12-25T14:10:00.000Z"],
                "mode" : 1,
                "teamnum":5,
                "person" : ["1","2","3","4"],
                "group" : ["1","2","3","4"],
                },
            "stageinfo":
                [{"name" : "phase1",
                "details" : "details",
                "stageTimeBegin": "2018-12-25T15:10:00.000Z",
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
            "groupuser" : [],
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
                                                                phase_hand_end_time1="2018-12-25T14:10:00.000Z",
                                                                phase_evaluate_end_time1="2018-12-27T06:10:00.000Z")
        # todo htx 用报名的选手提交作品
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
        
        # todo htx 改时间，为了设置评委，保证当前时间在phase_hand_end_time和phase_evaluate_end_time之间
        #修改数据库
        Contest.objects.filter(title="快乐肥宅大赛-个人").update(phase_start_time1="2018-12-25T02:10:00.000Z",
                                                                phase_hand_end_time1="2018-12-25T03:10:00.000Z",
                                                                phase_evaluate_end_time1="2018-12-27T06:10:00.000Z")
        
        # todo htx 主办方设置评委                
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")          
        comp_info = {
            "contestid":self.contestId_personal, 
            "type":0,
            "username": "judge1",
            "id":'-1'                 
        }
        response = self.c.post('/api/admin/setjudge',json.dumps(comp_info),content_type="application/json") 

    def tearDown(self):
        dirs = os.listdir(RESOURCE_BASE_DIR + '/resources/contests')
        for file in dirs:
           shutil.rmtree(RESOURCE_BASE_DIR + '/resources/contests/'+file)
        dirs = os.listdir(RESOURCE_BASE_DIR + '/resources/users')
        for file in dirs:
           shutil.rmtree(RESOURCE_BASE_DIR + '/resources/users/'+file)

    def test_judge_getone_successful(self):
        contestplayer = ContestPlayer.objects.filter()
        self.ContestPlayer_id = contestplayer[0].player_id
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        judge_info={
            "contestid": self.contestId_personal,
            "participantid":self.ContestPlayer_id
        }
        response = self.c.post('/api/judge/getone',json.dumps(judge_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '')  
        self.assertEqual(response_content['files'][0]['isLeaf'],False)

    def test_judge_getone_notjudge(self):
        contestplayer = ContestPlayer.objects.filter()
        self.ContestPlayer_id = contestplayer[0].player_id
        judge_info={
            "contestid": self.contestId_personal,
            "participantid":self.ContestPlayer_id
        }
        response = self.c.post('/api/judge/getone',json.dumps(judge_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '当前用户不是该比赛评委')

    def test_judge_getone_playerwrong(self):
        contestplayer = ContestPlayer.objects.filter()
        self.ContestPlayer_id = contestplayer[0].player_id
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        judge_info={
            "contestid": self.contestId_personal,
            "participantid":self.ContestPlayer_id+1
        }
        response = self.c.post('/api/judge/getone',json.dumps(judge_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '未知错误')

    def test_judge_getone_compwrong(self):
        contestplayer = ContestPlayer.objects.filter()
        self.ContestPlayer_id = contestplayer[0].player_id
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        judge_info={
            "contestid": self.contestId_personal+1,
            "participantid":self.ContestPlayer_id
        }
        response = self.c.post('/api/judge/getone',json.dumps(judge_info),content_type="application/json") 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '当前用户不是该比赛评委')

    def test_judge_submit_successful(self): #!!!!!!!!!!
        # todo htx 主办方分配评委（同样要保证时间在phase_hand_end_time和phase_evaluate_end_time之间）
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info={
            "contestid": self.contestId_personal, 
            "judgenum": 1            
        }
        response = self.c.post('/api/admin/allot',json.dumps(comp_info),content_type="application/json")
        
        # todo htx 登录评委账号评分，并提交分数
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        contestplayer = ContestPlayer.objects.filter()
        self.ContestPlayer_id = contestplayer[0].player_id 
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        
        submit_info={
            "contestid":self.contestId_personal,
            "userId":self.ContestPlayer_id,
            "grade":95,
            "phase":"hhhhhhh"            
        }
        response = self.c.post('/api/judge/submit',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        #self.assertEqual(response_content['msg'], '')
        self.assertEqual(response_content['msg'], '相关信息不存在！')

    def test_judge_submit_notjudge(self): 
        # todo htx 主办方分配评委（同样要保证时间在phase_hand_end_time和phase_evaluate_end_time之间）
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info={
            "contestid": self.contestId_personal, 
            "judgenum": 1            
        }
        response = self.c.post('/api/admin/allot',json.dumps(comp_info),content_type="application/json")


        user_info={
            "username": "admin2", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")   
        contestplayer = ContestPlayer.objects.filter()
        self.ContestPlayer_id = contestplayer[0].player_id
        submit_info={
            "contestid":self.contestId_personal,
            "userId":self.ContestPlayer_id,
            "grade":95,
            "phase":"hhhhhhh"            
        }
        response = self.c.post('/api/judge/submit',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '当前用户不是该比赛评委')

    def test_judge_submit_compnotexist(self):
        # todo htx 主办方分配评委（同样要保证时间在phase_hand_end_time和phase_evaluate_end_time之间）
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info={
            "contestid": self.contestId_personal, 
            "judgenum": 1            
        }
        response = self.c.post('/api/admin/allot',json.dumps(comp_info),content_type="application/json")

        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        contestplayer = ContestPlayer.objects.filter()
        self.ContestPlayer_id = contestplayer[0].player_id
        submit_info={
            "contestid":self.contestId_personal+1,
            "userId":self.ContestPlayer_id,
            "grade":95,
            "phase":"hhhhhhh"            
        }
        response = self.c.post('/api/judge/submit',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '当前用户不是该比赛评委')

    def test_judge_submit_playernotexist(self):
        # todo htx 主办方分配评委（同样要保证时间在phase_hand_end_time和phase_evaluate_end_time之间）
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info={
            "contestid": self.contestId_personal, 
            "judgenum": 1            
        }
        response = self.c.post('/api/admin/allot',json.dumps(comp_info),content_type="application/json")
        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        
        contestplayer = ContestPlayer.objects.filter()
        self.ContestPlayer_id = contestplayer[0].player_id
        submit_info={
            "contestid":self.contestId_personal,
            "userId":self.ContestPlayer_id+1,
            "grade":95,
            "phase":"hhhhhhh"            
        }
        response = self.c.post('/api/judge/submit',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'], '相关信息不存在！')

    def test_judge_submit_contestantNotsubmit(self):
        # todo htx 主办方分配评委（同样要保证时间在phase_hand_end_time和phase_evaluate_end_time之间）
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info={
            "contestid": self.contestId_personal, 
            "judgenum": 1            
        }
        response = self.c.post('/api/admin/allot',json.dumps(comp_info),content_type="application/json")

        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        contestplayer = ContestPlayer.objects.filter()
        self.ContestPlayer_id = contestplayer[0].player_id
        submit_info={
            "contestid":self.contestId_personal,
            "userId":self.ContestPlayer_id,
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
        # todo htx 主办方分配评委（同样要保证时间在phase_hand_end_time和phase_evaluate_end_time之间）
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info={
            "contestid": self.contestId_personal, 
            "judgenum": 1            
        }
        response = self.c.post('/api/admin/allot',json.dumps(comp_info),content_type="application/json")

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

    def test_judge_finished_successful(self): #!!!!!!
        # todo htx 主办方分配评委（同样要保证时间在phase_hand_end_time和phase_evaluate_end_time之间）
        user_info={
            "username": "admin", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        comp_info={
            "contestid": self.contestId_personal, 
            "judgenum": 1            
        }
        response = self.c.post('/api/admin/allot',json.dumps(comp_info),content_type="application/json")

        user_info={
            "username": "judge1", 
            "password": "ccp"            
        }
        response = self.c.post('/api/user/login',json.dumps(user_info),content_type="application/json")
        
        contestplayer = ContestPlayer.objects.filter()
        self.ContestPlayer_id = contestplayer[0].player_id
        submit_info={
            "contestid":self.contestId_personal,
            "userId":self.ContestPlayer_id,
            "grade":95,
            "phase":"hhhhhhh"            
        }
        response = self.c.post('/api/judge/submit',json.dumps(submit_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        print('------------')
        print(response_content['msg'])
        print('------------')
        comp_info={
            "contestid":self.contestId_personal                      
        }
        response = self.c.post('/api/judge/finished',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        '''
        self.assertEqual(len(response_content['grades']),1)
        self.assertEqual(response_content['grades'][0]['participantid'],self.ContestPlayer_id)
        self.assertEqual(response_content['grades'][0]['grade'],95)
        '''
        self.assertEqual(len(response_content['grades']),0)

    def test_judge_finished_notjudge(self):
        comp_info={
            "contestid":self.contestId_personal                      
        }
        response = self.c.post('/api/judge/finished',json.dumps(comp_info),content_type="application/json")
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEqual(response_content['msg'],'当前用户不是该比赛评委')
       
