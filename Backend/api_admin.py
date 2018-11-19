from .models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .utils import *

def participants(request):

    pass

def detail(request):

    pass

def modify(request):
    data = json.loads(request.body.decode('utf-8'))

    contest_id = data['contestId']

    basicinfo = data['basicinfo']
    name = basicinfo['name']
    holders = basicinfo['holders']
    sponsors = basicinfo['sponsors']
    comtype = basicinfo['comtype']
    details = basicinfo['details']

    signupinfo = data['signupinfo']
    time = signupinfo['time']
    mode = signupinfo['mode']
    person = signupinfo['person']
    group = signupinfo['group']

    stageinfo = data['stageinfo']

    # 在数据库里创建比赛
    if len(holders) > MAX_HOSTS or len(person) > MAX_EXTRA or len(group) > MAX_EXTRA \
            or len(stageinfo) > MAX_PHASE or len(time) != 2:
        return JsonResponse({'msg': 'Too much fields.'})
    try:
        contest = Contest.objects.get(contest_id=contest_id)
    except:
        return JsonResponse({'msg': 'Contest does not exists.'})

    contest.title = name
    index = 0
    while index < len(holders):
        setattr(contest, 'host' + str(index + 1), holders[index])
        index = index + 1
    index = 0
    while index < len(sponsors):
        contest.organizers = contest.organizers + '\n' + sponsors[index]
        index = index + 1
    contest.category = comtype
    contest.information = details
    contest.enroll_start = time[0]
    contest.enroll_end = time[1]
    contest.grouped = 1 if mode == 0 else 0
    index = 0
    while index < len(person):
        setattr(contest, 'extra_title' + str(index + 1), person[index])
        index = index + 1
    index = 0
    while index < len(group):
        setattr(contest, 'extra_group_title' + str(index + 1), group[index])
        index = index + 1
    index = 0
    while index < len(stageinfo):
        setattr(contest, 'phase_name' + str(index + 1), stageinfo[index]['name'])
        setattr(contest, 'phase_information' + str(index + 1), stageinfo[index]['details'])
        setattr(contest, 'phase_mode' + str(index + 1), stageinfo[index]['mode'])
        setattr(contest, 'phase_hand_end_time' + str(index + 1), stageinfo[index]['hangTimeEnd'])
        setattr(contest, 'phase_evaluate_end_time' + str(index + 1), stageinfo[index]['evaluationsTimeEnd'])
        index = index + 1
    contest.save()
    return JsonResponse({'msg': ''})

def addJudge(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data['username']
    contest_id = data['contestId']
    result = {}
    try:
        judge_id = CCPUser.objects.get(username=username).id
    except:
        return JsonResponse({'msg': 'Judge dos not exist'})

    contest_judge = ContestJudge()
    contest_judge.judge_id = judge_id
    contest_judge.contest_id = contest_id
    contest_judge.save()
    return JsonResponse({'msg': ''})

