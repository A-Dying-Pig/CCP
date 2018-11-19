from django.shortcuts import render
from .models import *
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
import json
import os
from .utils import *

def enroll(request):
    data = json.loads(request.body.decode('utf-8'))
    contestId = data['contestId']
    userId = request.user.id
    province = data['region']['province']
    city = data['region']['city']
    university = data['university']
    comp_type = data['comp_type']
    groupuser = data['groupuser']
    fields = data['custom_field']
    values = data['custom_value']

    contest_player = ContestPlayer()
    contest_player.player_id = userId
    contest_player.contest_id = contestId
    # need to modify database, add fileds to Contestplayer
    le = len(values)
    contest_player.extra_information1 = '' if le < 1 else values[0] 
    contest_player.extra_information1 = '' if le < 2 else values[1]
    contest_player.extra_information1 = '' if le < 3 else values[2]
    contest_player.extra_information1 = '' if le < 4 else values[3]
    contest_player.save()

    return JsonResponse("")

def list(request):
    amount = 10
    data = json.loads(request.body.decode('utf-8'))
    page = int(data['pageNum'])
    type = data['type']
    count = Contest.objects.filter().count()[(page - 1) * amount: page * amount]
    contests = Contest.objects.all()[page * amount]
    array = []
    for c in contests:
        d = {}
        d['title'] = c.title
        d['intro'] = c.brief_introduction
        d['contestId'] = c.id
        d['img_url'] = str(c.id) + '.jpg'
        array.append(d)
    total_page_num = (count - 1) // amount + 1
    return JsonResponse({
        'total_page_num': total_page_num,
        'current_page_num': page,
        'array': array
    })

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
    print(data)

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
        return JsonResponse({'code': 1, 'msg': 'Too much fields.'})

    contest = NonReviewdContest()
    contest.admin_id = request.user.id
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
        setattr(contest, 'phase_hand_end_time' + str(index + 1), stageinfo[index]['handTimeEnd'])
        setattr(contest, 'phase_evaluate_end_time' + str(index + 1), stageinfo[index]['evaluationTimeEnd'])
        index = index + 1
    contest.save()
    return JsonResponse({'code': 0, 'msg': ''})

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

