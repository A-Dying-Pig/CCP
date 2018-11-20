from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth


def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {'username': request.user.username})
    else:
        return render(request, 'index.html', {'username': ''})

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    return render(request, 'login.html', {'message': ''})

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    return render(request, 'register.html', {'message': ''})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def contest(request):
    if request.user.is_authenticated:
        return render(request, 'contest.html', {'username': request.user.username, 'pageNum': 1})
    else:
        return render(request, 'contest.html', {'username': '', 'pageNum': 1})

def detail(request):
    contestId = request.GET.get('contestId')
    print(contestId)
    if request.user.is_authenticated:
        return render(request, 'detail.html', {'username': request.user.username, 'contestid': str(contestId)})
    else:
        return render(request, 'detail.html', {'username': '', 'contestid': str(contestId)})

@login_required(login_url='/login/')
def enroll(request):
    contestId = request.GET.get('contestId')
    return render(request, 'enroll.html', {'contestId': contestId, 'username': request.user.username})

@login_required(login_url='/login')
def profile(request):
    return render(request, 'profile.html', {'username': request.user.username})

@login_required(login_url='/login')
def addContest(request):
    return render(request, 'addContest.html', {'username': request.user.username})

@login_required(login_url='/login')
def superadmin(request):
    return render(request, 'superadmin.html', {'username': request.user.username})
