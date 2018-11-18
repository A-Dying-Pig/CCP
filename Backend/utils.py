# 一些辅助函数
from .models import *

MAX_HOSTS = 4  # 最大主办方人数
MAX_PHASE = 5
MAX_EXTRA = 4
MAX_MEMBER = 5
MAX_CONTEST_ONE_PAGE = 10

class ContestUtil:
    @classmethod
    def getStage(cls, contest):
        result = []
        for i in range(0,5):
            if getattr(contest, 'phase_name'+str(i+1)) is not None:
                tmp_dict = {}
                tmp_dict['name'] = getattr(contest, 'phase_name'+str(i+1))
                tmp_dict['details'] = getattr(contest, 'phase_information'+str(i+1))
                tmp_dict['handTimeEnd'] = getattr(contest, 'phase_hand_end_time'+str(i+1))
                tmp_dict['evaluationTimeEnd'] = getattr(contest, 'phase_evaluate_end_time'+str(i+1))
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
    def getMember(cls, cg_obj, index):
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
