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
        return HttpResponse('name repeated')
    elif email_unique:
        return HttpResponse('email repeated')
    else:
        CCPUser.objects.create(username=username, password=password, email=email)
        return HttpResponse('')

def login(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data['username']
    password = data['password']
    # print(username, password)
    user = auth.authenticate(username=username, password=password)
    if user:
        auth.login(request, user)
        return HttpResponse('')
    else:
        return HttpResponse('Wrong username or password.')

def check(request):
    username = request.POST.get('username')
    contest_id = request.POST('competition_id')
    #todo: do some check
    return JsonResponse({'ok': 1})

def profile(request):
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
    data = {}
    data['img_url'] = img_url
    data['competition'] = competition
    data['person'] = person
    return JsonResponse(data)

def modify(request):
    id = request.user.id
    username = request.user.username
    data = json.loads(request.body.decode('utf-8'))
    university = data['university']
    province = data['region']['province']
    city = data['region']['city']
    CCPUser.objects.filter(id=id).update(university=university, province=province, city=city)
    return HttpResponse('')
