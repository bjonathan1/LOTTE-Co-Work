from . import tasks
from django.shortcuts import render



def index(request):
    context = {}
    return render(request, 'index.html', context)

def dashboard(request):
    context = {}
    return render(request, 'dashboard.html', context)
