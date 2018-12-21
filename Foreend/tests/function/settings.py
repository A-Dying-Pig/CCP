import os
import datetime

today = datetime.date.today()

configs = {
    'BASE_URL': 'http://127.0.0.1:8000',
    'SUPERADMIN_URL': 'http://127.0.0.1:8000/superadmin',
    'MAX_WAITING_TIME': 5,                 #seconds
    'PARTICIPANT_USERNAME': 'leiyiran',
    'PARTICIPANT_PASSWORD': '123456',
    'SUPERUSER_USERNAME': 'htx',
    'SUPERUSER_PASSWORD': '123456',
    'JUDGE_USERNAME': 'wzw',
    'JUDGE_PASSWORD': '123456',
    'REGISTER_EMAIL': 'function_test@163.com',
    'REGISTER_USERNAME': 'function_test_username',
    'REGISTER_PASSWORD': '123456',


    'CREATE_CONTEST':{
        'CONTEST_NAME': '功能测试比赛',
        'HOLDERS': ['清华大学','北京大学'],
        'SPONSORS': ['阿里巴巴','腾讯'],
        'CONTEST_TYPE_INDEX':0,
        'DEFAULT_CONTEST_IMAGE' : os.path.join(os.getcwd(), 'test_files/contest_image.jpg'),
        'BRIEF_INTRO': '功能测试比赛简介',
        'DETAIL_INTRO': '功能测试比赛详细介绍',
        #Enroll Time
        'ENROLL_START_TIME': today.strftime('%Y-%m-%d 00:00:00'),
        'ENROLL_END_TIME': today.replace(day = today.day + 1).strftime('%Y-%m-%d 00:00:00'),
        #Stage Time
        'STAGE_NUMBER': 2,
        #stage1
        'STAGE1_START_TIME':today.replace(day = today.day + 1).strftime('%Y-%m-%d 00:00:00'),
        'STAGE1_SUBMIT_END_TIME':today.replace(day = today.day + 2).strftime('%Y-%m-%d 00:00:00'),
        'STAGE1_JUDGE_END_TIME':today.replace(day = today.day + 3).strftime('%Y-%m-%d 00:00:00'),
        #stage2
        'STAGE2_START_TIME': today.replace(day=today.day + 3).strftime('%Y-%m-%d 00:00:00'),
        'STAGE2_SUBMIT_END_TIME': today.replace(day=today.day + 4).strftime('%Y-%m-%d 00:00:00'),
        'STAGE2_JUDGE_END_TIME': today.replace(day=today.day + 5).strftime('%Y-%m-%d 00:00:00'),

    },
}


