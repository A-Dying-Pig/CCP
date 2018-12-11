from django.urls import path
from Backend import api_user as user
from Backend import api_competition as competition
from Backend import api_superadmin as superadmin
from Backend import api_admin as admin
from Backend import api_judge as judge
from Backend import api_message as message

urlpatterns = [
    path('user/register', user.register),
    path('user/login', user.login),
    path('user/check', user.check),
    path('user/profile', user.profile),
    path('user/modify', user.modify),
    path('competition/create', competition.create),
    path('competition/neededinfo', competition.neededinfo),
    path('competition/enroll', competition.enroll),
    path('competition/slider', competition.slider),
    path('competition/hot', competition.hot),
    path('competition/detail', competition.detail),
    path('competition/list', competition.list),
    path('super/contests', superadmin.contests),
    path('super/detail', superadmin.detail),
    path('super/submit', superadmin.submit),
    path('admin/participants', admin.participants),
    path('admin/detail', admin.detail),
    path('admin/modify', admin.modify),
    path('admin/setjudge', admin.setjudge),
    path('admin/upload', admin.upload),
    path('admin/broadcast', admin.broadcast),
    path('admin/judgeprogress', admin.judgeprogress),
    path('admin/zone', admin.zone),
    path('admin/advanced', admin.advanced),
    path('admin/setadvanced', admin.setadvanced),
    path('admin/judgelist', admin.judgelist),
    path('judge/getone', judge.getone),
    path('judge/submit', judge.submit),
    path('judge/finished', judge.finished),
    path('message/getnew', message.getnew),
    path('message/getall', message.getall),
    path('message/detail', message.detail),
]
