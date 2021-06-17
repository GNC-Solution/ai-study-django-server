from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

active_roles = (
    ("manager", "manager"),
    ("partner", "partner"),
    ("user", "user"),
)

class profile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=active_roles, default="user")
    double_pwd = models.CharField(max_length=6, default='123456')
    verify_type = models.CharField(max_length=10, default='1')
    user_type = models.CharField(max_length=20, default='STUDENT')
    balance_amt = models.IntegerField(default=0)
    point_amt = models.IntegerField(default=0)
    profile_img = models.ImageField(default="human.png", null=True, blank=True, upload_to='static/profiles')
    profile_url = models.CharField(db_column='profile_url', null=True, max_length=1024, default='')
    qrcode_img = models.ImageField(default="qr_user.png", null=True, blank=True, upload_to='static/qrcode')
    qrcode_url = models.CharField(db_column='qrcode_url', null=True, max_length=1024, default='')
    usage_flag = models.CharField(max_length=10, default='1')
    logaction = models.CharField(max_length=20, default='')
    logstatus = models.CharField(max_length=10, default='0')
    logtime = models.DateTimeField(db_column='logtime', )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
