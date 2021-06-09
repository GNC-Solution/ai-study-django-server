from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from .models import SOStudyuser

def userlog(request):
    context = {}
    if not request.user.is_authenticated:
        print('Not logged in...')
        context["rsLog"] = None

    else:
        print('Log read...')
        username = request.user.username

        rsLog = SOStudyuser.objects.filter(username=username).order_by('-logtime')[:100]
        context["rsLog"] = rsLog

    return render(request, "userlog.html", context)
