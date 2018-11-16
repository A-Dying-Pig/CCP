from django.urls import path
from Backend import views

urlpatterns = [
    path('competition/create', views.createContest, name='createContest'),
    path('IndexSlider', views.indexSlider, name='indexSlider'),
    path('IndexHotCompetition', views.indexHotCompetition, name='indexHotCompetition'),
    path('CheckUser', views.checkUser, name='checkUser'),
    path('GetNeededInfo', views.getNeededInfo, name='getNeededInfo'),
    path('PersonCenter', views.personCenter, name='peronCenter'),
    path('SetPerson', views.setPerson, name='setPerson'),
    path('competition/getonepro', views.getOnePro, name='getOnePro'),
]
