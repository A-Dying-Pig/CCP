from django.shortcuts import render
from .models import *
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
import json
import time
import os
from .utils import *
import pytz
from datetime import datetime
import shutil

utctz=pytz.timezone('UTC')
chinatz=pytz.timezone('Asia/Shanghai')

def enroll(request):
    if not request.user.is_authenticated:
        return JsonResponse({'msg': '请先登录'})
    data = json.loads(request.body.decode('utf-8'))
    contestid = int(data['contestid'])
    userId = request.user.id
    province = data['region']['province']
    city = data['region']['city']
    university = data['university']

    try:
        contest = Contest.objects.get(id=contestid)
    except:
        return JsonResponse({'msg': '比赛不存在'})

    comp_type = contest.grouped
    if comp_type == 1:
        groupuser = data['groupuser']
    fields = data['custom_field']
    values = data['custom_value']

    if ContestPlayer.objects.filter(player_id=userId, contest_id=contestid):
        return JsonResponse({'msg': '不能重复报名'})

    if ContestJudge.objects.filter(judge_id=userId, contest_id=contestid):
        return JsonResponse({'msg': '比赛评委不能报名成为比赛选手'})

    try:
        if Contest.objects.get(id=contestid).admin_id == userId:
            return JsonResponse({'msg': '比赛主办方不能报名成为比赛选手'})
    except Exception as e:
        print(e)
        return JsonResponse({'msg': '未知错误'})

    le = len(values)
    if le < 0 or le > 4:
        return JsonResponse({'msg': '额外信息数目超出限制'})

    # need to modify database, add fileds to Contestplayer
    if comp_type == 0:  # 个人赛
        contest_player = ContestPlayer()
        contest_player.player_id = userId
        contest_player.contest_id = contestid
        index = 0
        while index < le:
            setattr(contest_player, 'extra_information' + str(index + 1), values[index])
            index = index + 1
        contest_player.save()
    elif comp_type == 1:  # 组队赛
        contest_group = ContestGroup()
        contest_group.leader_id = request.user.id
        glen = len(groupuser)
        if glen < 0 or glen > 4:
            return JsonResponse({'msg': '队员人数超出限制'})
        index = 0
        while index < glen:
            setattr(contest_group, 'member' + str(index + 1) + '_id', groupuser[index])
            index = index + 1
        index = 0
        while index < le:
            setattr(contest_group, 'extra_information' + str(index + 1), values[index])
            index = index + 1
    return JsonResponse({'msg': ''})

def list(request):
    amount = MAX_CONTEST_ONE_PAGE
    data = json.loads(request.body.decode('utf-8'))
    page = int(data['pageNum'])
    type = data['type']
    count = Contest.objects.filter(checked=1).count()
    contests = Contest.objects.filter(checked=1)[(page - 1) * amount: page * amount]
    array = []
    for c in contests:
        d = {}
        d['title'] = c.title
        d['intro'] = c.brief_introduction
        d['contestid'] = c.id
        d['img_url'] = '/static/img' + str(c.id) + '.jpg'
        array.append(d)
    total_page_num = (count - 1) // amount + 1
    return JsonResponse({
        'total_page_num': total_page_num,
        'current_page_num': page,
        'array': array,
        'msg': ''
    })

def slider(request):
    try:
        context = []
        contests = Slider.objects.all()
        for contest in contests:
            context.append({'url': '/detail?contestid=' + str(contest.contest_id),
                            'img_url': '/static/img/' + str(contest.contest_id) + '.jpg'})
        result = {
            'array': context,
            'msg': ''
        }
        return JsonResponse(result)
    except Exception as e:
        print(e)
        return JsonResponse({'msg': '未知错误'})

def hot(request):
    try:
        context = []
        contests = HotContest.objects.all()
        for contest in contests:
            context.append({
                'url': 'detail?contestid=' + str(contest.contest_id),
                'img_url': '/static/img/' + str(contest.contest_id) + '.jpg',
                'intro': contest.brief_introduction,
                'title': contest.brief_introduction
            })
        result = {
            'array': context,
            'msg': ''
        }
        return JsonResponse(result)
    except Exception as e:
        print(e)
        return JsonResponse({'msg': '未知错误'})

def neededinfo(request):
    data = json.loads(request.body.decode('utf-8'))
    contest_id = int(data['contestid'])
    contest = Contest.objects.filter(id=contest_id)
    if len(contest) != 0:
        target = contest[0]
        comp_type = not target.grouped
        extra = ContestUtil.getTitle(target)
        group_min_number = target.group_min_number
        group_max_number = target.group_max_number
        context = {
            'comp_type': 1 if comp_type else 0,
            'extra': extra,
            'group_min_number': group_min_number,
            'group_max_number': group_max_number,
            'msg': ''
        }
        return JsonResponse(context)
    else:
        return JsonResponse({'msg': '您所要查找的信息不存在！'})

def create(request):
    data = json.loads(request.body.decode('utf-8'))

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

    contest = Contest()
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
    contest.enroll_start = datetime.strptime(time[0],"%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc)
    contest.enroll_end = datetime.strptime(time[1],"%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc)
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
        setattr(contest, 'phase_start_time' + str(index + 1), datetime.strptime(stageinfo[index]['stageTimeBegin'], "%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc))
        setattr(contest, 'phase_hand_end_time' + str(index + 1), datetime.strptime(stageinfo[index]['handTimeEnd'],"%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc))
        setattr(contest, 'phase_evaluate_end_time' + str(index + 1), datetime.strptime(stageinfo[index]['evaluationTimeEnd'],"%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc))
        index = index + 1
    contest.save()
    return JsonResponse({'code': 0, 'msg': ''})

def detail(request):
    data = json.loads(request.body.decode('utf-8'))
    contest_id = int(data['contestid'])

    result = {'msg': ''}
    user_id = request.user.id
    try:
        contest = Contest.objects.get(id=contest_id)
        result['type'] = 0
        if ContestPlayer.objects.filter(player_id=user_id, contest_id=contest_id).count() == 1:
            result['type'] = 1
        elif ContestJudge.objects.filter(judge_id=user_id, contest_id=contest_id).count() == 1:
            result['type'] = 2
        elif contest.admin_id == user_id:
            result['type'] = 3
        result['info'] = {}
        info = result['info']
        info['basicinfo'] = {}
        basicinfo = info['basicinfo']
        basicinfo['name'] = contest.title
        basicinfo['holders'] = ContestUtil.getHost(contest)
        basicinfo['sponsors'] = contest.organizers.split('\n')
        basicinfo['comtype'] = contest.category
        basicinfo['details'] = contest.information

        info['signupinfo'] = {}
        signupinfo = info['signupinfo']
        signupinfo['time'] = [(time.mktime(contest.enroll_start.timetuple()) + 8 * 60 * 60) * 1000, (time.mktime(contest.enroll_end.timetuple()) + 8 * 60 * 60) * 1000]
        signupinfo['mode'] = 1 - contest.grouped
        signupinfo['person'] = ContestUtil.getTitle(contest)
        signupinfo['group'] = ContestUtil.getGroupTitle(contest)

        result['info']['stageinfo'] = []
        result['info']['stageinfo'] = ContestUtil.getStage(contest)
        return JsonResponse(result)
    except Exception as e:
        print("Exception here:")
        print(e)
        return JsonResponse({'msg': '未知错误！'})

def fileList(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        contest_id = int(data['contestid'])
        contest_path = "/resources/contests/" + str(contest_id)
        files = os.listdir(contest_path)
        result = []
        for file in files:
            entire_dir = os.path.join(contest_path, file)
            if os.path.isfile(entire_dir):
                result.append({
                    'name': file,
                    'url': entire_dir,
                    'size': os.path.getsize(entire_dir)
                })
        return JsonResponse({'msg': '',
                             'files': result})
    except Exception as e:
        print(e)
        return JsonResponse({'msg': '未知错误！'})

def enrollNum(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        contest_id = int(data['contestid'])
        try:
            contest = Contest.objects.get(id=contest_id)
        except:
            return JsonResponse({'msg': '比赛不存在'})
        if contest.grouped == 1:  # 组队赛
            num = ContestGroup.objects.filter(contest_id=contest_id).count()
        else:
            num = ContestPlayer.objects.filter(contest_id=contest_id).count()
        return JsonResponse({'msg': '', 'enrollnum': num})
    except Exception as e:
        print(e)
        return JsonResponse({'msg': '未知错误'})

def uploadImg(request):
    try:
        contest_id = int(request.POST['contestid'])
        try:
            contest = Contest.objects.get(id=contest_id)
        except:
            return JsonResponse({'msg': 'Contest does not exist.'})

        try:
            if contest.admin_id != request.user.id:  # 当前用户不是管理员
                return JsonResponse({'msg': 'Current user is not the admin of this contest'})
        except:
            return JsonResponse({'msg': 'Current user is not the admin of this contest'})

        File = request.FILES.get("file", None)
        if File is None:
            return JsonResponse({'msg': 'File not found.'})
        else:
            # 先删掉原来的文件夹内的所有内容，再新建一个
            shutil.rmtree(RESOURCE_BASE_DIR + '/resources/contests/' + str(contest_id))
            os.mkdir(RESOURCE_BASE_DIR + '/resources/contests/' + str(contest_id))
            # 打开特定的文件进行二进制的写操作;
            with open(RESOURCE_BASE_DIR + "/resources/contests/" + str(contest_id) + '/img/' + File.name, 'wb+') as f:
                # 分块写入文件;
                for chunk in File.chunks():
                    f.write(chunk)
            return JsonResponse({'msg': ''})
    except Exception as e:
        print(e)
        return JsonResponse({'msg': '未知错误'})

def discussion(request):
    try:
        amount = MAX_REPLY_ONE_PAGE
        data = json.loads(request.body.decode('utf-8'))
        contest_id = int(data['contestid'])
        post_id = int(data['discussionid'])
        page = data['pageNum']
        try:
            post = Post.objects.get(id=post_id)
        except:
            return JsonResponse({'msg': '主题帖不存在'})
        if contest_id != post.contest_id:
            return JsonResponse({'msg': '比赛与主题帖不匹配'})
        result = {'msg': ''}
        result['current_page_num'] = page
        count = Reply.objects.filter(post_id=post_id).count()
        replys = Reply.objects.filter(post_id=post_id)[(page - 1) * amount: page * amount]
        result['total_page_num'] = (count - 1) // amount + 1
        result['title'] = post.title
        result['content'] = post.content
        result['author'] = post.author
        result['issuetime'] = (time.mktime(post.time.timetuple()) + 8 * 60 * 60) * 1000
        result['array'] = []
        for single_reply in replys:
            result['array'].append({
                'imgurl': "/resources/user_images/" + str(single_reply.author_id) + '/',
                'username': single_reply.author,
                'content': single_reply.content,
                'time': (time.mktime(single_reply.time.timetuple()) + 8 * 60 * 60) * 1000
            })
        with transaction.atomic():
            post = Post.objects.select_for_update().get(id=post_id)
            post.views = post.views + 1
            post.save()
        return JsonResponse(result)
    except Exception as e:
        print(e)
        return JsonResponse({'msg': '未知错误'})

def addDiscussion(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'msg': '请先登录'})
        data = json.loads(request.body.decode('utf-8'))
        contest_id = int(data['contestid'])
        title = data['title']
        content = data['content']
        post = Post()
        post.contest_id = contest_id
        post.author_id = request.user.id
        post.author = CCPUser.objects.get(id=request.user.id).username
        post.title = title
        post.content = content
        post.time = datetime.utcnow()
        post.save()
        return JsonResponse({'msg': ''})
    except Exception as e:
        print(e)
        return JsonResponse({'msg': '未知错误'})

def discussionReply(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'msg': '请先登录'})
        data = json.loads(request.body.decode('utf-8'))
        contest_id = int(data['contestid'])
        post_id = int(data['discussionid'])
        content = data['content']
        reply_time = data['replytime']
        try:
            with transaction.atomic():
                try:
                    post = Post.objects.select_for_update().get(id=post_id, contest_id=contest_id)
                except:
                    return JsonResponse({'msg': '主题帖不存在'})
                reply = Reply()
                reply.post_id = post_id
                reply.author_id = request.user.id
                reply.author = CCPUser.objects.get(id=request.user.id).username
                reply.content = content
                reply.time = datetime.strptime(reply_time, "%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc)
                post.replies = post.replies + 1
                post.last_reply_time = reply.time
                reply.save()
                post.save()
                return JsonResponse({'msg': ''})
        except Exception as e:
            print(e)
            return JsonResponse({'msg': '数据不符合要求'})
    except Exception as e:
        print(e)
        return JsonResponse({'msg': '未知错误'})

def discussionList(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        try:
            page = data['pageNum']
        except:
            page = 1
        amount = MAX_POST_ONE_PAGE
        contest_id = int(data['contestid'])
        result = {'msg': ''}
        count = Post.objects.filter(contest_id=contest_id).count()
        posts = Post.objects.filter(contest_id=contest_id)[(page - 1) * amount: page * amount]
        result['current_page_num'] = page
        result['total_page_num'] = (count - 1) // amount + 1
        result['array'] = []
        for post in posts:
            result['array'].append({
                'discussionid': post.id,
                'title': post.title,
                'author': post.author,
                'issuetime': (time.mktime(post.time.timetuple()) + 8 * 60 * 60) * 1000,
                'replynum': post.replies,
                'lasttime': (time.mktime(post.last_reply_time.timetuple()) + 8 * 60 * 60) * 1000,
                'viewnum': post.views
            })
        return JsonResponse(result)
    except Exception as e:
        print(e)
        return JsonResponse({'msg': '未知错误'})
