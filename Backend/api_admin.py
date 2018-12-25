from .models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
import json
from .utils import *
from datetime import datetime
import random
import pytz
import django.utils.timezone as tz

utctz=pytz.timezone('UTC')
chinatz=pytz.timezone('Asia/Shanghai')


def participants(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        contest_id = int(data['contestid'])
        page_num = data['pageNum']

        result = {'msg': ''}
        try:
            contest = Contest.objects.get(id=contest_id)
        except:
            return JsonResponse({'msg': 'Contest does not exist.'})

        try:
            if contest.admin_id != request.user.id:  # 当前用户不是管理员
                return JsonResponse({'msg': 'Current user is not the admin of this contest'})
        except:
            return JsonResponse({'msg': 'Current user is not the admin of this contest'})

        result['mode'] = 1 - contest.grouped
        result['current_page_num'] = page_num
        cur_phase = ContestUtil.getCurrentPhase(contest_id)['phase']
        if cur_phase == 0:
            cur_phase = 1
        if result['mode'] == 1:  # 个人赛
            participants = ContestGrade.objects.filter(contest_id=contest_id, phase=cur_phase)
            participant_number = participants.count()
            if participant_number < 1:  # 没数据
                result['total_page_num'] = 0
                result['array'] = []
                return JsonResponse(result)
            result['total_page_num'] = int(participant_number / MAX_PARTICIPANT_ONE_PAGE) \
                if participant_number % MAX_PARTICIPANT_ONE_PAGE == 0 \
                else int(participant_number / MAX_PARTICIPANT_ONE_PAGE) + 1
            result['array'] = []
            index = MAX_PARTICIPANT_ONE_PAGE * (page_num - 1)
            while index < min(MAX_PARTICIPANT_ONE_PAGE * page_num, participant_number):
                single_team = {}
                single_team['userId'] = participants[index].leader_id
                player = CCPUser.objects.get(id=participants[index].leader_id)
                single_team['username'] = player.username
                single_team['email'] = player.email
                single_team['points'] = ContestGradeUtil.getGrade(leader_id=single_team['userId'], contest_id=contest_id)
                result['array'].append(single_team)
                index = index + 1
        else:  # 组队赛
            participants = ContestGrade.objects.filter(contest_id=contest_id, phase=cur_phase)
            participant_number = participants.count()
            if participant_number < 1:  # 没数据
                result['total_page_num'] = 0
                result['array'] = []
                return JsonResponse(result)
            result['total_page_num'] = int(participant_number / MAX_PARTICIPANT_ONE_PAGE) \
                if participant_number % MAX_PARTICIPANT_ONE_PAGE == 0 \
                else int(participant_number / MAX_PARTICIPANT_ONE_PAGE) + 1
            result['array'] = []
            index = MAX_PARTICIPANT_ONE_PAGE * (page_num - 1)
            while index < min(MAX_PARTICIPANT_ONE_PAGE * page_num, participant_number):
                single_team = {}
                single_team['captainId'] = participants[index].leader_id
                single_team['captainName'] = ContestGroup.objects.get(contest_id=contest_id, leader_id=participants[index].leader_id).group_name
                single_team['captainPoints'] = ContestGradeUtil.getGrade(leader_id=participants[index].leader_id, contest_id=contest_id)
                single_team['group'] = ContestGroupUtil.getMember(leader_id=participants[index].leader_id, contest_id=contest_id)
                result['array'].append(single_team)
                index = index + 1
        return JsonResponse(result)
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def detail(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        contest_id = int(data['contestid'])

        result = {'msg': ''}
        try:
            contest = Contest.objects.get(id=contest_id)
        except:
            return JsonResponse({'msg': 'Contest does not exist.'})

        try:
            if contest.admin_id != request.user.id:  # 当前用户不是管理员
                return JsonResponse({'msg': 'Current user is not the admin of this contest'})
        except:
            return JsonResponse({'msg': 'Current user is not the admin of this contest'})

        result['basicinfo'] = {}
        basicinfo = result['basicinfo']
        basicinfo['name'] = contest.title
        basicinfo['holders'] = ContestUtil.getHost(contest)
        basicinfo['sponsors'] = contest.organizers.split('\n')
        basicinfo['comtype'] = contest.category
        basicinfo['details'] = contest.information

        result['signupinfo'] = {}
        signupinfo = result['signupinfo']
        signupinfo['time'] = [time.mktime(contest.enroll_start.timetuple()) * 1000, time.mktime(contest.enroll_end.timetuple()) * 1000]
        signupinfo['mode'] = 1 - contest.grouped
        signupinfo['person'] = ContestUtil.getTitle(contest)
        signupinfo['group'] = ContestUtil.getGroupTitle(contest)

        result['stageinfo'] = []
        result['stageinfo'] = ContestUtil.getStage(contest)

        return JsonResponse(result)
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def modify(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        contest_id = int(data['contestid'])

        basicinfo = data['basicinfo']
        name = basicinfo['name']
        holders = basicinfo['holders']
        sponsors = basicinfo['sponsors']
        comtype = basicinfo['comtype']
        details = basicinfo['details']
        brief_introduction = basicinfo['briefintroduction']

        signupinfo = data['signupinfo']
        time = signupinfo['time']
        mode = signupinfo['mode']
        person = signupinfo['person']
        group = signupinfo['group']

        stageinfo = data['stageinfo']

        # 在数据库里查找比赛并更新
        if len(holders) > MAX_HOSTS or len(person) > MAX_EXTRA or len(group) > MAX_EXTRA \
                or len(stageinfo) > MAX_PHASE or len(time) != 2:
            return JsonResponse({'msg': 'Too much fields.'})
        try:
            contest = Contest.objects.get(id=contest_id)
        except:
            return JsonResponse({'msg': 'Contest does not exist.'})

        try:
            if contest.admin_id != request.user.id:  # 当前用户不是管理员
                return JsonResponse({'msg': 'Current user is not the admin of this contest'})
        except:
            return JsonResponse({'msg': 'Current user is not the admin of this contest'})

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
            # setattr(contest, 'phase_mode' + str(index + 1), stageinfo[index]['mode'])
            setattr(contest, 'phase_start_time' + str(index + 1), datetime.strptime(stageinfo[index]['stageTimeBegin'], "%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc))
            setattr(contest, 'phase_hand_end_time' + str(index + 1), datetime.strptime(stageinfo[index]['handTimeEnd'],"%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc))
            setattr(contest, 'phase_evaluate_end_time' + str(index + 1), datetime.strptime(stageinfo[index]['evaluationTimeEnd'],"%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc))
            setattr(contest, 'phase_region_mode' + str(index + 1), stageinfo[index]['zone'])
            index = index + 1
        contest.save()
        return JsonResponse({'msg': ''})
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def setjudge(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        contest_id = int(data['contestid'])
        zone_id = data['id']
        type = data['type']
        phase = ContestUtil.getCurrentPhase(contest_id)['phase']
        regionmode = ContestUtil.getCurrentRegionMode(contest_id)
        with open('zone.json', 'r', encoding='utf8') as f:
            zone = json.load(f)
        if regionmode == 1: #province
            zone = zone['province'][zone_id]
        elif regionmode == 2: #region
            zone = zone['region'][zone_id]
        else:
            zone = ''

        try:
            contest = Contest.objects.get(id=contest_id)
        except:
            return JsonResponse({'msg': 'Contest does not exist.'})

        try:
            if contest.admin_id != request.user.id:  # 当前用户不是管理员
                return JsonResponse({'msg': 'Current user is not the admin of this contest'})
        except:
            return JsonResponse({'msg': 'Current user is not the admin of this contest'})

        try:
            judge_id = CCPUser.objects.get(username=username).id
        except:
            return JsonResponse({'msg': 'Judge dos not exist'})
        if type == 0:
            contest_judge = ContestJudge()
            contest_judge.judge_id = judge_id
            contest_judge.contest_id = contest_id
            setattr(contest_judge, 'phase_region'+str(phase), zone)
            contest_judge.save()
        elif type == 1:
            ContestJudge.objects.filter(contest_id=contest_id, judge_id=judge_id).delete()
            contest_judge = ContestJudge()
            contest_judge.judge_id = judge_id
            contest_judge.contest_id = contest_id
            setattr(contest_judge, 'phase_region'+str(phase), zone)
            contest_judge.save()
        elif type == 2:
            ContestJudge.objects.filter(judge_id=judge_id).delete()

        return JsonResponse({'msg': ''})
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def upload(request):
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
            target_dir = '/resources/contests/' + str(contest_id) + '/contestFiles/'
            # GeneralUtil.del_dir(RESOURCE_BASE_DIR + target_dir)
            # 打开特定的文件进行二进制的写操作;
            with open(RESOURCE_BASE_DIR + target_dir + File.name, 'wb+') as f:
                # 分块写入文件;
                for chunk in File.chunks():
                    f.write(chunk)
            return JsonResponse({'msg': ''})
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})


def broadcast(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        contestid = int(data['contestid'])
        if Contest.objects.get(id=contestid).admin_id != request.user.id:
            return JsonResponse({'msg': '当前用户不是比赛主办方账号'})
        title = data['title']
        content = data['content']
        target_id = data['target']['id']
        notification = Notification()
        notification.context = content
        notification.title = title
        notification.save()
        msg_id = Notification.objects.last().id
        grouped = Contest.objects.get(id=contestid).grouped
        if target_id == -1:
            players = []
            plist = ContestPlayer.objects.filter(contest_id=contestid)
            for p in plist:
                players.append(p.player_id)
            plist = ContestGroup.objects.filter(contest_id=contestid)
            for p in plist:
                members = ContestGroupUtil.getMember(p.leader_id, contestid)
                for m in members:
                    players.append(m['userId'])
        else:
            players = []
            d = ContestUtil.getCurrentRegionMode(contestid)
            if d == 0:
                d = 1
            with open('zone.json', 'r', encoding='utf8') as f:
                zone = json.load(f)
            if d == 0: #all
                zone = ''
            elif d == 1: #province
                zone = zone['province'][target_id]
            elif d == 2: #region
                zone = zone['region'][target_id]
            modelcriteria = {'contest_id': contestid, 'phase_region'+str(d): zone}
            if grouped == 0:
                plist = ContestPlayer.objects.filter(**modelcriteria)
                for p in plist:
                    players.append(p.player_id)
            else:
                plist = ContestGroup.objects.filter(**modelcriteria)
                for p in plist:
                    members = ContestGroupUtil.getMember(p.leader_id, contestid)
                    for m in members:
                        players.append(m['userId'])
        for pid in players:
            notificationuser = NotificationUser()
            notificationuser.notification_id = msg_id
            notificationuser.user_id = pid
            notificationuser.read = False
            notificationuser.save()

        return JsonResponse({'msg': ''})
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def zone(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        contestid = int(data['contestid'])
        if Contest.objects.get(id=contestid).admin_id != request.user.id:
            return JsonResponse({'msg': '当前用户不是比赛主办方账号'})
        res = {}
        res['msg'] = ''
        res['list'] = []
        with open('zone.json', 'r', encoding='utf8') as f:
            zone = json.load(f)
        d = ContestUtil.getCurrentRegionMode(contestid)
        cid = 0
        if d == 1: #province
            for province in zone['province']:
                dic = {}
                dic['id'] = cid
                dic['value'] = province
                res['list'].append(dic)
                cid = cid + 1
        elif d == 2: #region
            for region in zone['region']:
                dic = {}
                dic['id'] = cid
                dic['value'] = region
                res['list'].append(dic)
                cid = cid + 1
        return JsonResponse(res)
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def judgelist(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        contestid = int(data['contestid'])
        if Contest.objects.get(id=contestid).admin_id != request.user.id:
            return JsonResponse({'msg': '当前用户不是比赛主办方账号'})
        res = {}
        res['msg'] = ''
        res['judges'] = []
        phase = ContestUtil.getCurrentPhase(contestid)['phase']
        judges = ContestJudge.objects.filter(contest_id=contestid)
        with open('zone.json', 'r', encoding='utf8') as f:
            zone = json.load(f)
        zone_id = {}
        cid = 0
        for province in zone['province']:
            zone_id[province] = cid
            cid = cid + 1
        cid = 0
        for region in zone['region']:
            zone_id[region] = cid
            cid = cid + 1
        zone_id[''] = -1
        zone_id[None] = -1
        for judge in judges:
            dic = {}
            dic['username'] = CCPUser.objects.filter(id=judge.judge_id)[0].username
            print(dic['username'])
            print(phase)
            if phase == 0:
                phase = 1
            print(getattr(judge, 'phase_region'+str(phase)))
            dic['id'] = zone_id[getattr(judge, 'phase_region'+str(phase))]
            res['judges'].append(dic)
        return JsonResponse(res)
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def judgeprogress(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        contestid = int(data['contestid'])
        if Contest.objects.get(id=contestid).admin_id != request.user.id:
            return JsonResponse({'msg': '当前用户不是比赛主办方账号'})
        res = {}
        res['msg'] = ''
        res['judges'] = []
        judges = ContestJudge.objects.filter(contest_id=contestid)
        phase = ContestUtil.getCurrentPhase(contestid)['phase']
        for judge in judges:
            dic = {}
            dic['name'] = CCPUser.objects.filter(id=judge.judge_id)[0].username
            dic['sum'] = ContestGrade.objects.filter(contest_id=contestid, judge_id=judge.id, phase=phase).count()
            dic['finish'] = ContestGrade.objects.filter(contest_id=contestid, judge_id=judge.id, phase=phase).exclude(grade=-1).count()
            res['judges'].append(dic)
        return JsonResponse(res)
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})


def advanced(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        contestid = int(data['contestid'])
        if Contest.objects.get(id=contestid).admin_id != request.user.id:
            return JsonResponse({'msg': '当前用户不是比赛主办方账号'})
        target = int(data['target'])
        res = {}
        res['msg'] = ''
        res['already'] = 0
        res['participants'] = []
        phase = ContestUtil.getCurrentPhase(contestid)['phase']
        try:
            res['already'] = Submitted.objects.get(contest_id=contestid, phase=phase+1, zone_id=target).advanced
        except:
            res['already'] = -1
        cg = ContestGrade.objects.filter(contest_id=contestid).annotate(average_rating=Avg('grade')).order_by('-average_rating')
        result = ContestGrade.objects.filter(contest_id=contestid).values('leader_id').annotate(average_rating=Avg('grade')).order_by('-average_rating')
        #todo htx 提高效率 现在效率太低了
        index = 0
        len_res = len(result)
        while index < len_res:
            if target != -1 and GeneralUtil.get_zone_id(cg[index].contest_id, phase, cg[index].leader_id) != target:
                continue
            row = result[index]
            dic = {}
            user = CCPUser.objects.filter(id=row['leader_id'])[0]
            dic['username'] = user.username
            dic['university'] = user.university
            dic['grade'] = row['average_rating']
            try:
                oldgrade = OldGrade.objects.get(leader_id=user.id, contest_id=contestid, phase=phase)
                dic['oldgrade'] = oldgrade.oldgrade
                dic['reason'] = oldgrade.reason
            except:
                dic['oldgrade'] = -1
                dic['reason'] = ''
            res['participants'].append(dic)
            index = index + 1
        return JsonResponse(res)
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def setnewgrade(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        contestid = int(data['contestid'])
        if Contest.objects.get(id=contestid).admin_id != request.user.id:
            return JsonResponse({'msg': '当前用户不是比赛主办方账号'})
        username = data['username']
        userid = CCPUser.objects.filter(username=username)[0].id
        grade = int(data['grade'])
        reason = data['reason']
        res = {}
        res['msg'] = ''
        phase = ContestUtil.getCurrentPhase(contestid)['phase']
        grades = ContestGrade.objects.filter(contest_id=contestid, leader_id=userid, phase=phase)
        l = len(grades)
        sum = 0
        for g in grades:
            sum = sum + g.grade
        grades.update(grade=grade)
        avg = sum / l
        oldgrade = OldGrade()
        oldgrade.leader_id = userid
        oldgrade.contest_id = contestid
        oldgrade.phase = phase
        oldgrade.oldgrade = avg
        oldgrade.reason = reason
        oldgrade.save()
        return JsonResponse(res)
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def setadvanced(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        contestid = int(data['contestid'])
        if Contest.objects.get(id=contestid).admin_id != request.user.id:
            return JsonResponse({'msg': '当前用户不是比赛主办方账号'})
        target = int(data['target'])
        advanced = int(data['advanced'])
        # need to be checked carefully
        phase = ContestUtil.getCurrentPhase(contestid)['phase']
        if Submitted.objects.filter(contest_id=contestid, phase=phase+1, zone_id=target).count() > 0:
            return JsonResponse({'msg': '不能重复提交晋级名单'})
        cg = ContestGrade.objects.filter(contest_id=contestid).annotate(average_rating=Avg('grade')).order_by('-average_rating')
        result = ContestGrade.objects.filter(contest_id=contestid, phase=phase).values('leader_id').annotate(average_rating=Avg('grade')).order_by('-average_rating')
        # todo htx 提高效率 现在效率太低了
        index = 0
        advanced_count = 0
        len_res = len(result)
        while index < len_res:
            p = result[index]
            if target != -1 and GeneralUtil.get_zone_id(cg[index].contest_id, phase, cg[index].leader_id) != target:
                continue
            contestgrade = ContestGrade()
            leader_id = p['leader_id']
            contestgrade.leader_id = leader_id
            contestgrade.contest_id = contestid
            contestgrade.phase = phase + 1
            contestgrade.save()
            index = index + 1
            advanced_count = advanced_count + 1
            if advanced_count >= advanced:
                break
        submit = Submitted()
        submit.contest_id = contestid
        submit.phase = phase + 1
        submit.zone_id = target
        submit.advanced = advanced
        submit.save()
        res = {}
        res['msg'] = ''
        return JsonResponse(res)
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def getSubmitNum(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({'msg': '请先登录'})
        data = json.loads(request.body.decode('utf-8'))
        contest_id = data['contestid']
        result = {'msg': ''}
        try:
            contest = Contest.objects.get(id=contest_id)
        except:
            return JsonResponse({'msg': '比赛不存在'})
        if contest.admin_id != request.user.id:
            return JsonResponse({'msg': '当前用户不是本比赛管理员'})
        phase = ContestUtil.getCurrentPhase(contest_id)['phase']
        result['submitnum'] = ContestGrade.objects.filter(contest_id=contest_id, phase=phase, work_name__isnull=False).count()
        result['allnum'] = ContestGrade.objects.filter(contest_id=contest_id, phase=phase).count()
        return JsonResponse(result)
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})

def allot_work(contest_id, phase, timesperpiece):
    contest = Contest.objects.get(id=contest_id)
    mode = getattr(contest, 'phase_region_mode' + str(phase))
    if mode == ContestUtil.NON_REGION:
        array = ContestGrade.objects.filter(contest_id=contest_id, phase=phase)
        leader = []
        for row in array:
            leader.append({'id': row.leader_id, 'work': row.work_name})
        random.shuffle(leader)
        ContestGrade.objects.filter(contest_id=contest_id, phase=phase).delete()
        judge_id = []
        array = ContestJudge.objects.filter(contest_id=contest_id)
        for row in array:
            judge_id.append(row.judge_id)
        
        num = len(judge_id)
        i = 0
        for j in range(len(leader)):
            for k in range(timesperpiece):
                contestgrade = ContestGrade()
                contestgrade.leader_id = leader[j]['id']
                contestgrade.work_name = leader[j]['work']
                contestgrade.contest_id = contest_id
                contestgrade.phase = phase
                contestgrade.judge_id = judge_id[i]
                i = (i + 1) % num
                contestgrade.save()
    else:
        with open('zone.json', 'r', encoding='utf8') as f:
            d = json.load(f)
        if mode == ContestUtil.BIG_REGION:
            zonelist = d['region']
        else:
            zonelist = d['province']
        array = ContestGrade.objects.filter(contest_id=contest_id, phase=phase)
        leader = []
        for row in array:
            leader.append({'id': row.leader_id, 'work': row.work_name})
        random.shuffle(leader)
        ContestGrade.objects.filter(contest_id=contest_id, phase=phase).delete()
        judge_id = []
        array = ContestJudge.objects.filter(contest_id=contest_id)
        for row in array:
            judge_id.append(row.judge_id)
        
        for zone in zonelist:
            playeridzone = []
            for l in leader:
                try:
                    contestplayer = ContestPlayer.objects.get(player_id=l['id'], contest_id=contest_id)
                    region = getattr(contestplayer, 'phase_region' + str(phase))
                    if zone == region:
                        playeridzone.append(l)
                except:
                    contestgroup = ContestGroup.objects.get(leader_id=l['id'], contest_id=contest_id)
                    region = getattr(contestgroup, 'phase_region' + str(phase))
                    if zone == region:
                        playeridzone.append(l)
            judgeidzone = []
            for i in judge_id:
                contestjudge = ContestJudge.objects.get(judge_id=i, contest_id=contest_id)
                region = getattr(contestjudge, 'phase_region' + str(phase))
                if zone == region:
                    judgeidzone.append(i)

            num = len(judgeidzone)
            i = 0
            for j in range(len(playeridzone)):
                for k in range(timesperpiece):
                    contestgrade = ContestGrade()
                    contestgrade.leader_id = playeridzone[j]['id']
                    contestgrade.work_name = playeridzone[j]['work']
                    contestgrade.contest_id = contest_id
                    contestgrade.phase = phase
                    contestgrade.judge_id = judgeidzone[i]
                    i = (i + 1) % num
                    contestgrade.save()

def allot(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        contest_id = data['contestid']
        if Contest.objects.get(id=contest_id).admin_id != request.user.id:
            return JsonResponse({'msg': '当前用户不是比赛主办方账号'})
        judgenum = data['judgenum']
        phase = ContestUtil.getCurrentPhase(contest_id)['phase']
        contest = Contest.objects.filter(id=contest_id)[0]
        if getattr(contest, 'phase_judge_start' + str(phase)):
            return JsonResponse({'msg': 'already allotted.'})
        allot_work(contest_id, phase, judgenum)
        setattr(contest, 'phase_judge_start' + str(phase), True)
        contest.save()
        return JsonResponse({'msg': ''})
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误'})


