from django.urls import path
from . import views

urlpatterns = [
    path('userlog', views.userlog, name='userlog'),
]
