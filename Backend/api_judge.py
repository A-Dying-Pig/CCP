from .models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
import json
import os
import random
from .utils import ContestUtil,GeneralUtil,RESOURCE_BASE_DIR
import traceback

def getone(request):
    if not request.user.is_authenticated:
        return JsonResponse({'msg': '请先登录'})
    judge_id = request.user.id
    data = json.loads(request.body.decode('utf-8'))
    contest_id = int(data['contestid'])
    participant_id = int(data['participantid'])
    result = {}
    if participant_id == -1:
        participant = ContestGrade.objects.filter(grade=-1, judge_id=judge_id, contest_id=contest_id, phase=ContestUtil.getCurrentPhase(contest_id)['phase'])
        if participant.count() == 0:
            return JsonResponse({'msg': '已无待评作品'})
        participant_id = participant[0].leader_id

    result['participantid'] = participant_id
    base_dir = RESOURCE_BASE_DIR + "/resources/contests/" + str(contest_id) + '/playerFiles/' + str(participant_id)
    children = GeneralUtil.getChildren(base_dir)
    result['msg'] = ''
    result['files'] = children
    return JsonResponse(result)

def submit(request):
    data = json.loads(request.body.decode('utf-8'))
    if not request.user.is_authenticated:
        return JsonResponse({'msg': '请先登录'})
    judge_id = request.user.id
    contest_id = int(data['contestid'])
    user_id = data['userId']
    grade = data['grade']
    phase = data['phase']

    try:
        target = ContestGrade.objects.get(contest_id=contest_id, leader_id=user_id, phase=phase, judge_id=judge_id)
    except:
        return JsonResponse({'msg': '相关信息不存在！'})
    target.grade = grade

    return JsonResponse({'msg': ''})

def finished(request):
    if not request.user.is_authenticated:
        return JsonResponse({'msg': '请先登录'})
    judge_id = request.user.id
    data = json.loads(request.body.decode('utf-8'))
    contest_id = int(data['contestid'])
    res = {}
    res['msg'] = ''
    res['grades'] = []
    result = ContestGrade.objects.filter(contest_id=contest_id, judge_id=judge_id).exclude(grade=-1)
    for row in result:
        dic = {}
        dic['participantid'] = row.leader_id
        dic['grade'] = row.grade
        res['grades'].append(dic)
    return JsonResponse(res)

