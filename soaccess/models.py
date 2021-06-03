from django.db import models
from django.contrib.auth.models import User


class SOStudyuser(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    roomno = models.CharField(db_column='roomno', max_length=255)
    username = models.CharField(db_column='username', max_length=255)
    existflag = models.CharField(db_column='existflag', max_length=10)
    logtime = models.DateTimeField(db_column='logtime', )

    class Meta:
        managed = False
        db_table = 'sosyudylog'
