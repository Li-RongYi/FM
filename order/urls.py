from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^myorder', views.myorder, name='myorder'),
    url(r'^completeorder', views.completeorder, name='completeorder'),
    url(r'^check_order/(?P<order_id>[\w\-]+)', views.check_order, name='check_order'),
    url(r'^delete_order/(?P<order_id>[\w\-]+)', views.delete_order, name='delete_order'),
]
