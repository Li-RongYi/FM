from django.db import models
from user.models import UserProfile
from goods.models import Goods


# Create your models here.
class Order(models.Model):
    seller = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(UserProfile, blank=True, null=True, on_delete=models.CASCADE, related_name='buyer')
    goods = models.ForeignKey(Goods, blank=True, null=True, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(default=1)
    sum = models.FloatField(default=0)
    contact = models.CharField(max_length=20, null=True)
    message = models.CharField(max_length=512, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.message
