from django.urls import path
from . import views

app_name = 'demoapp'

urlpatterns = [
    path('main/', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('meeting/', views.meeting, name='meeting'),
    path('issue/', views.issue, name='issue'),
    path('drive/', views.drive, name='drive'),
    path('timeline/', views.timeline, name='timeline'),
    path('', views.login, name='login'),
]
