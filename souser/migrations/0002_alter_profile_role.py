# Generated by Django 3.2.3 on 2021-06-03 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('souser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('manager', 'manager'), ('partner', 'partner'), ('user', 'user')], default='user', max_length=20),
        ),
    ]
