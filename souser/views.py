from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from soaccess.models import SOStudyuser, SORoom

def home(request):
    context = {}

    rsRoom = SORoom.objects.filter(active_flag='1')
    context['rsRoom'] = rsRoom

    return render(request, "home.html", context)


@csrf_exempt
def sologincheck(request):
    context = {}

    uname = request.POST['username']
    upwd = request.POST['userpwd']

    user = authenticate(username=uname, password=upwd)
    if user is not None:
        login(request, user)
        print("login success...")

    else:
        print("login failed...")

    return redirect('/')
