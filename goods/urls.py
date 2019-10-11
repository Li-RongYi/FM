from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^goods/(?P<goods_id>[\w\-]+)', views.goods_page, name='goods'),
    url(r'^add_comment/(?P<goods_id>[\w\-]+)', views.add_comment, name='add_comment'),
    url(r'^add_cart/(?P<goods_id>[\w\-]+)', views.add_cart, name='add_cart'),
    url(r'^clear_cart', views.clear_cart, name='clear_cart'),
    url(r'^delete_cart/(?P<cart_id>[\w\-]+)', views.delete_cart, name='delete_cart'),
    url(r'^mygoods', views.mygoods, name='mygoods'),
    url(r'^publish_goods', views.publish_goods, name='publish_goods'),
    url(r'^edit_goods/(?P<goods_id>[\w\-]+)', views.edit_goods, name='edit_goods'),
    url(r'^delete_goods/(?P<goods_id>[\w\-]+)', views.delete_goods, name='delete_goods'),
    # url(r'^add_cart/(?P<goods_id>[\w\-]+)', views.add_cart, name='add_cart'),
    # url(r'^add_cart/(?P<goods_id>[\w\-]+)', views.add_cart, name='add_cart'),
    # url(r'^category/(?P<category_id>[\w\-]+)', views.category, name='category'),
    # url(r'^add_goods', views.add_goods, name='add_goods'),
    # url(r'^profile/(?P<user_id>[\w\-]+)', views.profile, name='profile'),
    # url(r'^search', views.search, name='search'),
    # url(r'^message/', views.display_message, name='message'),
]
