from django.shortcuts import render
from .models import *
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.decorators import login_required


def indexSlider(request):
    context = []
    # todo:保存轮播图信息
    contest = Contest.objects.filter()
    contest_id = [contest[0].id, contest[1].id, contest[2].id]
    for i in range(0, 3):
        context.append({'url': '/detail?contestId' + str(contest_id[i]),
                        'img_url': str(contest_id[i]) + '.jpg'})
    return JsonResponse(context)


def indexHotCompetition(request):
    context = []
    # todo:根据比赛参赛情况返回参赛情况最好的 或者 管理员手动管理数据库中某字段
    contest = Contest.objects.filter()
    for i in range(0, 3):
        context.append({'url': '/detail?contestId' + str(contest[i].id),
                        'img_url': str(contest[i].id) + '.jpg',
                       'intro': contest[i].brief_introduction,
                        'title': contest[i].title})
    return JsonResponse(context)


def checkUser(request):
    username = request.POST.get('username')
    contest_id = request.POST('competition_id')
    # do some check
    return JsonResponse({'ok': 1})


def getNeededInfo(request):
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

def createContest(request):
    basicinfo = request.POST.get('basicinfo')
    name = basicinfo.get('name')
    holders = basicinfo.get('holders')
    sponsors = basicinfo.get('sponsors')
    comtype = basicinfo.get('comtype')
    details = basicinfo.get('details')

    signupinfo = request.get('signupinfo')
    time = signupinfo.get('time')
    mode = signupinfo.get('mode')
    person = signupinfo.getlist('person')
    group = signupinfo.getlist('group')

    stageinfo = request.getlist('stageinfo')
    for stage in stageinfo:
        name = stage['name']
        details = stage['details']
        handTimeEnd = stage['handTimeEnd']
        evaluationTimeEnd = stage['evaluationsTimeEnd']
        mode = stage['mode']

    return HttpResponse("")

def personCenter(request):
    id = request.user.id
    img_url = '/resources/user_images/' + id + '.jpg'
    competition = {}
    participated = ContestPlayer.objects.filter(player_id=id)
    competition['participated_competition'] = []
    for contest in participated:
        competition['participated_competition'].append({
            'title': Contest.objects.get(id=contest.contest_id).title,
            'url': '/detail?contestId=' + contest.contest_id,
        })
    created = Contest.objects.filter(admin_id=id)
    competition['created_competition'] = []
    for contest in created:
        competition['created_competition'].append({
            'title': Contest.objects.get(id=contest.contest_id).title,
            'url': '/detail?contestId=' + contest.contest_id,
        })

    rated = ContestJudge.objects.filter(judge_id=id)
    competition['rated_competition'] = []
    for contest in rated:
        competition['rated_competition'].append({
            'title': Contest.objects.get(id=contest.contest_id).title,
            'url': '/detail?contestId=' + contest.contest_id,
        })

    person = {}
    person['university'] = request.user.university
    person['region'] = {}
    person['region']['province'] = request.user.province
    person['region']['city'] = request.user.city
    data = {}
    data['img_url'] = img_url
    data['competition'] = competition
    data['person'] = person
    return JsonResponse(data)
