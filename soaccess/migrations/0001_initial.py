# Generated by Django 3.2.3 on 2021-06-18 07:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SORoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomno', models.CharField(db_column='roomno', max_length=255)),
                ('room_title', models.CharField(db_column='room_title', max_length=255)),
                ('active_flag', models.CharField(db_column='active_flag', max_length=10)),
                ('delete_flag', models.CharField(db_column='delete_flag', max_length=10)),
                ('member_cnt', models.IntegerField(db_column='member_cnt', default=0)),
                ('username', models.CharField(db_column='username', max_length=255)),
                ('createdat', models.DateTimeField(db_column='createdat')),
                ('closedat', models.DateTimeField(db_column='closedat')),
            ],
            options={
                'db_table': 'soroom',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SOStudylog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomid', models.IntegerField(db_column='roomid', default=0)),
                ('roomno', models.CharField(db_column='roomno', max_length=255)),
                ('username', models.CharField(db_column='username', max_length=255)),
                ('existflag', models.CharField(db_column='existflag', max_length=10)),
                ('action', models.CharField(db_column='action', max_length=20)),
                ('logtime', models.DateTimeField(db_column='logtime', default=datetime.datetime(2021, 6, 18, 16, 10, 20, 223606))),
            ],
            options={
                'db_table': 'sosyudylog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SOUserDaily',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(db_column='user_id', default=0)),
                ('username', models.CharField(db_column='username', max_length=255)),
                ('yyyymmdd', models.CharField(db_column='yyyymmdd', max_length=8)),
                ('total_study', models.IntegerField(db_column='total_study', default=0)),
                ('total_pause', models.IntegerField(db_column='total_pause', default=0)),
                ('phone_cnt', models.IntegerField(db_column='phone_cnt', default=0)),
                ('pause_cnt', models.IntegerField(db_column='pause_cnt', default=0)),
            ],
            options={
                'db_table': 'souserdaily',
                'managed': False,
            },
        ),
    ]
