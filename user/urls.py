from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^register_info/$', views.register_info, name='register_info'),
    url(r'^$', views.user_login, name='login'),
    url(r'login^$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^login_code/$', views.login_code, name='login_code'),
    url(r'^login_face/$', views.login_face, name='login_face'),
    url(r'^forgetpassword/', views.forgetpassword, name='forgetpassword'),
    url(r'^forgetpassword2/', views.forgetpassword2, name='forgetpassword2'),
    url(r'^profile/', views.profilechange, name='profilechange'),
    url(r'^faceprofile/', views.faceprofile, name='faceprofile'),
    url(r'^passwordchange/', views.passwordchange, name='passwordchange'),
    url(r'^accountcancellation/', views.accountcancellation, name='accountcancellation'),
]
