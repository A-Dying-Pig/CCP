from django.urls import path
from Backend import api_user as user
from Backend import api_competition as competition

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
    path('competition/getonepro', competition.getonepro),
]
