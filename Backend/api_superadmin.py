from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .utils import *

def contests(request):
    data = json.loads(request.body.decode('utf-8'))
    page_number = data['pageNum']
    response = {}
    contests_number = NonReviewdContest.objects.all().count()
    total_pasges = int(contests_number / MAX_CONTEST_ONE_PAGE) if contests_number % MAX_CONTEST_ONE_PAGE == 0 \
        else int(contests_number / MAX_CONTEST_ONE_PAGE) + 1
    if total_pasges < 1:  # 数据库里没数据
        return JsonResponse({'current_page_num': page_number, 'total_page_num': 0, 'array': []})
    response['current_page_num'] = page_number
    response['total_page_num'] = total_pasges
    response['array'] = []
    index = MAX_CONTEST_ONE_PAGE * (page_number - 1)
    while index < min(MAX_CONTEST_ONE_PAGE * page_number, contests_number):
        target = NonReviewdContest.objects.all()[index]
        response['array'].append({
            'contestid': target.id,
            'title': target.title,
            'holders': ContestUtil.getHost(target),
            'sponsors': target.organizers.split('\n'),
            'img_url': '/resources/contests/images/' + str(target.id) + '.jpg',  # todo:多种格式
            'details': target.information
        })
    return JsonResponse(response)

def detail(request):
    data = json.loads(request.body.decode('utf-8'))
    contest_id = data['contestid']

    result = {}
    contest = NonReviewdContest.objects.get(id=contest_id)
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
    data = json.loads(request.body.decode('utf-8'))
    contest_id = data['contestid']
    passed = data['pass']
    if passed == 0:  # not pass
        target = NonReviewdContest.objects.get(id=contest_id)
        target.checked = True
        return JsonResponse({'msg': ''})
    else:  # pass
        old_contest = NonReviewdContest.objects.get(id=contest_id)
        new_contest = Contest()

        new_contest.title = old_contest.title
        new_contest.category = old_contest.category
        new_contest.grouped = old_contest.grouped
        new_contest.group_min_number = old_contest.group_min_number
        new_contest.group_max_number = old_contest.group_max_number
        new_contest.enroll_start = old_contest.enroll_start
        new_contest.enroll_end = old_contest.enroll_end
        new_contest.information = old_contest.information
        new_contest.brief_introduction = old_contest.brief_introduction
        new_contest.phase_name1 = old_contest.phase_name1
        new_contest.phase_name2 = old_contest.phase_name2
        new_contest.phase_name3 = old_contest.phase_name3
        new_contest.phase_name4 = old_contest.phase_name4
        new_contest.phase_name5 = old_contest.phase_name5
        new_contest.phase_hand_end_time1 = old_contest.phase_hand_end_time1
        new_contest.phase_hand_end_time2 = old_contest.phase_hand_end_time2
        new_contest.phase_hand_end_time3 = old_contest.phase_hand_end_time3
        new_contest.phase_hand_end_time4 = old_contest.phase_hand_end_time4
        new_contest.phase_hand_end_time5 = old_contest.phase_hand_end_time5
        new_contest.phase_evaluate_end_time1 = old_contest.phase_evaluate_end_time1
        new_contest.phase_evaluate_end_time2 = old_contest.phase_evaluate_end_time2
        new_contest.phase_evaluate_end_time3 = old_contest.phase_evaluate_end_time3
        new_contest.phase_evaluate_end_time4 = old_contest.phase_evaluate_end_time4
        new_contest.phase_evaluate_end_time5 = old_contest.phase_evaluate_end_time5
        new_contest.phase_information1 = old_contest.phase_information1
        new_contest.phase_information2 = old_contest.phase_information2
        new_contest.phase_information3 = old_contest.phase_information3
        new_contest.phase_information4 = old_contest.phase_information4
        new_contest.phase_information5 = old_contest.phase_information5
        new_contest.phase_mode1 = old_contest.phase_mode1
        new_contest.phase_mode2 = old_contest.phase_mode2
        new_contest.phase_mode3 = old_contest.phase_mode3
        new_contest.phase_mode4 = old_contest.phase_mode4
        new_contest.phase_mode5 = old_contest.phase_mode5
        new_contest.admin_id = old_contest.admin_id
        new_contest.host1 = old_contest.host1
        new_contest.host2 = old_contest.host2
        new_contest.host3 = old_contest.host3
        new_contest.host4 = old_contest.host4
        new_contest.organizers = old_contest.organizers
        new_contest.extra_title1 = old_contest.extra_title1
        new_contest.extra_title2 = old_contest.extra_title2
        new_contest.extra_title3 = old_contest.extra_title3
        new_contest.extra_title4 = old_contest.extra_title4
        new_contest.extra_group_title1 = old_contest.extra_group_title1
        new_contest.extra_group_title2 = old_contest.extra_group_title2
        new_contest.extra_group_title3 = old_contest.extra_group_title3
        new_contest.extra_group_title4 = old_contest.extra_group_title4

        new_contest.save()
        old_contest.delete()
        return JsonResponse({'msg': ''})
