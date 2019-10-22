from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^index_category/(?P<category_id>[\w\-]+)', views.index_category, name='index_category'),
    url(r'^about/$', views.about, name='about'),
    url(r'^categories/', views.categories, name='categories'),

    url(r'^goods/(?P<goods_id>[\w\-]+)', views.goods_page, name='goods'),
    url(r'^add_comment/(?P<goods_id>[\w\-]+)', views.add_comment, name='add_comment'),

    url(r'^cart/$', views.cart, name='cart'),
    url(r'^add_cart/(?P<goods_id>[\w\-]+)', views.add_cart, name='add_cart'),
    url(r'^clear_cart', views.clear_cart, name='clear_cart'),
    url(r'^delete_cart/(?P<cart_id>[\w\-]+)', views.delete_cart, name='delete_cart'),

    url(r'^mygoods', views.mygoods, name='mygoods'),
    url(r'^publish_goods', views.publish_goods, name='publish_goods'),
    url(r'^edit_goods/(?P<goods_id>[\w\-]+)', views.edit_goods, name='edit_goods'),
    url(r'^delete_goods/(?P<goods_id>[\w\-]+)', views.delete_goods, name='delete_goods'),
    url(r'^mysale', views.mysale, name='mysale'),
    url(r'^completesale', views.completesale, name='completesale'),
    url(r'^checkout/(?P<cart_id>[\w\-]+)', views.checkout, name='checkout'),

    url(r'^myorder', views.myorder, name='myorder'),
    url(r'^completeorder', views.completeorder, name='completeorder'),
    url(r'^check_order/(?P<order_id>[\w\-]+)', views.check_order, name='check_order'),
    url(r'^delete_order/(?P<order_id>[\w\-]+)', views.delete_order, name='delete_order'),
]
