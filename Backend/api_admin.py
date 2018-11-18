from .models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
import json

def participants(request):
    pass

def detail(request):
    pass

def modify(request):
    pass

def addJudge(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data['username']
    contest_id = data['contestId']
    result = {}
    try:
        judge_id = CCPUser.objects.get(username=username).id
    except:
        return JsonResponse({'msg': 'Judge dos not exist'})

    contest_judge = ContestJudge.objects.create()
    contest_judge.judge_id = judge_id
    contest_judge.contest_id = contest_id
    contest_judge.save()
    return JsonResponse({'msg': ''})

