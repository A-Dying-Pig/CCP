from django.shortcuts import render
from .models import *
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from Backend import api_mail
import json
import time
import os
from .utils import *
import pytz
from datetime import datetime, timezone, timedelta
import shutil
import jwt
from django.db.models import Q
import traceback
import csv
import pickle

utctz=pytz.timezone('UTC')
chinatz=pytz.timezone('Asia/Shanghai')

def enroll(request):
    if not request.user.is_authenticated:
        return JsonResponse({'msg': '请先登录'})
    data = json.loads(request.body.decode('utf-8'))
    contestid = int(data['contestid'])
    userId = request.user.id
    phone_number = data['phone_number']
    university = data['university']

    try:
        contest = Contest.objects.get(id=contestid)
    except:
        return JsonResponse({'msg': '比赛不存在'})

    comp_type = 1 - contest.grouped
    if comp_type == 0:
        groupuser = data['groupuser']
    fields = data['custom_field']
    values = data['custom_value']

    if contest.grouped == 0:  # 个人赛
        if ContestPlayer.objects.filter(player_id=userId, contest_id=contestid):
            return JsonResponse({'msg': '不能重复报名'})
    else:
        if ContestGroup.objects.filter(Q(contest_id=contestid) & (Q(leader_id=userId) | Q(member1_id=userId) | Q(member2_id=userId) | Q(member3_id=userId) | Q(member4_id=userId))):
            return JsonResponse({'msg': '不能重复报名'})

    if ContestJudge.objects.filter(judge_id=userId, contest_id=contestid):
        return JsonResponse({'msg': '比赛评委不能报名成为比赛选手'})

    try:
        if Contest.objects.get(id=contestid).admin_id == userId:
            return JsonResponse({'msg': '比赛主办方不能报名成为比赛选手'})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

    le = len(values)
    if le < 0 or le > 4:
        return JsonResponse({'msg': '额外信息数目超出限制'})

    if os.path.exists('university.pkl'):
        with open('university.pkl', 'rb') as f:
            uni_dic = pickle.load(f)
    else:
        uni_dic = {}
        with open('university.csv') as f:
            r = csv.DictReader(f)
            for row in r:
                uni_dic[row['University']] = {'province': row['Province'], 'region': row['Region']}
        with open('university.pkl', 'wb') as fw:
            pickle.dump(uni_dic, fw)

    # need to modify database, add fileds to Contestplayer
    if comp_type == 1:  # 个人赛
        with transaction.atomic():
            contest_player = ContestPlayer()
            contest_player.player_id = userId
            contest_player.contest_id = contestid
            contest_player.phone_number = phone_number
            phase_num = ContestUtil.phaseNum(contestid)
            contest = Contest.objects.filter(id=contestid)[0]
            for i in range(1, phase_num+1):
                mode = getattr(contest, 'phase_region_mode' + str(i))
                if mode == 0:
                    setattr(contest_player, 'phase_region' + str(i), '')
                elif mode == 1:
                    try:
                        zone = uni_dic[university]['province']
                    except:
                        zone = '其他'
                    setattr(contest_player, 'phase_region' + str(i), zone)
                elif mode == 2:
                    try:
                        zone = uni_dic[university]['region']
                    except:
                        zone = '其他'
                    setattr(contest_player, 'phase_region' + str(i), zone)
            index = 0
            while index < le:
                setattr(contest_player, 'extra_information' + str(index + 1), values[index])
                index = index + 1
            contest_player.save()
            contest_grade = ContestGrade()
            contest_grade.leader_id = userId
            contest_grade.contest_id = contestid
            contest_grade.phase = 1
            contest_grade.save()
    elif comp_type == 0:  # 组队赛
        with transaction.atomic():
            contest_group = ContestGroup()
            contest_group.contest_id = contestid
            contest_group.leader_id = request.user.id
            glen = len(groupuser)
            if glen < 0 or glen > 4:
                return JsonResponse({'msg': '队员人数超出限制'})
            index = 0
            while index < glen:
                gid = CCPUser.objects.get(username=groupuser[index]).id
                #setattr(contest_group, 'member' + str(index + 1) + '_id', gid)
                send_invitation(userId, gid, contestid)
                index = index + 1
            index = 0
            while index < le:
                setattr(contest_group, 'extra_information' + str(index + 1), values[index])
                index = index + 1
            contest_group.phone_number = phone_number

            phase_num = ContestUtil.phaseNum(contestid)
            contest = Contest.objects.filter(id=contestid)[0]
            for i in range(1, phase_num+1):
                mode = getattr(contest, 'phase_region_mode' + str(i))
                if mode == 0:
                    setattr(contest_group, 'phase_region' + str(i), '')
                elif mode == 1:
                    try:
                        zone = uni_dic[university]['province']
                    except:
                        zone = '其他'
                    setattr(contest_group, 'phase_region' + str(i), zone)
                elif mode == 2:
                    try:
                        zone = uni_dic[university]['region']
                    except:
                        zone = '其他'
                    setattr(contest_group, 'phase_region' + str(i), zone)
            contest_group.save()
            contest_grade = ContestGrade()
            contest_grade.phase = 1
            contest_grade.contest_id = contestid
            contest_grade.leader_id = userId
            contest_grade.save()
    os.mkdir(RESOURCE_BASE_DIR + '/resources/contests/' + str(contestid) + '/playerFiles/' + str(request.user.id))
    os.mkdir(RESOURCE_BASE_DIR + '/resources/contests/' + str(contestid) + '/playerFiles/' + str(request.user.id) + '/decompress')
    os.mkdir(RESOURCE_BASE_DIR + '/resources/contests/' + str(contestid) + '/playerFiles/' + str(request.user.id) + '/compress')
    return JsonResponse({'msg': ''})

def list(request):
    amount = MAX_CONTEST_ONE_PAGE
    data = json.loads(request.body.decode('utf-8'))
    page = int(data['pageNum'])
    type = data['type']
    if type == 'all':
        count = Contest.objects.filter(checked=1).count()
        contests = Contest.objects.filter(checked=1)[(page - 1) * amount: page * amount]
    elif type == 'web':
        count = Contest.objects.filter(checked=1, category='web开发').count()
        contests = Contest.objects.filter(checked=1, category='web开发')[(page - 1) * amount: page * amount]
    elif type == 'weixin':
        count = Contest.objects.filter(checked=1, category='微信小程序').count()
        contests = Contest.objects.filter(checked=1, category='微信小程序')[(page - 1) * amount: page * amount]
    else:
        return JsonResponse({'msg': '不存在的比赛类型'})
    array = []
    for c in contests:
        d = {}
        d['title'] = c.title
        d['intro'] = c.brief_introduction
        d['contestid'] = c.id
        tmp_path = '/resources/contests/' + str(c.id) + '/img/'
        d['img_url'] = GeneralUtil.find_first_img(tmp_path, 'contest')
        d['enroll_number'] = ContestGroup.objects.filter(contest_id=c.id).count() if c.grouped == 1 else ContestPlayer.objects.filter(contest_id=c.id).count()
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
            tmp_path = '/resources/contests/' + str(contest.contest_id) + '/img/'
            context.append({'url': '/detail?contestid=' + str(contest.contest_id),
                            'img_url': GeneralUtil.find_first_img(tmp_path, 'contest')})
        result = {
            'array': context,
            'msg': ''
        }
        return JsonResponse(result)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def hot(request):
    try:
        context = []
        contests = HotContest.objects.all()
        for contest in contests:
            tmp_path = '/resources/contests/' + str(contest.contest_id) + '/img/'
            context.append({
                'url': '/detail?contestid=' + str(contest.contest_id),
                'img_url': GeneralUtil.find_first_img(tmp_path, 'contest'),
                'intro': contest.brief_introduction,
                'title': contest.title
            })
        result = {
            'array': context,
            'msg': ''
        }
        return JsonResponse(result)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def neededinfo(request):
    data = json.loads(request.body.decode('utf-8'))
    contest_id = int(data['contestid'])
    contest = Contest.objects.filter(id=contest_id)
    if len(contest) != 0:
        target = contest[0]
        comp_type = 1 - target.grouped
        extra = ContestUtil.getTitle(target) if comp_type else ContestUtil.getGroupTitle(target)
        group_min_number = target.group_min_number
        group_max_number = target.group_max_number
        context = {
            'comp_type': comp_type,
            'comp_type': comp_type,
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
    print(data)

    basicinfo = data['basicinfo']
    name = basicinfo['name']
    holders = basicinfo['holders']
    sponsors = basicinfo['sponsors']
    comtype = basicinfo['comtype']
    details = basicinfo['details']
    img_url = basicinfo['img']
    brief_introduction = basicinfo['briefintroduction']

    signupinfo = data['signupinfo']
    time = signupinfo['time']
    mode = int(signupinfo['mode'])
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
    contest.brief_introduction = brief_introduction
    contest.enroll_start = datetime.strptime(time[0],"%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc)
    contest.enroll_end = datetime.strptime(time[1],"%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc)
    if mode == 0:
        contest.grouped = 1
        contest.group_min_number = signupinfo['teamnum'][0]
        contest.group_max_number = signupinfo['teamnum'][1]
    elif mode == 1:
        contest.grouped = 0
    else:
        return JsonResponse({'msg': '不支持的比赛模式'})
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
        # setattr(contest, 'phase_mode' + str(index + 1), stageinfo[index]['mode'])
        setattr(contest, 'phase_start_time' + str(index + 1), datetime.strptime(stageinfo[index]['stageTimeBegin'], "%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc))
        setattr(contest, 'phase_hand_end_time' + str(index + 1), datetime.strptime(stageinfo[index]['handTimeEnd'],"%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc))
        setattr(contest, 'phase_evaluate_end_time' + str(index + 1), datetime.strptime(stageinfo[index]['evaluationTimeEnd'],"%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc))
        setattr(contest, 'phase_region_mode' + str(index + 1), stageinfo[index]['zone'])
        index = index + 1
    contest.save()
    os.mkdir(RESOURCE_BASE_DIR + '/resources/contests/' + str(contest.id))
    os.mkdir(RESOURCE_BASE_DIR + '/resources/contests/' + str(contest.id) + '/img')
    os.mkdir(RESOURCE_BASE_DIR + '/resources/contests/' + str(contest.id) + '/playerFiles')
    os.mkdir(RESOURCE_BASE_DIR + '/resources/contests/' + str(contest.id) + '/contestFiles')
    # 将用户目录下的比赛图片的临时文件放到文件系统规定好的位置
    source_dir = RESOURCE_BASE_DIR + img_url
    filename = source_dir[(1 + source_dir.rfind('/')):]
    dest_dir = RESOURCE_BASE_DIR + '/resources/contests/' + str(contest.id) + '/img/' + filename
    with open(source_dir, 'rb') as fs:
        # 分块写入文件;
        with open(dest_dir, 'wb+') as fd:
            fd.write(fs.read())
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
        elif ContestGroup.objects.filter(Q(contest_id=contest_id) & (Q(leader_id=user_id) | Q(member1_id=user_id) | Q(member2_id=user_id) | Q(member3_id=user_id) | Q(member4_id=user_id))):
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
        basicinfo['sponsors'] = contest.organizers.split('\n')[1:]
        basicinfo['comtype'] = contest.category
        basicinfo['details'] = contest.information
        basicinfo['briefintroduction'] = contest.brief_introduction
        basicinfo['img'] = GeneralUtil.find_first_img('/resources/contests/' + str(contest_id) + '/img/', 'contest')
        phase = ContestUtil.getCurrentPhase(contest.id)['phase']
        if phase == 0:
            phase = 1
        basicinfo['judgebegin'] = getattr(contest, 'phase_judge_start'+str(phase))

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
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误！'})

def fileList(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        contest_id = int(data['contestid'])
        contest_path = RESOURCE_BASE_DIR + "/resources/contests/" + str(contest_id) + "/contestFiles"
        files = os.listdir(contest_path)
        result = []
        for file in files:
            entire_dir = os.path.join(contest_path, file)
            if os.path.isfile(entire_dir):
                result.append({
                    'name': file,
                    'url': entire_dir[len(RESOURCE_BASE_DIR):],
                    'size': str((os.path.getsize(entire_dir) - 1) // 1024 + 1) + 'KB'
                })
        return JsonResponse({'msg': '',
                             'files': result})
    except Exception as e:
        traceback.print_exc()
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
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def uploadImg(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'msg': '请先登录'})
        File = request.FILES.get("file", None)
        if File is None:
            return JsonResponse({'msg': 'File not found.'})
        else:
            # 暂存临时文件
            cur_dir = RESOURCE_BASE_DIR + '/resources/users/' + str(request.user.id) + '/tmp/' + str(time.time()) + '/'
            os.mkdir(cur_dir)
            # 打开特定的文件进行二进制的写操作;
            with open(cur_dir + File.name, 'wb+') as f:
                # 分块写入文件;
                for chunk in File.chunks():
                    f.write(chunk)
            return JsonResponse({'msg': '', 'url': cur_dir[len(RESOURCE_BASE_DIR):] + File.name})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def send_invitation(sender_id, receiver_id, contest_id):
    sender_name = CCPUser.objects.filter(id=sender_id)[0].username
    with open('config.json', 'r', encoding='utf8') as f:
        d = json.load(f)
        key = d['key']
        domain = d['domain']
    encoded = jwt.encode({'sender': sender_id, 'receiver': receiver_id, 'contest': contest_id}, key, algorithm='HS256')
    link = domain + '/invite?token=' + encoded.decode('utf8')
    msg = sender_name + '邀请你加入队伍，点击链接' + link
    notification = Notification()
    notification.context = msg
    notification.title = sender_name + '邀请你加入队伍'
    notification.time = datetime.now(timezone.utc)
    notification.save()
    msg_id = Notification.objects.last().id
    ntfuser = NotificationUser()
    ntfuser.notification_id = msg_id
    ntfuser.user_id = receiver_id
    ntfuser.save()
    email = CCPUser.objects.filter(id=receiver_id)[0].email
    api_mail.sendmail(sender_name + '邀请你加入队伍', msg, email)


def addGroupUser(leader_id, member_id, contest_id):
    cg_obj = ContestGroup.objects.filter(leader_id=leader_id, contest_id=contest_id)[0]
    ContestGroupUtil.addMember(cg_obj, member_id)
    return True

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
                'imgurl': GeneralUtil.find_first_img('/resources/users/' + str(single_reply.author_id) + '/img/', 'user'),
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
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def addDiscussion(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'msg': '请先登录'})
        data = json.loads(request.body.decode('utf-8'))
        contest_id = int(data['contestid'])
        title = data['title']
        content = data['content']
        if len(title) == 0:
            return JsonResponse({'msg': '发帖主题不能为空！'})
        if len(content) == 0:
            return JsonResponse({'msg': '发帖内容不能为空！'})
        post = Post()
        post.contest_id = contest_id
        post.author_id = request.user.id
        post.author = CCPUser.objects.get(id=request.user.id).username
        post.title = title
        post.content = content
        post.time = datetime.now(tz=utctz)
        post.last_reply_time = datetime.now(tz=utctz)
        post.save()
        return JsonResponse({'msg': ''})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def discussionReply(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'msg': '请先登录'})
        data = json.loads(request.body.decode('utf-8'))
        contest_id = int(data['contestid'])
        post_id = int(data['discussionid'])
        content = data['content']
        if len(content) == 0:
            return JsonResponse({'msg': '发帖内容不能为空！'})
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
                reply.time = datetime.now(timezone.utc)
                post.replies = post.replies + 1
                post.last_reply_time = reply.time
                reply.save()
                post.save()
                return JsonResponse({'msg': ''})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'msg': '数据不符合要求'})
    except Exception as e:
        traceback.print_exc()
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
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})


def worksname(request):
    data = json.loads(request.body.decode('utf-8'))
    contestid = data['contestid']
    userid = request.user.id
    filename = ''
    try:
        dirs = os.listdir(RESOURCE_BASE_DIR + '/resources/contests/' + str(contestid) + '/playerFiles/' + str(userid) + '/compress/')
    except:
        return JsonResponse({'msg': '', 'filename': ''})
    for d in dirs:
        if os.path.isfile(RESOURCE_BASE_DIR + '/resources/contests/' + str(contestid) + '/playerFiles/' + str(userid) + '/compress/' + d):
            filename = d
            break
    return JsonResponse({'msg': '', 'filename': filename})
