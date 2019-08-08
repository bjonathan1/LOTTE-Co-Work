import random
from django.shortcuts import render
from . import tasks


def index(request):
    context = {}
    return render(request, 'demoapp/index.html', context)

def dashboard(request):
    context = {}
    return render(request, 'demoapp/dashboard.html', context)
