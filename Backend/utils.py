# 一些辅助函数
from .models import *
import time
import os
import traceback

MAX_HOSTS = 4  # 最大主办方人数
MAX_PHASE = 5
MAX_EXTRA = 4
MAX_MEMBER = 5
MAX_CONTEST_ONE_PAGE = 10
MAX_PARTICIPANT_ONE_PAGE = 10
MAX_POST_ONE_PAGE = 8
MAX_REPLY_ONE_PAGE = 8

RESOURCE_BASE_DIR = 'D:/CCP'

class ContestUtil:
    NON_REGION = 0
    BIG_REGION = 1
    PROVINCE_REGION = 2
    @classmethod
    def getStage(cls, contest):
        result = []
        for i in range(0, 5):
            if getattr(contest, 'phase_name'+str(i+1)) is not None:
                tmp_dict = {}
                tmp_dict['name'] = getattr(contest, 'phase_name'+str(i+1))
                tmp_dict['details'] = getattr(contest, 'phase_information'+str(i+1))

                tmp_dict['stageTimeBegin'] = (time.mktime(getattr(contest, 'phase_start_time' + str(i+1)).timetuple()) + 8 * 60 * 60) * 1000
                tmp_dict['handTimeEnd'] = (time.mktime(getattr(contest, 'phase_hand_end_time'+str(i+1)).timetuple()) + 8 * 60 * 60) * 1000
                tmp_dict['evaluationTimeEnd'] = (time.mktime(getattr(contest, 'phase_evaluate_end_time' + str(i+1)).timetuple()) + 8 * 60 * 60) * 1000
                tmp_dict['mode'] = getattr(contest, 'phase_mode' + str(i+1))
                tmp_dict['zone'] = getattr(contest, 'phase_region_mode' + str(i+1))
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
                        result.append(contest.extra_group_title4)
        return result

    @classmethod
    def setGroupTitle(cls, contest, index, group_title):
        pass

    @classmethod
    def getCurrentPhase(cls, contestid):
        # return current phase and status
        # phase 0 is the enroll stage
        # phase 1 is the first stage, 0 is submission, 1 is judging
        contest = Contest.objects.get(id=contestid)
        enroll_start = time.mktime(contest.enroll_start.timetuple()) + 8 * 60 * 60
        enroll_end = time.mktime(contest.enroll_end.timetuple()) + 8 * 60 * 60
        cur_time = time.time()
        if cur_time < enroll_start:
            return {'phase': -1}
        if enroll_start < cur_time < enroll_end:
            return {'phase': 0}
        for i in range(1, 6):
            if i != MAX_PHASE and getattr(contest, 'phase_name' + str(i+1)) is not None:
                pre_start = getattr(contest, 'phase_start_time' + str(i))
                pre_sub = getattr(contest, 'phase_hand_end_time' + str(i))
                pre_judge = getattr(contest, 'phase_evaluate_end_time' + str(i))
                cur_start = getattr(contest, 'phase_start_time' + str(i+1))
                if time.mktime(pre_start.timetuple()) + 8 * 60 * 60 < cur_time < time.mktime(cur_start.timetuple()) + 8 * 60 * 60:
                    if cur_time < time.mktime(pre_sub.timetuple()) + 8 * 60 * 60:
                        return {'phase': i, 'status': 0}
                    elif cur_time < time.mktime(pre_judge.timetuple()) + 8 * 60 * 60:
                        return {'phase': i, 'status': 1}
                    else:
                        return {'phase': i, 'status': 2}
            else:  # i阶段已经是最后一个阶段
                sub_time = getattr(contest, 'phase_hand_end_time' + str(i))
                judge_time = getattr(contest, 'phase_evaluate_end_time' + str(i))
                if cur_time < time.mktime(sub_time.timetuple()) + 8 * 60 * 60:
                    return {'phase': i, 'status': 0}
                elif cur_time < time.mktime(judge_time.timetuple()) + 8 * 60 * 60:
                    return {'phase': i, 'status': 1}
                else:
                    return {'phase': i, 'status': 2}

    @classmethod
    def getCurrentRegionMode(cls, contestid):
        # todo
        # return current Regionmode 0, 1, 2
        try:
            cur_phase = cls.getCurrentPhase(contestid)
            contest = Contest.objects.get(id=contestid)
            phase = cur_phase['phase']
            if phase == 0:
                phase = 1
            mode = getattr(contest, 'phase_region_mode'+str(phase))
            if mode is None:
                return -1
            else:
                return mode
        except Exception as e:
            traceback.print_exc()
            return -1


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
    def addMember(cls, cg_obj, member):
        # add a member to group(member is id)
        pass

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
            if phase_judges == 0:
                result.append(0)
            else:
                phase_grade = total_grade / phase_judges
                result.append(phase_grade)
            index = index + 1
        return result


class GeneralUtil:
    @classmethod
    def getChildren(cls, basedir):  # api/judge/getone接口遍历得到文件夹结构的递归函数
        targets = os.listdir(basedir)
        result = []
        for file_name in targets:
            full_path = os.path.join(basedir, file_name)
            if os.path.isdir(full_path):  # 文件夹
                children = cls.getChildren(full_path)
                result.append({
                    'title': file_name,
                    'isLeaf': False,
                    'children': children
                })
            elif os.path.isfile(full_path):  # 文件
                result.append({
                    'title': file_name,
                    'isLeaf': True,
                    'data': {'src': full_path[len(RESOURCE_BASE_DIR):]}
                })
        return result

    @classmethod
    def del_dir(cls, path):
        if os.path.isdir(path):
            for file in os.listdir(path):
                full_path = path + file
                if os.path.isfile(full_path):
                    os.remove(full_path)
                elif os.path.isdir(full_path):
                    cls.del_dir(full_path)
                    os.rmdir(full_path)
