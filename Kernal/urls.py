
from django.urls import path, include, re_path
from django.contrib import admin
import Foreend.views
import Files.views

urlpatterns = [
    path(r'', Foreend.views.index),
    path(r'index', Foreend.views.index),
    path(r'login', Foreend.views.login),
    path(r'register', Foreend.views.register),
    path(r'logout', Foreend.views.logout),
    path(r'contest', Foreend.views.contest),
    path(r'detail', Foreend.views.detail),
    path(r'enroll', Foreend.views.enroll),
    path(r'profile', Foreend.views.profile),
    path(r'addContest', Foreend.views.addContest),
    path(r'api/', include('Backend.urls')),
    path(r'superadmin', Foreend.views.superadmin),
    re_path(r'^resources/', Files.views.download),
]
