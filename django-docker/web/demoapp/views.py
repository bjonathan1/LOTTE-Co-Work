from . import tasks
from django.shortcuts import render



def index(request):
    context = {}
    return render(request, 'demoapp/index.html', context)

def dashboard(request):
    context = {}
    return render(request, 'demoapp/dashboard.html', context)

def meeting(request):
    context = {}
    return render(request, 'demoapp/meeting.html', context)
