from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Backend import api

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'render.html')
    elif request.method == 'POST':
        # use Backend api to authenticate
        pass

def register(request):
    if request.method == 'GET':
        # render register html
        pass
    elif request.method == 'POST':
        # use Backend api to create user
        pass

def contest(request):
    # return all contests
    pass

def detail(request):
    # render contest detail
    pass

@login_required
def enroll(request):
    if request.method == 'GET':
        # render signup html
        pass
    elif request.method == 'POST':
        # use Backend api to post
        pass

@login_required
def profile(request):
    if request.method == 'GET':
        # render profile html
        pass
    elif request.method == 'POST':
        # use Backend api to update userinfo
        pass

# Create your views here.
