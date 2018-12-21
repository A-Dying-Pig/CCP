from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from Backend import api_competition

import jwt
import json

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {'musername': request.user.username})
    else:
        return render(request, 'index.html', {'musername': '#undefined'})

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    return render(request, 'login.html', {'message': '#'})

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    return render(request, 'register.html', {'message': '#'})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def contest(request):
    if request.user.is_authenticated:
        return render(request, 'contest.html', {'musername': request.user.username, 'pageNum': 1})
    else:
        return render(request, 'contest.html', {'musername': '#undefined', 'pageNum': 1})

def detail(request):
    contestid = request.GET.get('contestid')
    if request.user.is_authenticated:
        return render(request, 'detail.html', {'musername': request.user.username, 'contestid': str(contestid)})
    else:
        return render(request, 'detail.html', {'musername': '#undefined', 'contestid': str(contestid)})

@login_required(login_url='/login/')
def enroll(request):
    contestid = request.GET.get('contestid')
    return render(request, 'enroll.html', {'contestid': contestid, 'musername': request.user.username})

@login_required(login_url='/login')
def profile(request):
    return render(request, 'profile.html', {'musername': request.user.username})

@login_required(login_url='/login')
def message(request):
    return render(request, 'profile.html', {'musername': request.user.username, 'index': '3'})

@login_required(login_url='/login')
def addContest(request):
    return render(request, 'addContest.html', {'musername': request.user.username})

@login_required(login_url='/login')
def superadmin(request):
    if not request.user.is_superuser:
        return render(request, 'message.html', {'title': '#' ,'msg': 'Unauthorized.', 'musername':request.user.username, 'url':'/'})
    return render(request, 'superadmin.html', {'musername': request.user.username if request.user.is_authenticated else '#undefined'})

def about(request):
    return render(request, 'message.html', {'title': '雷怡然征婚', 'msg': '雷怡然征婚，请加微信号：SJ11235813', 'musername':request.user.username if request.user.is_authenticated else '#undefined', 'url': '#'})

def service(request):
    return render(request, 'message.html', {'title': '雷怡然征婚', 'msg': '雷怡然征婚，请加微信号：SJ11235813', 'musername':request.user.username if request.user.is_authenticated else '#undefined', 'url': '#'})

@login_required(login_url='/login')
def invite(request):
    token = request.GET.get('token')
    with open('config.json', 'r', encoding='utf8') as f:
        d = json.load(f)
        key = d['key']
    try:
        decoded = jwt.decode(token, key, algorithm='HS256')
    except:
        return render(request, 'message.html', {'title': '#', 'msg': '邀请链接失效', 'musername': request.user.username, 'url': '/'})
    if request.user.id != decoded['receiver']:
        return render(request, 'message.html', {'title': '#', 'msg': '邀请链接失效', 'musername': request.user.username, 'url': '/'})
    if api_competition.addGroupUser(decoded['sender'], decoded['receiver'], decoded['contest']):
        return render(request, 'message.html', {'title': '#', 'msg': '加入成功', 'musername': request.user.username, 'url': '/'})
    else:
        return render(request, 'message.html', {'title': '#', 'msg': '邀请链接失效', 'musername': request.user.username, 'url': '/'})
