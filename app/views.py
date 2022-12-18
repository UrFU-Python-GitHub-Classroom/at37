from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from .models import *

def index(request):
    data = {
        'profession': Profession.objects.get(id=1)
    }
    return render(request, 'app/index.html', context=data)

def info(request):
    data = {
        'info': Statistic.objects.get(id=1)
    }
    return render(request, 'app/info.html', context=data)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')