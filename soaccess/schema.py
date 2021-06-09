import graphene
from graphene import ObjectType, String, Field, Int, List, InputObjectType
from graphene_file_upload.scalars import Upload
from graphene_django.types import DjangoObjectType

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage, send_mail
from django.core.files.storage import FileSystemStorage
from django.db.models import Count, Sum, Q

from django.conf import settings

from souser.models import profile
from soaccess.models import SOStudyuser, SORoom

from validate_email import validate_email

# from django.core.files.storage import FileSystemStorage

import json
import os
import random
from datetime import datetime

import threading
import qrcode

import bitcoin.main as btc

class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()

# class FilesType(DjangoObjectType):
#     class Meta:
#         model = Files

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"

class ProfileType(DjangoObjectType):
    class Meta:
        model = profile
        fields = "__all__"

class Response(graphene.ObjectType):
    success = graphene.Boolean(required=True)
    message = graphene.String()

class UserResponse(graphene.ObjectType):
    success = graphene.Boolean(required=True)
    message = graphene.String()
    user = graphene.Field(UserType)

class ProfileResponse(graphene.ObjectType):
    success = graphene.Boolean(required=True)
    message = graphene.String()
    user = graphene.Field(ProfileType)

class SOUserQuery(graphene.ObjectType):
    user_check = graphene.Field(UserResponse, username=graphene.String(required=True), userpwd=graphene.String(required=True))

    def resolve_user_check(self, info, username, userpwd):

        user_response = {}

        success = True
        user = None

        username = username.strip()
        userpwd = userpwd.strip()

        try:
            if User.objects.filter(username=username).exists():
                message = '정상입니다.'
            else:
                message = '아이디가 존재하지 않습니다.'
                success = False

        except Exception as identifier:
            message = '아이디 읽기 오류입니다.'
            success = False

        if success:
            user = User.objects.get(username=username)

            if user.is_active == False:
                message = '인증되지 않은 사용자입니다.'
                success = False

            if not user.check_password(userpwd):
                message = '비밀번호가 일치하지 않습니다.'
                success = False

        user_response["user"] = user
        user_response["success"] = success
        user_response["message"] = message

        return user_response


class WriteLog(graphene.Mutation):
    Output = Response

    class Arguments:
        roomno = graphene.String()
        username = graphene.String()
        existflag = graphene.String()

    def mutate(self, info, roomno, username, existflag):
        response_info = {}
        message = "로그 기록..."
        success = True

        if User.objects.filter(username=username).exists():
            studylog = SOStudyuser.objects.create(roomno=roomno,
                                                  username=username,
                                                  existflag=existflag,
                                                  logtime=datetime.now()
                                                  )

        else:
            message = "사용자 없음..."
            success = False

        response_info["success"] = success
        response_info["message"] = message

        return response_info


class WriteStudy(graphene.Mutation):
    Output = Response

    class Arguments:
        roomno = graphene.String()
        action = graphene.String()

    def mutate(self, info, roomno, action):
        response_info = {}
        message = "로그 기록..."
        success = True

        userid = info.context.user.id
        print(userid)
        if userid:
            username = info.context.user.username

            if SORoom.objects.filter(roomno=roomno).exists():

                if action == 'start':
                    existflag = 'Y'
                if action == 'stop':
                    existflag = 'N'
                if action == 'empty':
                    existflag = 'N'
                else:
                    existflag = 'N'

                studylog = SOStudyuser.objects.create(roomno=roomno,
                                                      username=username,
                                                      action=action,
                                                      existflag=existflag,
                                                      logtime=datetime.now()
                                                      )

            else:
                message = "방이 없습니다."
                success = False

        else:
            message = "로그인 안되어 있습니다."
            success = False

        response_info["success"] = success
        response_info["message"] = message

        return response_info


class CreateRoom(graphene.Mutation):
    Output = Response

    class Arguments:
        roomno = graphene.String()
        roomtitle = graphene.String()

    def mutate(self, info, roomno, roomtitle):
        response_info = {}
        message = "방 생성..."
        success = True

        userid = info.context.user.id
        print(userid)

        if userid:
            username = info.context.user.username

            soroom = SORoom.objects.create(roomno=roomno,
                                           room_title=roomtitle,
                                           username=username,
                                           active_flag='1',
                                           member_cnt=0,
                                           createdat=datetime.now()
                                           )

        else:
            message = "사용자 없음..."
            success = False

        response_info["success"] = success
        response_info["message"] = message

        return response_info