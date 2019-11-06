from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^index_category/(?P<category_id>[\w\-]+)', views.index_category, name='index_category'),
    url(r'^about/$', views.about, name='about'),
    url(r'^categories/', views.categories, name='categories'),
]
