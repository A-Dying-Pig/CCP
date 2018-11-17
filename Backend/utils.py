# 一些辅助函数
from .models import *

class ContestUtil:
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
    def getHost(cls, contest, index):
        pass

    @classmethod
    def setHost(cls, contest, index, host):
        pass

    @classmethod
    def getTitle(cls, contest, index):
        pass

    @classmethod
    def setTitle(cls, contest, index, title):
        pass

    @classmethod
    def getGroupTitle(cls, contest, index):
        pass

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
