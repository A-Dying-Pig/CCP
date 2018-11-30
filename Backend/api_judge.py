from .models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
import json
import os

def getone(request):
    # todo: 设置分配规则，现在直接返回第一个选手的作品
    try:
        judge_id = request.user.id
    except:
        return JsonResponse({'msg': '权限认证失败！'})
    data = json.loads(request.body.decode('utf-8'))
    contest_id = data['contestid']
    user_id = ContestPlayer.objects.filter()[0].id
    files = []
    base_dir = '/resources/contests/' + str(contest_id) + 'works/' + str(user_id) + '/'
    for maindir, subdir, file_name_list in os.walk(base_dir):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)  # 合并成一个完整路径
            files.append(apath)
    return JsonResponse({
        'files': files,
        'msg': ''
    })

def submit(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        judge_id = request.user.id
    except:
        return JsonResponse({'msg': '权限认证失败！'})
    contest_id = data['contestid']
    user_id = data['userId']
    grade = data['grade']
    phase = data['phase']

    try:
        target = ContestGrade.objects.get(contest_id=contest_id, leader_id=user_id, phase=phase, judge_id=judge_id)
    except:
        return JsonResponse({'msg': '相关信息不存在！'})
    target.grade = grade

    return JsonResponse({'msg': ''})

