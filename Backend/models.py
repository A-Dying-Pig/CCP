from django.db import models
from django.contrib.auth.models import AbstractUser


# 用户信息总表
class CCPUser(AbstractUser):
    birthday = models.DateTimeField(blank=True, null=True)  # 生日
    introduction = models.CharField(max_length=64, blank=True, null=True)  # 个人简介
    university = models.CharField(max_length=64, null=True)
    province = models.CharField(max_length=32, null=True)
    city = models.CharField(max_length=32, null=True)

# 比赛信息总表
class Contest(models.Model):
    title = models.CharField(max_length=32)  # 比赛名称
    category = models.CharField(max_length=32)  # 比赛类别
    grouped = models.BooleanField(default=False)  # 是否需要组队参赛
    group_min_number = models.IntegerField(blank=True, null=True)  # 组队最小人数
    group_max_number = models.IntegerField(blank=True, null=True)  # 组队最大人数
    start_time = models.DateTimeField()  # 比赛开始时间
    end_time = models.DateTimeField()  # 比赛结束时间
    enroll_start = models.DateTimeField()  # 报名开始时间
    enroll_end = models.DateTimeField()  # 报名结束时间
    information = models.TextField()  # 比赛详情
    brief_introduction = models.CharField(max_length=128)  # 比赛简介
    phase = models.CharField(max_length=512, blank=True)  # 比赛阶段
    # phase_start_time = models.CharField(max_length=512, blank=True, null=True)  # 各阶段开始时间
    phase_end_time1 = models.DateTimeField(blank=True, null=True)  # 阶段一结束时间
    phase_end_time2 = models.DateTimeField(blank=True, null=True)
    phase_end_time3 = models.DateTimeField(blank=True, null=True)
    phase_end_time4 = models.DateTimeField(blank=True, null=True)
    phase_end_time5 = models.DateTimeField(blank=True, null=True)
    phase_information1 = models.CharField(max_length=128, blank=True, null=True)  # 比赛阶段一详情
    phase_information2 = models.CharField(max_length=128, blank=True, null=True)
    phase_information3 = models.CharField(max_length=128, blank=True, null=True)
    phase_information4 = models.CharField(max_length=128, blank=True, null=True)
    phase_information5 = models.CharField(max_length=128, blank=True, null=True)
    admin_id = models.IntegerField()  # 比赛管理员User表里的id
    host1 = models.CharField(max_length=32)  # 主办方
    host2 = models.CharField(max_length=32)
    host3 = models.CharField(max_length=32)
    host4 = models.CharField(max_length=32)
    organizers = models.CharField(max_length=255)  # 承办方
    extra_title1 = models.CharField(max_length=32, blank=True, null=True)  # 每个比赛特需的选手数据的标题
    extra_title2 = models.CharField(max_length=32, blank=True, null=True)
    extra_title3 = models.CharField(max_length=32, blank=True, null=True)
    extra_title4 = models.CharField(max_length=32, blank=True, null=True)
    extra_group_title1 = models.CharField(max_length=32, blank=True, null=True)  # 额外组队信息
    extra_group_title2 = models.CharField(max_length=32, blank=True, null=True)
    extra_group_title3 = models.CharField(max_length=32, blank=True, null=True)
    extra_group_title4 = models.CharField(max_length=32, blank=True, null=True)

# 记录选手和比赛的对应关系
class ContestPlayer(models.Model):
    player_id = models.IntegerField(db_index=True)  # 选手id
    contest_id = models.IntegerField(db_index=True)  # 比赛id
    extra_information1 = models.CharField(max_length=64, blank=True, null=True)  # 每个比赛特需的选手数据
    extra_information2 = models.CharField(max_length=64, blank=True, null=True)
    extra_information3 = models.CharField(max_length=64, blank=True, null=True)
    extra_information4 = models.CharField(max_length=64, blank=True, null=True)

# 记录比赛和小组的对应关系，目前小组成员上限为5名，设组长1名
# 现在使用Group来控制？
class ContestGroup(models.Model):
    leader_id = models.IntegerField(db_index=True)  # 组长id
    member1_id = models.IntegerField(db_index=True, null=True)
    member2_id = models.IntegerField(db_index=True, null=True)
    member3_id = models.IntegerField(db_index=True, null=True)
    member4_id = models.IntegerField(db_index=True, null=True)
    contest_id = models.IntegerField(db_index=True)  # 比赛id
    group_name = models.CharField(max_length=32)  # 组名
    extra_information1 = models.CharField(max_length=64, blank=True, null=True)  # 每个比赛特需的组队数据
    extra_information2 = models.CharField(max_length=64, blank=True, null=True)
    extra_information3 = models.CharField(max_length=64, blank=True, null=True)
    extra_information4 = models.CharField(max_length=64, blank=True, null=True)

# 记录比赛和评委的对应关系
# 现在可能使用Group来控制，每个比赛有一个评委组？
class ContestJudge(models.Model):
    judge_id = models.IntegerField(db_index=True)  # 评委id
    contest_id = models.IntegerField(db_index=True)  # 比赛id


# 记录小组和比赛评委、评分的对应关系
class ContestGrade(models.Model):
    leader_id = models.IntegerField(db_index=True)  # 组长id
    contest_id = models.IntegerField(db_index=True)  # 比赛id
    phase = models.IntegerField(blank=True, null=True)  # 比赛阶段
    judge_id = models.IntegerField(default=-1, db_index=True)  # 评委id
    grade = models.IntegerField(default=-1)  # 选手(小组)由当前评委打出的该阶段比赛的成绩


# 消息列表
class Notification(models.Model):
    context = models.CharField(max_length=1024)  # 消息体


# 记录消息和接受消息的用户的对应关系
class NotificationUser(models.Model):
    notification_id = models.IntegerField(db_index=True)  # 消息id
    user_id = models.IntegerField(db_index=True)  # 接受消息的用户id
    read = models.BooleanField(default=False)  # 消息已读/未读
    time = models.DateTimeField()  # 消息发送时间
