from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Goods)
admin.site.register(models.Category)
admin.site.register(models.Comment)
admin.site.register(models.InstationMessage)
