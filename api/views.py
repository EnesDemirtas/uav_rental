from django.shortcuts import render
from rest_framework.decorators import api_view

from uavs.models import UAV


@api_view(['GET'])
def register(request):
    return render(request, 'register.html')


@api_view(['GET'])
def login(request):
    return render(request, 'login.html')


@api_view(['GET'])
def home(request):
    uavs = UAV.objects.all()
    return render(request, 'home.html', context={
        'uavs': uavs
    })
