from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class CustomUser(AbstractUser):
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    is_blocked = models.BooleanField(default=False)
    f_name = models.CharField(max_length=100, null=True)
    s_name = models.CharField(max_length=100, null=True)
    phone_no = models.CharField(max_length=12, null=True)
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referral_code_used = models.BooleanField(default=False)
    bonus = models.IntegerField(null=True, blank=True, default=100)


'USERNAME_FIELD' == 'username'
