from django.db import models
from user.models import UserProfile
from goods.models import Goods


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, blank=True, null=True, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    num = models.PositiveIntegerField(default=1)
    sum = models.FloatField(default=0)
