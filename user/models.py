from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    height = models.PositiveIntegerField(default="30", blank=True, null=True, editable=False)
    width = models.PositiveIntegerField(default="30", blank=True, null=True, editable=False)
    image = models.ImageField(upload_to='profile', height_field='height', width_field='width', blank=True)

    def __str__(self):
        return self.username


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, default='靓仔')
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    height = models.PositiveIntegerField(default="30", blank=True, null=True, editable=False)
    width = models.PositiveIntegerField(default="30", blank=True, null=True, editable=False)
    avatar = models.ImageField(upload_to='profile', height_field='height', width_field='width')
    contact = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.user.username


class ConfirmString(models.Model):
    code = models.CharField(max_length=6)
    email = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
