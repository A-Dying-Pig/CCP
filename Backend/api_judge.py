from .models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
import json
import os
import random
from .utils import ContestUtil,GeneralUtil,RESOURCE_BASE_DIR
import traceback

def allot(contest_id, phase, timesperpiece):
    contest = Contest.objects.get(id=contest_id)
    mode = getattr(contest, 'phase_region_mode' + str(phase))
    if mode == ContestUtil.NON_REGION:
        array = ContestGrade.objects.filter(contest_id=contest_id, phase=phase)
        leader_id = []
        for row in array:
            leader_id.append(row.leader_id)
        leader_id = random.shuffle(leader_id)
        ContestGrade.objects.filter(contest_id=contest_id, phase=phase).delete()
        judge_id = []
        array = ContestJudge.objects.filter(contest_id=contest_id)
        for row in array:
            judge_id.append(row.judge_id)
        
        num = len(judge_id)
        i = 0
        for j in range(len(leader_id)):
            for k in range(timesperpiece):
                contestgrade = ContestGrade()
                contestgrade.leader_id = leader_id[j]
                contestgrade.contest_id = contest_id
                contestgrade.phase = phase
                contestgrade.judge_id = judge_id[i]
                i = (i + 1) % num
                contestgrade.save()
    else:
        with open('zone.json', 'r', encoding='utf8') as f:
            d = json.load(f)
        if mode == ContestUtil.BIG_REGION:
            zonelist = d['region']
        else:
            zonelist = d['province']
        array = ContestGrade.objects.filter(contest_id=contest_id, phase=phase)
        leader_id = []
        for row in array:
            leader_id.append(row.leader_id)
        leader_id = random.shuffle(leader_id)
        ContestGrade.objects.filter(contest_id=contest_id, phase=phase).delete()
        judge_id = []
        array = ContestJudge.objects.filter(contest_id=contest_id)
        for row in array:
            judge_id.append(row.judge_id)
        
        for zone in zonelist:
            playeridzone = []
            for i in leader_id:
                contestplayer = ContestPlayer.objects.get(player_id=i)
                region = getattr(contestplayer, 'phase_region' + str(phase))
                if zone == region:
                    playeridzone.append(i)
            judgeidzone = []
            for i in judge_id:
                contestjudge = ContestJudge.objects.get(judge_id=i)
                region = getattr(contestjudge, 'phase_region' + str(phase))
                if zone == region:
                    judgeidzone.append(i)

            num = len(judgeidzone)
            i = 0
            for j in range(len(playeridzone)):
                for k in range(timesperpiece):
                    contestgrade = ContestGrade()
                    contestgrade.leader_id = playeridzone[j]
                    contestgrade.contest_id = contest_id
                    contestgrade.phase = phase
                    contestgrade.judge_id = judgeidzone[i]
                    i = (i + 1) % num
                    contestgrade.save()
                

def getone(request):
    try:
        judge_id = request.user.id
    except:
        return JsonResponse({'msg': '权限认证失败！'})
    data = json.loads(request.body.decode('utf-8'))
    contest_id = int(data['contestid'])
    participant_id = data['participantid']
    if participant_id == -1:
        participant = ContestGrade.objects.filter(grade=-1, judge_id=judge_id, contest_id=contest_id, phase=ContestUtil.getCurrentPhase(contest_id)['phase'])
        if participant.count() == 0:
            return JsonResponse({'msg': '已无待评作品'})
        participant_id = participant[0].leader_id
    base_dir = RESOURCE_BASE_DIR + "/resources/contests/" + str(contest_id) + '/playerFiles/' + str(participant_id)
    children = GeneralUtil.getChildren(base_dir)
    return JsonResponse({
        'msg': '',
        'files': children
    })

def submit(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        judge_id = request.user.id
    except:
        return JsonResponse({'msg': '权限认证失败！'})
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
    try:
        judge_id = request.user.id
    except:
        return JsonResponse({'msg': 'Unauthorized'})
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

