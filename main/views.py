from django.shortcuts import render
from django.http import HttpResponse
from .models import Owl
from django.shortcuts import render

# Create your views here.


def index(request):
    context=dict()
    return render(request,'main/index.html',context)


def uploads(request):
    context = dict()
    return render(request, 'main/upload.html', context)
