from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

class SOStudylog(models.Model):
    roomid = models.IntegerField(db_column='roomid', default=0)
    roomno = models.CharField(db_column='roomno', max_length=255)
    username = models.CharField(db_column='username', max_length=255)
    existflag = models.CharField(db_column='existflag', max_length=10)
    action = models.CharField(db_column='action', max_length=20)
    logtime = models.DateTimeField(db_column='logtime', default=datetime.now())

    class Meta:
        managed = False
        db_table = 'sosyudylog'

class SORoom(models.Model):
    roomno = models.CharField(db_column='roomno', max_length=255)
    room_title = models.CharField(db_column='room_title', max_length=255)
    username = models.CharField(db_column='username', max_length=255)
    active_flag = models.CharField(db_column='active_flag', max_length=10)
    delete_flag = models.CharField(db_column='delete_flag', max_length=10)
    member_cnt = models.IntegerField(db_column='member_cnt', default=0)
    username = models.CharField(db_column='username', max_length=255)
    createdat = models.DateTimeField(db_column='createdat', )
    closedat = models.DateTimeField(db_column='closedat', )

    class Meta:
        managed = False
        db_table = 'soroom'


class SOUserDaily(models.Model):
    user_id = models.IntegerField(db_column='user_id', default=0)
    username = models.CharField(db_column='username', max_length=255)
    yyyymmdd = models.CharField(db_column='yyyymmdd', max_length=8)
    total_study = models.IntegerField(db_column='total_study', default=0)
    total_pause = models.IntegerField(db_column='total_pause', default=0)
    phone_cnt = models.IntegerField(db_column='phone_cnt', default=0)
    pause_cnt = models.IntegerField(db_column='pause_cnt', default=0)

    class Meta:
        managed = False
        db_table = 'souserdaily'