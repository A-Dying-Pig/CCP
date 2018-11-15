
from django.urls import path, include
from django.contrib import admin
import Foreend

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    path(r'/', Foreend.views.index),
    path(r'login/', Foreend.views.login),
    path(r'register/', Foreend.views.register),
    path(r'logout/', Foreend.views.logout),
    path(r'contests/', Foreend.views.contest),
    path(r'detail/', Foreend.views.detail),
    path(r'enroll/', Foreend.views.enroll),
    path(r'profile/', Foreend.views.profile),
    path(r'api/', include('Backend.urls')),
]
