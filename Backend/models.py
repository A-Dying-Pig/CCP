from django.db import models
from django.contrib.auth.models import AbstractUser


class CCPUser(AbstractUser):
    # id = models.AutoField(primary_key=True)
    email = models.EmailField()
    gender = models.BooleanField()
    birthday = models.DateTimeField(blank=True)
    introduction = models.CharField(max_length=50, blank=True)


class Contest(models.Model):
    title = models.CharField(max_length=20)
    status = models.IntegerField()  # to be extended
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    enroll_start = models.DateTimeField()
    enroll_end = models.DateTimeField()
    information = models.TextField()
    organiser1_id = models.IntegerField()  # User表里的id
    extra_title = models.CharField(max_length=255)  # 每个比赛特需的选手数据的标题


    # organiser = models.ForeignKey(User, on_delete=models.PROTECT)


class Relation(models.Model):
    competitor_id = models.IntegerField(db_index=True)
    contest_id = models.IntegerField(db_index=True)
    judge_id = models.IntegerField(default=-1, db_index=True)
    grade = models.IntegerField(default=-1)
    extra_information = models.CharField(max_length=511, blank=True)  # 每个比赛特需的选手数据


class ContestJudge(models.Model):
    judge_id = models.IntegerField(db_index=True)
    contest_id = models.IntegerField(db_index=True)



