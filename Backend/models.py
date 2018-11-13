from django.db import models
from django.contrib.auth.models import AbstractUser


# 用户信息总表
class CCPUser(AbstractUser):
    gender = models.BooleanField()  # 性别
    birthday = models.DateTimeField(blank=True, null=True)  # 生日
    introduction = models.CharField(max_length=64, blank=True, null=True)  # 个人简介


# 比赛信息总表
class Contest(models.Model):
    title = models.CharField(max_length=32)  # 比赛名称
    category = models.CharField(max_length=32)  # 比赛类别
    grouped = models.BooleanField(default=False)  # 是否需要组队参赛
    start_time = models.DateTimeField()  # 比赛开始时间
    end_time = models.DateTimeField()  # 比赛结束时间
    enroll_start = models.DateTimeField()  # 报名开始时间
    enroll_end = models.DateTimeField()  # 报名结束时间
    information = models.TextField()  # 比赛详情
    phase = models.CharField(max_length=512, blank=True)  # 比赛阶段
    phase_start_time = models.CharField(max_length=512, blank=True)  # 各阶段开始时间
    phase_end_time = models.CharField(max_length=512, blank=True)  # 各阶段结束时间
    phase_information = models.TextField(blank=True)  # 比赛阶段详情
    admin_id = models.IntegerField()  # 比赛管理员User表里的id
    host = models.CharField(max_length=32)  # 主办方
    organizers = models.CharField(max_length=255)  # 承办方
    extra_title = models.CharField(max_length=255, blank=True, null=True)  # 每个比赛特需的选手数据的标题


# 记录选手和比赛的对应关系
class ContestPlayer(models.Model):
    player_id = models.IntegerField(db_index=True)  # 选手id
    contest_id = models.IntegerField(db_index=True)  # 比赛id
    extra_information = models.CharField(max_length=512, blank=True, null=True)  # 每个比赛特需的选手数据


# 记录比赛和小组的对应关系，目前小组成员上限为5名，设组长1名
class ContestGroup(models.Model):
    leader_id = models.IntegerField(db_index=True)  # 组长id
    member1_id = models.IntegerField(db_index=True, null=True)
    member2_id = models.IntegerField(db_index=True, null=True)
    member3_id = models.IntegerField(db_index=True, null=True)
    member4_id = models.IntegerField(db_index=True, null=True)
    contest_id = models.IntegerField(db_index=True)  # 比赛id


# 记录比赛和评委的对应关系
class ContestJudge(models.Model):
    judge_id = models.IntegerField(db_index=True)  # 评委id
    contest_id = models.IntegerField(db_index=True)  # 比赛id


# 记录小组和比赛评委、评分的对应关系
class ContestGrade(models.Model):
    leader_id = models.IntegerField(db_index=True)  # 组长id
    contest_id = models.IntegerField(db_index=True)  # 比赛id
    judge_id = models.IntegerField(default=-1, db_index=True)  # 评委id
    grade = models.IntegerField(default=-1)  # 选手(小组)由当前评委打出的成绩




