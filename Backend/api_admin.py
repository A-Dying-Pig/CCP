from .models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .utils import *
from datetime import datetime
import pytz
import django.utils.timezone as tz

utctz=pytz.timezone('UTC')
chinatz=pytz.timezone('Asia/Shanghai')


def participants(request):
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
    if result['mode'] == 1: # 个人赛
        participants= ContestPlayer.objects.filter(contest_id=contest_id)
        participant_number= participants.count()
        if participant_number < 1: # 没数据
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
            single_team['userId'] = participants[index].player_id
            player = CCPUser.objects.get(id=participants[index].player_id)
            single_team['username'] = player.username
            single_team['email'] = player.email
            single_team['points'] = ContestGradeUtil.getGrade(leader_id=single_team['userId'], contest_id=contest_id)
            result['array'].append(single_team)
            index = index + 1
    else:  # 组队赛
        participants = ContestGroup.objects.filter(contest_id=contest_id)
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
            single_team['captainId'] = participants[index].player_id
            player = CCPUser.objects.get(id=participants[index].player_id)
            single_team['captainName'] = player.username
            single_team['captainPoints'] = ContestGradeUtil.getGrade(leader_id=single_team['userId'], contest_id=contest_id)
            single_team['group'] = ContestGroupUtil.getMember(leader_id=single_team['userId'], contest_id=contest_id)
            result['array'].append(single_team)
            index = index + 1
    return JsonResponse(result)

def detail(request):
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

def modify(request):
    data = json.loads(request.body.decode('utf-8'))

    contest_id = int(data['contestid'])

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
        setattr(contest, 'phase_mode' + str(index + 1), stageinfo[index]['mode'])
        setattr(contest, 'phase_start_time' + str(index + 1), datetime.strptime(stageinfo[index]['stageTimeBegin'], "%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc))
        setattr(contest, 'phase_hand_end_time' + str(index + 1), datetime.strptime(stageinfo[index]['handTimeEnd'],"%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc))
        setattr(contest, 'phase_evaluate_end_time' + str(index + 1), datetime.strptime(stageinfo[index]['evaluationTimeEnd'],"%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=pytz.utc))
        index = index + 1
    contest.save()
    return JsonResponse({'msg': ''})

def setjudge(request):
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
        ContestJudge.objects.filter(judge_id=judge_id).delete()
        contest_judge = ContestJudge()
        contest_judge.judge_id = judge_id
        contest_judge.contest_id = contest_id
        setattr(contest_judge, 'phase_region'+str(phase), zone)
        contest_judge.save()
    elif type == 2:
        ContestJudge.objects.filter(judge_id=judge_id).delete()
    
    return JsonResponse({'msg': ''})


def upload(request):
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
        # 打开特定的文件进行二进制的写操作;
        with open(RESOURCE_BASE_DIR + "/resources/contests/" + str(contest_id) + '/contestFile/' + File.name, 'wb+') as f:
            # 分块写入文件;
            for chunk in File.chunks():
                f.write(chunk)
        return JsonResponse({'msg': ''})


def broadcast(request):
    # todo privileges
    data = json.loads(request.body.decode('utf-8'))
    contestid = int(data['contestid'])
    title = data['title']
    content = data['content']
    target_id = data['target']['id']
    target_type = data['target']['type']
    notification = Notification()
    notification.context = content
    notification.title = title
    notification.save()
    msg_id = Notification.objects.last().id
    
    # todo next turn
    if target_id == -1:
        players = ContestPlayer.objects.filter(contest_id=contestid)
    else:
        d = ContestUtil.getCurrentRegionMode(contestid)
        with open('zone.json', 'r', encoding='utf8') as f:
            zone = json.load(f)
        if d == 0: #all
            pass
        elif d == 1: #province
            zone = zone['province'][target_id]
        elif d == 2: #region
            zone = zone['region'][target_id]
        modelcriteria = {'contest_id': contestid, 'phase_region'+str(d): zone}
        players = ContestPlayer.objects.filter(**modelcriteria)

    for player in players:
        pid = player.player_id
        notificationuser = NotificationUser()
        notificationuser.notification_id = msg_id
        notificationuser.user_id = pid
        notificationuser.read = False
        notificationuser.save()

    return JsonResponse({'msg': ''})

def zone(request):
    # todo privilleges
    data = json.loads(request.body.decode('utf-8'))
    contestid = int(data['contestid'])
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

def judgelist(request):
    # todo privileges
    data = json.loads(request.body.decode('utf-8'))
    contestid = int(data['contestid'])
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
    for judge in judges:
        dic = {}
        dic['username'] = CCPUser.objects.filter(id=judge.judge_id)[0].username
        print(dic['username'])
        print(phase)
        print(getattr(judge, 'phase_region'+str(phase)))
        dic['id'] = zone_id[getattr(judge, 'phase_region'+str(phase))]
        res['judges'].append(dic)
    return JsonResponse(res)

def judgeprogress(request):
    # todo privileges
    data = json.loads(request.body.decode('utf-8'))
    contestid = int(data['contestid'])
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


def advanced(request):
    # todo privileges
    data = json.loads(request.body.decode('utf-8'))
    contestid = int(data['contestid'])
    target = int(data['target'])
    res = {}
    res['msg'] = ''
    participants = []
    phase = ContestUtil.getCurrentPhase(contestid)['phase']
    result = ContestGrade.objects.filter(contest_id=contestid).values('leader_id').annotate(average_rating=Avg('grade'))
    for row in result:
        dic = {}
        dic['username'] = CCPUser.objects.filter(id=row.leader_id)[0].username
        dic['university'] = CCPUser.objects.filter(id=row.leader_id)[0].university
        dic['grade'] = row.average_rating
        # default is 0
        dic['advanced'] = 0
        res['participants'].append(dic)
    return JsonResponse(res)

def setadvanced(request):
    # todo privileges
    data = json.loads(request.body.decode('utf-8'))
    contestid = int(data['contestid'])
    target = int(data['target'])
    participants = data['participants']
    # need to be checked carefully
    phase = ContestUtil.getCurrentPhase(contestid)['phase']
    for p in participants:
        contestgrade = ContestGrade()
        leader_id = CCPUser.objects.filter(username=p)[0].id
        contestgrade.leader_id = leader_id
        contestgrade.contest_id = contestid
        contestgrade.phase = phase
        contestgrade.save()
    res = {}
    res['msg'] = ''
    return res
