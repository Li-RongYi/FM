from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^goods/(?P<goods_id>[\w\-]+)', views.goods_page, name='goods'),
    url(r'^add_comment/(?P<goods_id>[\w\-]+)', views.add_comment, name='add_comment'),

    url(r'^mygoods', views.mygoods, name='mygoods'),
    url(r'^publish_goods', views.publish_goods, name='publish_goods'),
    url(r'^edit_goods/(?P<goods_id>[\w\-]+)', views.edit_goods, name='edit_goods'),
    url(r'^delete_goods/(?P<goods_id>[\w\-]+)', views.delete_goods, name='delete_goods'),

    url(r'^mysale', views.mysale, name='mysale'),
    url(r'^completesale', views.completesale, name='completesale'),

    url(r'^check_goods', views.check_goods, name='check_goods'),
    url(r'^check/(?P<goods_id>[\w\-]+)', views.check, name='check'),
]
