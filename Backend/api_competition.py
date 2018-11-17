from django.shortcuts import render
from .models import *
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
import json
import os

def enroll(request):
    pass

def slider(request):
    context = []
    # todo:保存轮播图信息
    contest = Contest.objects.filter()
    contest_id = [contest[0].id, contest[1].id, contest[2].id]
    for i in range(0, 3):
        context.append({'url': '/detail?contestId' + str(contest_id[i]),
                        'img_url': str(contest_id[i]) + '.jpg'})
    return JsonResponse(context)

def hot(request):
    context = []
    # todo:根据比赛参赛情况返回参赛情况最好的 或者 管理员手动管理数据库中某字段
    contest = Contest.objects.filter()
    for i in range(0, 3):
        context.append({'url': '/detail?contestId' + str(contest[i].id),
                        'img_url': str(contest[i].id) + '.jpg',
                        'intro': contest[i].brief_introduction,
                        'title': contest[i].title})
    return JsonResponse(context)

def neededinfo(request):
    contest_id = request.POST['competition_id']
    contest = Contest.objects.filter(id=contest_id)
    if len(contest) != 0:
        target = contest[0]
        comp_type = not target.grouped
        extra = []
        extra_str = target.extra_title
        current_pos = 0
        last_pos = 0
        while current_pos != -1 and current_pos != len(extra_str) - 1:
            last_pos = current_pos
            current_pos = extra_str.find('\n', current_pos)
            extra.append(extra_str[last_pos, current_pos])
        group_min_number = target.group_min_number
        group_max_number = target.group_max_number
        context = {
            'comp_type': comp_type,
            'extra': extra,
            'group_min_number': group_min_number,
            'group_max_number': group_max_number
        }
        return JsonResponse(context)
    else:
        return JsonResponse({})

def create(request):
    data = json.loads(request.body.decode('utf-8'))
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
    for stage in stageinfo:
        name = stage['name']
        details = stage['details']
        handTimeEnd = stage['handTimeEnd']
        evaluationTimeEnd = stage['evaluationsTimeEnd']
        mode = stage['mode']
    #todo 在数据库里创建比赛
    
    return HttpResponse("")

def getonepro(request):
    # todo:根据评分规则返回一个作品，现在直接用第一个
    contest_id = request.POST.get('contestId')
    user_id = CCPUser.objects.filter()
    files = []
    base_dir = '/resources/contests/works/' + str(user_id) + '/'
    for maindir, subdir, file_name_list in os.walk(base_dir):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)  # 合并成一个完整路径
            files.append(apath)
    return JsonResponse({'files': files})



