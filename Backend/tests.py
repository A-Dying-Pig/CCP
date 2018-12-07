
from django.test import TestCase
from .models import *
# Django的单元测试基于unittest库
class StudentTestCase(TestCase):
    # 测试函数执行前执行
    def setUp(self):
        print("======in setUp")
    # 需要测试的内容
    def test_add(self):
        student = CCPUser(username='aaa',email='120862596@qq.com',password='123456')
        student.save()
        Contest.objects.create(title='title', category='category', enroll_start='2018-12-10T16:00:00.000Z', enroll_end='2018-12-18T16:00:00.000Z',
                               information='hahaha', brief_introduction='brief',admin_id=1,host1='htx',organizers='\n')
        self.assertEqual(student.username, 'aaa')
        # 需要测试的内容
    def test_check_exit(self):
        self.assertEqual(0, CCPUser.objects.count())
        # 测试函数执行后执行
    def tearDown(self):
        print("======in tearDown")
