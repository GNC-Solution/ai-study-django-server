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

import pymysql

from souser.models import profile
from soaccess.models import SOStudylog, SORoom, SOUserDaily

from validate_email import validate_email

# from django.core.files.storage import FileSystemStorage

import json
import os
import random
from datetime import datetime

import threading
import qrcode

import bitcoin.main as btc

MYDB = getattr(settings, "DATABASES", None)
MYDB_NAME = MYDB["default"]["NAME"]
MYDB_USER = MYDB["default"]["USER"]
MYDB_PWD = MYDB["default"]["PASSWORD"]
MYDB_HOST = MYDB["default"]["HOST"]

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

class RoomType(DjangoObjectType):
    class Meta:
        model = SORoom
        fields = "__all__"

class DailyType(DjangoObjectType):
    class Meta:
        model = SOUserDaily
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

class RoomResponse(graphene.ObjectType):
    success = graphene.Boolean(required=True)
    message = graphene.String()
    room = graphene.Field(RoomType)

class RoomsResponse(graphene.ObjectType):
    success = graphene.Boolean(required=True)
    message = graphene.String(required=True)
    rooms = graphene.List(RoomType)

class DailyResponse(graphene.ObjectType):
    success = graphene.Boolean(required=True)
    message = graphene.String(required=True)
    daily = graphene.List(DailyType)

class SOUserQuery(graphene.ObjectType):
    user_check = graphene.Field(UserResponse, username=graphene.String(required=True), userpwd=graphene.String(required=True))
    room_list = graphene.Field(RoomsResponse)
    daily_list = graphene.Field(DailyResponse, username=graphene.String(required=True))

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


    def resolve_room_list(self, info):

        userid = info.context.user.id

        response_info = {}
        success = True
        message = "채팅방 읽기"
        rooms = None

        try:
            rooms = SORoom.objects.filter(delete_flag='0')
            print(len(rooms))

        except Exception as identifier:
            success = False
            message = '채팅방 읽기 오류입니다.'

        response_info["success"] = success
        response_info["message"] = message
        response_info["rooms"] = rooms

        return response_info


    def resolve_daily_list(self, info, username):

        if User.objects.filter(username=username).exists():
            rsuser = User.objects.get(username=username)
            userid = rsuser.id

            response_info = {}
            success = True
            message = "일별 학습도 읽기"
            daily = None

            try:
                daily = SOUserDaily.objects.filter(username=username)

            except Exception as identifier:
                success = False
                message = '일별 학습도 읽기 오류입니다.'

        else:
            message = "사용자가 없습니다."
            success = False
            daily = None

        response_info["success"] = success
        response_info["message"] = message
        response_info["daily"] = daily

        return response_info


# class WriteLog(graphene.Mutation):
#     Output = Response
#
#     class Arguments:
#         roomno = graphene.String()
#         username = graphene.String()
#         existflag = graphene.String()
#
#     def mutate(self, info, roomno, username, existflag):
#         response_info = {}
#         message = "로그 기록..."
#         success = True
#
#         if User.objects.filter(username=username).exists():
#             studylog = SOStudylog.objects.create(roomno=roomno,
#                                                   username=username,
#                                                   existflag=existflag,
#                                                   logtime=datetime.now()
#                                                   )
#
#         else:
#             message = "사용자 없음..."
#             success = False
#
#         response_info["success"] = success
#         response_info["message"] = message
#
#         return response_info


class WriteStudy(graphene.Mutation):
    Output = Response

    class Arguments:
        username = graphene.String()
        roomid = graphene.String()
        action = graphene.String()

    def mutate(self, info, username, roomid, action):
        response_info = {}
        message = "로그 기록..."
        success = True

        if User.objects.filter(username=username).exists():
            rsuser = User.objects.get(username=username)
            userid = rsuser.id

            if SORoom.objects.filter(id=roomid).exists():

                if action == 'start':
                    existflag = 'Y'
                elif action == 'stop':
                    existflag = 'N'
                elif action == 'empty':
                    existflag = 'N'
                else:
                    existflag = 'N'

                studylog = SOStudylog.objects.create(roomid=roomid,
                                                      username=username,
                                                      action=action,
                                                      existflag=existflag,
                                                      logtime=datetime.now()
                                                      )

                # Table 있는지 읽어본다
                strsql = f"CALL p_souserdaily_calculate ('{userid}','{action}') "
                print(strsql)

                dbCon = pymysql.connect(host=MYDB_HOST,
                                        user=MYDB_USER,
                                        password=MYDB_PWD,
                                        database=MYDB_NAME,
                                        charset='utf8'
                                        )

                cursor = dbCon.cursor()
                cursor.execute(strsql)
                results = cursor.fetchone()
                cursor.close()

                userprofile = profile.objects.get(user_id=userid)
                userprofile.logtime = datetime.now()
                userprofile.logaction = action
                userprofile.save()

            else:
                message = "방이 없습니다."
                success = False

        else:
            message = "사용자가 없습니다."
            success = False

        response_info["success"] = success
        response_info["message"] = message

        return response_info


class CreateRoom(graphene.Mutation):
    Output = RoomResponse

    class Arguments:
        roomtitle = graphene.String()

    def mutate(self, info, roomtitle):
        response_info = {}
        message = "방 생성..."
        success = True

        userid = info.context.user.id
        print(userid)

        soroom = None
        if userid:
            username = info.context.user.username

            soroom = SORoom.objects.create(roomno='',
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
        response_info["room"] = soroom

        return response_info