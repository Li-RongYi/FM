from django.db import models
from user.models import UserProfile


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Goods(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, blank=True)
    trade_location = models.CharField(max_length=32)
    price = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    picture_url = models.CharField(max_length=128, blank=True)
    picture = models.ImageField(upload_to='goods', blank=True, null=True)
    seller = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE)
    discount = models.IntegerField(default=0, blank=True)
    goods_phone = models.CharField(max_length=20,null=True)
    goods_qq = models.CharField(max_length=15,null=True)
    publish_time = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    goods = models.ForeignKey(Goods, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=256)
    #comment_time = models.DateField(auto_now_add=True)
    comment_time = models.DateTimeField(auto_now_add=True)
    rate = models.PositiveSmallIntegerField(default=5)


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


class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(default=1)
    sum = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.sum