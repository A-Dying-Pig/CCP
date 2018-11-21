from .models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .utils import *

def participants(request):
    data = json.loads(request.body.decode('utf-8'))

    contest_id = data['contestid']
    page_num = data['pageNum']

    result = {}
    try:
        contest = Contest.objects.get(id=contest_id)
    except:
        return JsonResponse({'msg': 'Contest does not exist.'})
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

    contest_id = data['contestid']

    result = {}
    contest = Contest.objects.get(id=contest_id)
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

    contest_id = data['contestid']

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
        contest = Contest.objects.get(contest_id=contest_id)
    except:
        return JsonResponse({'msg': 'Contest does not exists.'})

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
    contest.enroll_start = time[0]
    contest.enroll_end = time[1]
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
        setattr(contest, 'phase_hand_end_time' + str(index + 1), stageinfo[index]['handTimeEnd'])
        setattr(contest, 'phase_evaluate_end_time' + str(index + 1), stageinfo[index]['evaluationTimeEnd'])
        index = index + 1
    contest.save()
    return JsonResponse({'msg': ''})

def addJudge(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data['username']
    contest_id = data['contestid']
    result = {}
    try:
        judge_id = CCPUser.objects.get(username=username).id
    except:
        return JsonResponse({'msg': 'Judge dos not exist'})

    contest_judge = ContestJudge()
    contest_judge.judge_id = judge_id
    contest_judge.contest_id = contest_id
    contest_judge.save()
    return JsonResponse({'msg': ''})

def upload(request):
    File = request.FILES.get("upload_file", None)
    if File is None:
        return JsonResponse({'msg': 'File not found.'})
    else:
        # 打开特定的文件进行二进制的写操作;
        with open("/resources/contests/" % File.name, 'wb') as f:
            # 分块写入文件;
            for chunk in File.chunks():
                f.write(chunk)
        return JsonResponse({'msg': ''})
