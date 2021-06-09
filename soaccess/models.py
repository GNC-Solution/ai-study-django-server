from django.db import models
from django.contrib.auth.models import User


class SOStudyuser(models.Model):
    roomno = models.CharField(db_column='roomno', max_length=255)
    username = models.CharField(db_column='username', max_length=255)
    existflag = models.CharField(db_column='existflag', max_length=10)
    action = models.CharField(db_column='action', max_length=20)
    logtime = models.DateTimeField(db_column='logtime', )

    class Meta:
        managed = False
        db_table = 'sosyudylog'

class SORoom(models.Model):
    roomno = models.CharField(db_column='roomno', max_length=255)
    room_title = models.CharField(db_column='room_title', max_length=255)
    username = models.CharField(db_column='username', max_length=255)
    active_flag = models.CharField(db_column='active_flag', max_length=10)
    member_cnt = models.IntegerField(db_column='member_cnt', default=0)
    username = models.CharField(db_column='username', max_length=255)
    createdat = models.DateTimeField(db_column='createdat', )
    closedat = models.DateTimeField(db_column='closedat', )

    class Meta:
        managed = False
        db_table = 'soroom'