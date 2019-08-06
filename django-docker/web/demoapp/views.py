from django.shortcuts import render
from . import tasks


def index(request):
    context = {}
    return render(request, 'demoapp/index.html', context)
