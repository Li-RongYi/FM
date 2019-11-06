from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^add_cart/(?P<goods_id>[\w\-]+)', views.add_cart, name='add_cart'),
    url(r'^clear_cart', views.clear_cart, name='clear_cart'),
    url(r'^delete_cart/(?P<cart_id>[\w\-]+)', views.delete_cart, name='delete_cart'),
    url(r'^checkout/(?P<cart_id>[\w\-]+)', views.checkout, name='checkout'),
]
