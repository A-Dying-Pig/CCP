from django.shortcuts import render
from .models import *
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import auth
import json
import os
from .utils import *
import shutil
import traceback
import datetime
from zipfile import ZipFile, BadZipFile
from django.db.models import Q

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
        new_user = CCPUser.objects.create(username=username, password=password, email=email)
        os.mkdir(RESOURCE_BASE_DIR + '/resources/users/' + str(new_user.id))
        os.mkdir(RESOURCE_BASE_DIR + '/resources/users/' + str(new_user.id) + '/tmp')
        return JsonResponse({'msg': ''})

def login(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        password = data['password']
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
        if not request.user.is_authenticated:
            return JsonResponse({'msg': '请先登录'})
        id = request.user.id
        img_url = '/resources/users/' + str(id) + '/img/'
        img_url = GeneralUtil.find_first_img(img_url, 'user')
        competition = {}
        participated = ContestPlayer.objects.filter(player_id=id)
        competition['participated_competition'] = []
        for contest in participated:
            competition['participated_competition'].append({
                'title': Contest.objects.get(id=contest.contest_id).title,
                'url': '/detail?contestid=' + str(contest.contest_id),
            })
        participated = ContestGroup.objects.filter(Q(leader_id=request.user.id) | Q(member1_id=request.user.id) |
                              Q(member2_id=request.user.id) | Q(member3_id=request.user.id) | Q(member4_id=request.user.id))
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

def uploadImg(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'msg': '请先登录'})
        File = request.FILES.get("file", None)
        if File is None:
            return JsonResponse({'msg': 'File not found.'})
        else:
            # 先删掉原来的文件夹内的头像，再新建一个
            cur_dir = RESOURCE_BASE_DIR + '/resources/users/' + str(request.user.id) + '/img/'
            for file in os.listdir(cur_dir):
                full_path = cur_dir + file
                if os.path.isfile(full_path):
                    os.remove(full_path)
            # 打开特定的文件进行二进制的写操作;
            with open(cur_dir + File.name, 'wb+') as f:
                # 分块写入文件;
                for chunk in File.chunks():
                    f.write(chunk)
            return JsonResponse({'msg': '', 'url': cur_dir[len(RESOURCE_BASE_DIR):] + File.name})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def modify(request):
    if not request.user.is_authenticated:
        return JsonResponse({'msg': '请先登录'})
    data = json.loads(request.body.decode('utf-8'))
    university = data['university']
    province = data['region']['province']
    city = data['region']['city']
    CCPUser.objects.filter(id=request.user.id).update(university=university, province=province, city=city)
    return JsonResponse({'msg': ''})


def upload(request):
    contest_id = int(request.POST['contestid'])
    name = request.POST['name']
    try:
        contest = Contest.objects.get(id=contest_id)
    except:
        return JsonResponse({'msg': 'Contest does not exist.'})
    cur_phase = ContestUtil.getCurrentPhase(contest_id)['phase']
    if not(getattr(contest, 'phase_start_time' + str(cur_phase)) < datetime.datetime.now(datetime.timezone.utc) < getattr(contest, 'phase_hand_end_time' + str(cur_phase))):
        return JsonResponse({'msg': '比赛当前阶段的提交已经截止'})
    if contest.grouped == 0:  # 组队赛
        try:
            ContestPlayer.objects.get(contest_id=contest_id, player_id=request.user.id)
        except:
            return JsonResponse({'msg': 'Current user did not attend this contest'})
    else:  #个人赛
        try:
            ContestGroup.objects.get(contest_id=contest_id, leader_id=request.user.id)
        except:
            return JsonResponse({'msg': 'Current user is not a leader of one group in this contest'})
    cg = ContestGrade.objects.filter(leader_id=request.user.id, contest_id=contest_id, phase=cur_phase)
    if cg.count() == 0:  # 不存在，则创建新的
        cg = ContestGrade()
    else:
        cg = cg[0]
    cg.leader_id = request.user.id
    cg.work_name = name
    cg.phase = cur_phase
    cg.save()

    File = request.FILES.get("file", None)
    if File is None:
        return JsonResponse({'msg': 'File not found.'})
    else:
        # 先删除旧文件夹下所有内容，再打开特定的文件进行二进制的写操作;
        try:
            cur_dir = RESOURCE_BASE_DIR + "/resources/contests/" + str(contest_id) + '/playerFiles/' + str(request.user.id) + '/compress/'
            dirs = os.listdir(cur_dir)
            for dir in dirs:
                if os.path.isfile(dir):  # 删掉原来的压缩文件
                    os.remove(dir)
            with open(cur_dir + File.name, 'wb') as f:
                # 分块写入文件;
                for chunk in File.chunks():
                    f.write(chunk)
            # 解压缩
            extract_dir = RESOURCE_BASE_DIR + "/resources/contests/" + str(contest_id) + '/playerFiles/' + str(request.user.id) + '/decompress/'
            GeneralUtil.del_dir(extract_dir)
            try:
                with ZipFile(cur_dir + File.name) as zfile:
                    zfile.extractall(path=extract_dir)
            except BadZipFile as e:
                traceback.print_exc()
                return JsonResponse({'msg': '文件解压缩出错！'})
            return JsonResponse({'msg': ''})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'msg': '未知错误'})
