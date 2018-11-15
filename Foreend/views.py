from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from Backend import api

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {'isLogin': True, 'username': request.user.username})
    else:
        return render(request, 'index.html', {'isLogin': False})

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'GET':
        return render(request, 'login.html', {'message': ''})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {'message': 'incorrect username or password'})

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    if request.method == 'GET':
        return render(request, 'register.html', {'message': ''})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        val = api.createUser(username, password, email)
        if val == 0:
            return HttpResponseRedirect('/login')
        else:
            return render(request, 'register.html', {'message': val})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def contest(request):
    if request.user.is_authenticated:
        return render(request, 'contest.html', {'isLogin': True, 'username': request.user.username, 'pageNum': 1})
    else:
        return render(request, 'contest.html', {'isLogin': False, 'pageNum': 1})

def detail(request):
    contestId = request.GET.get('contestId')
    if request.user.is_authenticated:
        return render(request, 'detail.html', {'isLogin': True, 'username': request.user.username, 'contestId': contestId})
    else:
        return render(request, 'detail.html', {'isLogin': False, 'contestId': contestId})

@login_required
def enroll(request):
    contestId = request.GET.get('contestId')
    return render(request, 'enroll.html', {'contestId': contestId, 'username': request.user.username})

@login_required
def profile(request):
    return render(request, 'profile.html', {'username': request.user.username})

@login_required
def addContest(request):
    return render(request, 'addContest.html', {'username': request.user.username})
