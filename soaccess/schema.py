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
from soaccess.models import SOStudylog, SORoom, SOUserDaily, SOUserchat

from validate_email import validate_email

# from django.core.files.storage import FileSystemStorage

import json
import os
import random
from datetime import datetime, timezone

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
                message = '???????????????.'
            else:
                message = '???????????? ???????????? ????????????.'
                success = False

        except Exception as identifier:
            message = '????????? ?????? ???????????????.'
            success = False

        if success:
            user = User.objects.get(username=username)

            if user.is_active == False:
                message = '???????????? ?????? ??????????????????.'
                success = False

            if not user.check_password(userpwd):
                message = '??????????????? ???????????? ????????????.'
                success = False

        user_response["user"] = user
        user_response["success"] = success
        user_response["message"] = message

        return user_response


    def resolve_room_list(self, info):

        userid = info.context.user.id

        response_info = {}
        success = True
        message = "????????? ??????"
        rooms = None

        try:
            rooms = SORoom.objects.filter(delete_flag='0')
            print(len(rooms))

        except Exception as identifier:
            success = False
            message = '????????? ?????? ???????????????.'

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
            message = "?????? ????????? ??????"
            daily = None

            try:
                daily = SOUserDaily.objects.filter(username=username)

            except Exception as identifier:
                success = False
                message = '?????? ????????? ?????? ???????????????.'

        else:
            message = "???????????? ????????????."
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
#         message = "?????? ??????..."
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
#             message = "????????? ??????..."
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
        message = "?????? ??????..."
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

                nowtime = datetime.now(timezone.utc)
                yyyymmdd = nowtime.strftime("%Y%m%d")

                studylog = SOStudylog.objects.create(roomid=roomid,
                                                      username=username,
                                                      action=action,
                                                      existflag=existflag,
                                                      logtime=datetime.now()
                                                      )

                if SOUserchat.objects.filter(user_id=userid).exists():
                    rsChat = SOUserchat.objects.get(user_id=userid)
                else:
                    rsChat = SOUserchat.objects.create(user_id=userid,
                                                       username=username,
                                                       yyyymmdd=yyyymmdd,
                                                       logaction=action,
                                                       logstatus='0',
                                                       userlogtime=nowtime,
                                                       starttime=nowtime
                                                       )

                userlogtime = rsChat.userlogtime
                logstatus = rsChat.logstatus

                if action == 'start':
                    print('start... create yyyymmdd')
                    rsChat.yyyymmdd = yyyymmdd

                else:
                    yyyymmdd = rsChat.yyyymmdd


                if SOUserDaily.objects.filter(user_id=userid, yyyymmdd=yyyymmdd).exists():
                    rsDaily = SOUserDaily.objects.get(user_id=userid, yyyymmdd=yyyymmdd)
                else:
                    rsDaily = SOUserDaily.objects.create(user_id=userid,
                                                         username=username,
                                                         yyyymmdd=yyyymmdd,
                                                         total_study=0,
                                                         total_pause=0,
                                                         phone_cnt=0,
                                                         pause_cnt=0
                                                         )

                totaltime = nowtime - userlogtime
                totalsec = totaltime.total_seconds()

                if totalsec < 0:
                    totalsec = 0

                p_studytime = 0
                p_pausetime = 0
                p_pausecnt = 0
                p_status = '0'
                if action == 'start':
                    p_studytime = 0
                    p_pausetime = 0
                    p_status = '1'
                elif action == 'stop':
                    p_studytime = totalsec
                    p_pausetime = 0
                    p_status = '0'
                elif action == 'pause':
                    p_studytime = totalsec
                    p_pausetime = 0
                    p_pausecnt = 1
                    p_status = '1'
                elif action == 'resume':
                    p_studytime = 0
                    p_pausetime = totalsec
                    p_status = '0'
                else:
                    action = 'invalid'

                print(p_studytime)
                print(p_pausetime)
                print(p_pausecnt)

                rsDaily.total_study = rsDaily.total_study + p_studytime
                rsDaily.total_pause = rsDaily.total_pause + p_pausetime
                rsDaily.pause_cnt = rsDaily.pause_cnt + p_pausecnt
                rsDaily.save()

                rsChat.userlogtime = nowtime
                rsChat.logaction = action
                rsChat.logstatus = logstatus
                rsChat.save()

                # dbCon = pymysql.connect(host=MYDB_HOST,
                #                         user=MYDB_USER,
                #                         password=MYDB_PWD,
                #                         database=MYDB_NAME,
                #                         charset='utf8'
                #                         )

                # cursor = dbCon.cursor()
                # strsql = f"CALL p_souserdaily_calculate ('{userid}','{action}') "

                # ==> ???????????? ?????????
                # cursor.execute(strsql)
                # results = cursor.fetchone()

                # ==> ????????? ?????? ??????
                # csr.execute(strsql)
                
                # print(results)
                # cursor.close()
                # dbCon.close()
                                
                # userprofile = profile.objects.get(user_id=userid)
                # userprofile.logtime = datetime.now()
                # userprofile.logaction = action
                # userprofile.save()

            else:
                message = "?????? ????????????."
                success = False

        else:
            message = "???????????? ????????????."
            success = False

        response_info["success"] = success
        response_info["message"] = message

        return response_info


class UsePhone(graphene.Mutation):
    Output = Response

    class Arguments:
        username = graphene.String()

    def mutate(self, info, username):
        response_info = {}
        message = "????????? ??????..."
        success = True

        if User.objects.filter(username=username).exists():
            rsuser = User.objects.get(username=username)
            userid = rsuser.id

            nowtime = datetime.now(timezone.utc)
            yyyymmdd = nowtime.strftime("%Y%m%d")

            if SOUserDaily.objects.filter(user_id=userid, yyyymmdd=yyyymmdd).exists():
                rsDaily = SOUserDaily.objects.get(user_id=userid, yyyymmdd=yyyymmdd)
            else:
                rsDaily = SOUserDaily.objects.create(user_id=userid,
                                                     username=username,
                                                     yyyymmdd=yyyymmdd,
                                                     total_study=0,
                                                     total_pause=0,
                                                     phone_cnt=0,
                                                     pause_cnt=0
                                                     )

            rsDaily.phone_cnt = rsDaily.phone_cnt + 1
            rsDaily.save()

        else:
            message = "???????????? ????????????."
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
        message = "??? ??????..."
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
            message = "????????? ??????..."
            success = False

        response_info["success"] = success
        response_info["message"] = message
        response_info["room"] = soroom

        return response_info