# 一些辅助函数
from .models import *
import time

MAX_HOSTS = 4  # 最大主办方人数
MAX_PHASE = 5
MAX_EXTRA = 4
MAX_MEMBER = 5
MAX_CONTEST_ONE_PAGE = 10
MAX_PARTICIPANT_ONE_PAGE = 10

class ContestUtil:
    NON_REGION = 0
    BIG_REGION = 1
    PROVINCE_REGION = 2
    @classmethod
    def getStage(cls, contest):
        result = []
        for i in range(0,5):
            if getattr(contest, 'phase_name'+str(i+1)) is not None:
                tmp_dict = {}
                tmp_dict['name'] = getattr(contest, 'phase_name'+str(i+1))
                tmp_dict['details'] = getattr(contest, 'phase_information'+str(i+1))
                tmp_dict['stageTimeBegin'] = (time.mktime(getattr(contest, 'phase_start_time' + str(i+1)).timetuple()) + 8 * 60 * 60 * 1000) * 1000
                tmp_dict['handTimeEnd'] = (time.mktime(getattr(contest, 'phase_hand_end_time'+str(i+1)).timetuple()) + 8 * 60 * 60 * 1000) * 1000
                tmp_dict['evaluationTimeEnd'] = (time.mktime(getattr(contest, 'phase_evaluate_end_time' + str(i+1)).timetuple()) + 8 * 60 * 60 * 1000) * 1000
                tmp_dict['mode'] = getattr(contest, 'phase_mode'+str(i+1))
                result.append(tmp_dict)
            else:
                break
        return result

    @classmethod
    def getHandTime(cls, contest, index):
        pass

    @classmethod
    def setHandTime(cls, contest, index, time):
        setattr(contest, 'phase_hand_end_time' + str(index), time)
        pass

    @classmethod
    def getEvaluateTime(cls, contest, index):
        pass

    @classmethod
    def setEvaluateTime(cls, contest, index, time):
        pass

    @classmethod
    def getInfo(cls, contest, index):
        pass

    @classmethod
    def setInfo(cls, contest, index, info):
        pass

    @classmethod
    def getMode(cls, contest, index):
        pass

    @classmethod
    def setMode(cls, contest, index, mode):
        pass

    @classmethod
    def getHost(cls, contest):
        result = []
        if contest.host1 is not None:
            result.append(contest.host1)
            if contest.host2 is not None:
                result.append(contest.host2)
                if contest.host3 is not None:
                    result.append(contest.host3)
                    if contest.host4 is not None:
                        result.append(contest.host4)
        return result

    @classmethod
    def setHost(cls, contest, index, host):
        pass

    @classmethod
    def getTitle(cls, contest):
        result = []
        if contest.extra_title1 is not None:
            result.append(contest.extra_title1)
            if contest.extra_title2 is not None:
                result.append(contest.extra_title2)
                if contest.extra_title3 is not None:
                    result.append(contest.extra_title3)
                    if contest.extra_title4 is not None:
                        result.append(contest.extra_title4)
        return result

    @classmethod
    def setTitle(cls, contest, index, title):
        pass

    @classmethod
    def getGroupTitle(cls, contest):
        result = []
        if contest.extra_group_title1 is not None:
            result.append(contest.extra_group_title1)
            if contest.extra_group_title2 is not None:
                result.append(contest.extra_group_title2)
                if contest.extra_group_title3 is not None:
                    result.append(contest.extra_group_title3)
                    if contest.extra_group_title4 is not None:
                        result.append(contest.extra_gourp_title4)
        return result

    @classmethod
    def setGroupTitle(cls, contest, index, group_title):
        pass

class ContestPlayerUtil:
    @classmethod
    def getInfo(cls, cp_obj, index):
        pass

    @classmethod
    def setInfo(cls, cp_obj, index, info):
        pass

class ContestGroupUtil:
    @classmethod
    def getMember(cls, leader_id, contest_id):
        result = []
        group = ContestGroup.objects.filter(leader_id=leader_id, contest_id=contest_id)
        member = CCPUser.objects.get(id=leader_id)
        result.append({
            'userId': leader_id,
            'username': member.username,
            'email': member.email
        })
        index = 0
        while index < MAX_MEMBER - 1:
            member_id = getattr(group, 'member' + str(index+1) + '_id')
            if member_id is None:
                break
            member = CCPUser.objects.get(id=member_id)
            result.append({
                'userId': member_id,
                'username': member.username,
                'email': member.email
            })
        return result

    @classmethod
    def setMember(cls, cg_obj, index, member):
        pass

    @classmethod
    def getInfo(cls, cg_obj, index):
        pass

    @classmethod
    def setInfo(cls, cg_obj, index, info):
        pass

class ContestGradeUtil:
    @classmethod
    def getGrade(cls, leader_id, contest_id):
        result = []
        index = 0
        while index < MAX_PHASE:
            objects = ContestGrade.objects.filter(leader_id=leader_id, contest_id=contest_id, phase=index+1)
            total_grade = 0
            phase_judges = 0
            if objects.count() == 0:
                break
            for obj in objects:
                if obj.grade == -1:  # 还未打分
                    break
                total_grade = total_grade + obj.grade
                phase_judges = phase_judges + 1
            phase_grade = total_grade / phase_judges
            result.append(phase_grade)
            index = index + 1
        return result
