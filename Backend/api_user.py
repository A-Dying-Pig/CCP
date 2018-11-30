from django.shortcuts import render
from .models import *
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import auth
import json
import os

def register(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data['username']
    email = data['email']
    password = data['password']
    password = make_password(password)
    name_unique = CCPUser.objects.filter(username=username)
    email_unique = CCPUser.objects.filter(email=email)
    if name_unique:
        return JsonResponse({'msg': '用户名已存在！'})
    elif email_unique:
        return JsonResponse({'msg': '邮箱地址已经被注册！'})
    else:
        CCPUser.objects.create(username=username, password=password, email=email)
        return JsonResponse({'msg': ''})

def login(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        password = data['password']
        # print(username, password)
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return JsonResponse({'msg': ''})
        else:
            return JsonResponse({'msg': '用户名或密码错误'})
    except:
        return JsonResponse({'msg': '未知错误！'})

def check(request):
    username = request.POST.get('username')
    contest_id = request.POST('competition_id')
    #todo: do some check
    return JsonResponse({'ok': 1, 'msg': ''})

def profile(request):
    try:
        id = request.user.id
        img_url = '/resources/user_images/' + str(id) + '.jpg'
        competition = {}
        participated = ContestPlayer.objects.filter(player_id=id)
        competition['participated_competition'] = []
        for contest in participated:
            competition['participated_competition'].append({
                'title': Contest.objects.get(id=contest.contest_id).title,
                'url': '/detail?contestid=' + str(contest.contest_id),
            })
        created = Contest.objects.filter(admin_id=id)
        competition['created_competition'] = []
        for contest in created:
            competition['created_competition'].append({
                'title': Contest.objects.get(id=contest.id).title,
                'url': '/detail?contestid=' + str(contest.id),
            })

        rated = ContestJudge.objects.filter(judge_id=id)
        competition['rated_competition'] = []
        for contest in rated:
            competition['rated_competition'].append({
                'title': Contest.objects.get(id=contest.contest_id).title,
                'url': '/detail?contestid=' + str(contest.contest_id),
            })

        user = CCPUser.objects.get(id=id)
        person = {}
        person['university'] = user.university
        person['region'] = {}
        person['region']['province'] = user.province
        person['region']['city'] = user.city
        data = {'msg': ''}
        data['img_url'] = img_url
        data['competition'] = competition
        data['person'] = person
        return JsonResponse(data)
    except:
        return JsonResponse({'msg': '未知错误！'})

def modify(request):
    try:
        id = request.user.id
    except:
        return JsonResponse({'msg': '用户权限认证失败！'})
    username = request.user.username
    data = json.loads(request.body.decode('utf-8'))
    university = data['university']
    province = data['region']['province']
    city = data['region']['city']
    CCPUser.objects.filter(id=id).update(university=university, province=province, city=city)
    return JsonResponse({'msg': ''})
