from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .utils import *
import traceback
import datetime
from dateutil import tz

def contests(request):
    try:
        user = CCPUser.objects.get(id=request.user.id)
    except:
        return JsonResponse({'msg': 'User does not exist.'})
    if not user.is_superuser: # 是超级用户
        return JsonResponse({'msg': 'Authority denied.'})
    data = json.loads(request.body.decode('utf-8'))
    page_number = data['pageNum']
    response = {'msg': ''}
    contests_number = Contest.objects.filter(checked=-1).count()
    total_pasges = int(contests_number / MAX_CONTEST_ONE_PAGE) if contests_number % MAX_CONTEST_ONE_PAGE == 0 \
        else int(contests_number / MAX_CONTEST_ONE_PAGE) + 1
    if total_pasges < 1:  # 数据库里没数据
        return JsonResponse({'msg': '', 'current_page_num': page_number, 'total_page_num': 0, 'array': []})
    response['current_page_num'] = page_number
    response['total_page_num'] = total_pasges
    response['array'] = []
    index = MAX_CONTEST_ONE_PAGE * (page_number - 1)
    while index < min(MAX_CONTEST_ONE_PAGE * page_number, contests_number):
        target = Contest.objects.filter(checked=-1)[index]
        tmp_path = '/resources/contests/' + str(target.id) + '/img/'
        response['array'].append({
            'contestid': target.id,
            'title': target.title,
            'holders': ContestUtil.getHost(target),
            'sponsors': target.organizers.split('\n')[1:],
            'img_url': GeneralUtil.find_first_img(tmp_path, 'contest'),
            'details': target.information
        })
        index = index + 1
    return JsonResponse(response)

def detail(request):
    try:
        user = CCPUser.objects.get(id=request.user.id)
    except:
        return JsonResponse({'msg': 'User does not exist.'})
    if not user.is_superuser: # 是超级用户
        return JsonResponse({'msg': 'Authority denied.'})
    data = json.loads(request.body.decode('utf-8'))
    contest_id = int(data['contestid'])
    result = {'msg': ''}
    contest = Contest.objects.get(id=contest_id)
    if contest.checked != -1: # 如果不是未审核状态
        return JsonResponse({'msg': '该比赛不是未审核状态'})
    result['basicinfo'] = {}
    basicinfo = result['basicinfo']
    basicinfo['name'] = contest.title
    basicinfo['holders'] = ContestUtil.getHost(contest)
    basicinfo['sponsors'] = contest.organizers.split('\n')
    basicinfo['comtype'] = contest.category
    basicinfo['details'] = contest.information

    result['signupinfo'] = {}
    signupinfo = result['signupinfo']
    signupinfo['time'] = [contest.enroll_start, contest.enroll_end]
    signupinfo['mode'] = 1 - contest.grouped
    signupinfo['person'] = ContestUtil.getTitle(contest)
    signupinfo['group'] = ContestUtil.getGroupTitle(contest)

    result['stageinfo'] = []
    result['stageinfo'] = ContestUtil.getStage(contest)

    return JsonResponse(result)

def submit(request):
    try:
        user = CCPUser.objects.get(id=request.user.id)
    except:
        return JsonResponse({'msg': 'User does not exist.'})
    if not user.is_superuser: # 是超级用户
        return JsonResponse({'msg': 'Authority denied.'})
    data = json.loads(request.body.decode('utf-8'))
    contest_id = int(data['contestid'])
    passed = data['pass']
    if passed == 0:  # not pass
        target = Contest.objects.get(id=contest_id)
        target.checked = 0
        return JsonResponse({'msg': ''})
    else:  # pass
        old_contest = Contest.objects.get(id=contest_id)
        old_contest.checked = 1
        old_contest.save()
        return JsonResponse({'msg': ''})

def indexInfo(request):
    try:
        user = CCPUser.objects.get(id=request.user.id)
    except:
        return JsonResponse({'msg': 'User does not exist.'})
    if not user.is_superuser: # 是超级用户
        return JsonResponse({'msg': 'Authority denied.'})
    try:
        cur_time = datetime.datetime.now(tz=datetime.timezone.utc)
        all_contests = Contest.objects.filter(enroll_start__lte=cur_time, enroll_end__gte=cur_time)
        hot_contests = HotContest.objects.all()
        slider = Slider.objects.all()
        contests = []
        for single_contest in all_contests:
            is_slider = 0
            for single_slider in slider:
                if single_slider.contest_id == single_contest.id:
                    is_slider = 1
            is_hot = 0
            for single_hot in hot_contests:
                if single_hot.contest_id == single_contest.id:
                    is_hot = 1
            contests.append({
                'contestid': single_contest.id,
                'is_slider': is_slider,
                'is_hot': is_hot,
                'title': single_contest.title
            })
        return JsonResponse({'msg': '',
                             'contests': contests})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误！'})

def setIndex(request):
    try:
        user = CCPUser.objects.get(id=request.user.id)
    except:
        return JsonResponse({'msg': 'User does not exist.'})
    if not user.is_superuser: # 是超级用户
        return JsonResponse({'msg': 'Authority denied.'})
    try:
        data = json.loads(request.body.decode('utf-8'))
        req_slider = data['slider']
        req_hot = data['hot']
        hots = []
        sliders = []
        for con_id in req_slider:
            try:
                contest = Contest.objects.get(id=con_id)
            except:
                return JsonResponse({'msg': '比赛不存在'})
            sliders.append({'id': con_id, 'title': contest.title})
        for con_id in req_hot:
            try:
                contest = Contest.objects.get(id=con_id)
            except:
                return JsonResponse({'msg': '比赛不存在'})
            hots.append(({'id': con_id, 'title': contest.title, 'brief_introduction': contest.brief_introduction}))
        HotContest.objects.all().delete()
        Slider.objects.all().delete()
        for single_slider in sliders:
            s = Slider()
            s.contest_id = single_slider['id']
            s.title = single_slider['title']
            s.save()
        for single_hot in hots:
            h = HotContest()
            h.contest_id = single_hot['id']
            h.title = single_hot['title']
            h.brief_introduction = single_hot['brief_introduction']
            h.save()
        return JsonResponse({'msg': ''})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误！'})
