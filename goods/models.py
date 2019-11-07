from django.db import models
from user.models import UserProfile
from index.models import Category

# Create your models here.



class Goods(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, blank=True)
    trade_location = models.CharField(max_length=32)
    price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='goods', blank=True, null=True)
    seller = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE)
    contact = models.CharField(max_length=20, null=True)
    publish_time = models.DateField(auto_now_add=True, null=True, blank=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Comment(models.Model):
    goods = models.ForeignKey(Goods, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    comment_time = models.DateTimeField(auto_now_add=True)
    rate = models.PositiveSmallIntegerField(default=5, null=True)

    def __str__(self):
        return self.content


class InstationMessage(models.Model):
    receiver = models.ForeignKey(UserProfile, related_name='receiver_id', on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, related_name='sender_id', on_delete=models.CASCADE)
    content = models.CharField(max_length=140)
    send_time = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.content
