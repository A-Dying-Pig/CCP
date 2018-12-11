from django.db import models
from django.contrib.auth.models import AbstractUser

# 用户信息总表
class CCPUser(AbstractUser):
    birthday = models.DateTimeField(blank=True, null=True)  # 生日
    introduction = models.CharField(max_length=64, blank=True, null=True)  # 个人简介
    university = models.CharField(max_length=64, null=True)
    province = models.CharField(max_length=32, null=True)
    city = models.CharField(max_length=32, null=True)
    class Meta:
        db_table = "CCPUser"

# 比赛信息总表
class Contest(models.Model):
    title = models.CharField(max_length=32)  # 比赛名称
    category = models.CharField(max_length=32)  # 比赛类别
    grouped = models.BooleanField(default=False)  # 是否需要组队参赛
    group_min_number = models.IntegerField(blank=True, null=True)  # 组队最小人数
    group_max_number = models.IntegerField(blank=True, null=True)  # 组队最大人数
    # start_time = models.DateTimeField()  # 比赛开始时间
    # end_time = models.DateTimeField()  # 比赛结束时间
    enroll_start = models.DateTimeField()  # 报名开始时间
    enroll_end = models.DateTimeField()  # 报名结束时间
    information = models.TextField()  # 比赛详情
    brief_introduction = models.CharField(max_length=128)  # 比赛简介
    # phase = models.CharField(max_length=512, blank=True)  # 比赛阶段
    # phase_start_time = models.CharField(max_length=512, blank=True, null=True)  # 各阶段开始时间
    phase_name1 = models.CharField(max_length=32, blank=True, null=True)  # 各阶段名称
    phase_name2 = models.CharField(max_length=32, blank=True, null=True)
    phase_name3 = models.CharField(max_length=32, blank=True, null=True)
    phase_name4 = models.CharField(max_length=32, blank=True, null=True)
    phase_name5 = models.CharField(max_length=32, blank=True, null=True)
    phase_start_time1 = models.DateTimeField(blank=True, null=True)  # 每个阶段的开始时间
    phase_start_time2 = models.DateTimeField(blank=True, null=True)
    phase_start_time3 = models.DateTimeField(blank=True, null=True)
    phase_start_time4 = models.DateTimeField(blank=True, null=True)
    phase_start_time5 = models.DateTimeField(blank=True, null=True)
    phase_hand_end_time1 = models.DateTimeField(blank=True, null=True)  # 每个阶段选手上交作品截止时间
    phase_hand_end_time2 = models.DateTimeField(blank=True, null=True)
    phase_hand_end_time3 = models.DateTimeField(blank=True, null=True)
    phase_hand_end_time4 = models.DateTimeField(blank=True, null=True)
    phase_hand_end_time5 = models.DateTimeField(blank=True, null=True)
    phase_evaluate_end_time1 = models.DateTimeField(blank=True, null=True)  # 每个阶段评测截止时间
    phase_evaluate_end_time2 = models.DateTimeField(blank=True, null=True)
    phase_evaluate_end_time3 = models.DateTimeField(blank=True, null=True)
    phase_evaluate_end_time4 = models.DateTimeField(blank=True, null=True)
    phase_evaluate_end_time5 = models.DateTimeField(blank=True, null=True)
    phase_information1 = models.CharField(max_length=128, blank=True, null=True)  # 每个比赛阶段的详情
    phase_information2 = models.CharField(max_length=128, blank=True, null=True)
    phase_information3 = models.CharField(max_length=128, blank=True, null=True)
    phase_information4 = models.CharField(max_length=128, blank=True, null=True)
    phase_information5 = models.CharField(max_length=128, blank=True, null=True)
    phase_mode1 = models.CharField(max_length=16, blank=True, null=True)  # 各阶段评测方式
    phase_mode2 = models.CharField(max_length=16, blank=True, null=True)
    phase_mode3 = models.CharField(max_length=16, blank=True, null=True)
    phase_mode4 = models.CharField(max_length=16, blank=True, null=True)
    phase_mode5 = models.CharField(max_length=16, blank=True, null=True)
    phase_region_mode1 = models.IntegerField(default=0)  # 各阶段划分赛区的方式
    phase_region_mode2 = models.IntegerField(default=0)
    phase_region_mode3 = models.IntegerField(default=0)
    phase_region_mode4 = models.IntegerField(default=0)
    phase_region_mode5 = models.IntegerField(default=0)
    admin_id = models.IntegerField()  # 比赛管理员User表里的id
    host1 = models.CharField(max_length=32)  # 主办方
    host2 = models.CharField(max_length=32, blank=True, null=True)
    host3 = models.CharField(max_length=32, blank=True, null=True)
    host4 = models.CharField(max_length=32, blank=True, null=True)
    organizers = models.CharField(max_length=255)  # 承办方
    extra_title1 = models.CharField(max_length=32, blank=True, null=True)  # 每个比赛特需的选手数据的标题
    extra_title2 = models.CharField(max_length=32, blank=True, null=True)
    extra_title3 = models.CharField(max_length=32, blank=True, null=True)
    extra_title4 = models.CharField(max_length=32, blank=True, null=True)
    extra_group_title1 = models.CharField(max_length=32, blank=True, null=True)  # 额外组队信息
    extra_group_title2 = models.CharField(max_length=32, blank=True, null=True)
    extra_group_title3 = models.CharField(max_length=32, blank=True, null=True)
    extra_group_title4 = models.CharField(max_length=32, blank=True, null=True)
    checked = models.IntegerField(default=-1)  # 是否已经审核过，-1表示管理员未审核，0表示审核未通过，1表示审核通过
    class Meta:
        db_table = "Contest"

# 记录选手和比赛的对应关系
# 选手报名时填
class ContestPlayer(models.Model):
    player_id = models.IntegerField(db_index=True)  # 选手id
    contest_id = models.IntegerField(db_index=True)  # 比赛id
    phase_region1 = models.CharField(max_length=32, blank=True, null=True)  # 选手在每个阶段的赛区
    phase_region2 = models.CharField(max_length=32, blank=True, null=True)
    phase_region3 = models.CharField(max_length=32, blank=True, null=True)
    phase_region4 = models.CharField(max_length=32, blank=True, null=True)
    phase_region5 = models.CharField(max_length=32, blank=True, null=True)
    extra_information1 = models.CharField(max_length=64, blank=True, null=True)  # 每个比赛特需的选手数据
    extra_information2 = models.CharField(max_length=64, blank=True, null=True)
    extra_information3 = models.CharField(max_length=64, blank=True, null=True)
    extra_information4 = models.CharField(max_length=64, blank=True, null=True)
    class Meta:
        db_table = "ContestPlayer"

# 记录比赛和小组的对应关系，目前小组成员上限为5名，设组长1名
# 选手成组报名时填
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
    class Meta:
        db_table = "ContestGroup"

# 记录比赛和评委的对应关系
# 这张表在主办方分添加评委的时候用到
# 现在可能使用Group来控制，每个比赛有一个评委组？
class ContestJudge(models.Model):
    judge_id = models.IntegerField(db_index=True)  # 评委id
    contest_id = models.IntegerField(db_index=True)  # 比赛id
    phase_region1 = models.CharField(max_length=32, blank=True, null=True)
    phase_region2 = models.CharField(max_length=32, blank=True, null=True)
    phase_region3 = models.CharField(max_length=32, blank=True, null=True)
    phase_region4 = models.CharField(max_length=32, blank=True, null=True)
    phase_region5 = models.CharField(max_length=32, blank=True, null=True)
    class Meta:
        db_table = "ContestJudge"

# 记录小组和比赛评委、评分的对应关系
# 这张表在提交作品的时候填组长（选手）id和比赛id和比赛阶段三个字段，评委分配算法中填评委id字段，评委评分过程中填成绩字段
class ContestGrade(models.Model):
    leader_id = models.IntegerField(db_index=True)  # 组长id
    contest_id = models.IntegerField(db_index=True)  # 比赛id
    phase = models.IntegerField(blank=True, null=True)  # 比赛阶段
    judge_id = models.IntegerField(default=-1, db_index=True)  # 评委id
    grade = models.IntegerField(default=-1)  # 选手(小组)由当前评委打出的该阶段比赛的成绩
    class Meta:
        db_table = "ContestGrade"

# 消息列表
class Notification(models.Model):
    context = models.CharField(max_length=2048)  # 消息体
    title = models.CharField(max_length=64)  # 消息标题
    time = models.DateTimeField(null=True)  # 消息发送时间
    class Meta:
        db_table = "Notification"

# 记录消息和接受消息的用户的对应关系
class NotificationUser(models.Model):
    notification_id = models.IntegerField(db_index=True)  # 消息id
    user_id = models.IntegerField(db_index=True)  # 接受消息的用户id
    read = models.BooleanField(default=False)  # 消息已读/未读
    class Meta:
        db_table = "NotificationUser"

# 轮播图
class Slider(models.Model):
    contest_id = models.IntegerField()  # 比赛id
    title = models.CharField(max_length=32)  # 比赛名称


# 热门比赛
class HotContest(models.Model):
    contest_id = models.IntegerField()  # 比赛id
    title = models.CharField(max_length=32)  # 比赛名称
