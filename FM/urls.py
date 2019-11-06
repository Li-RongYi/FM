# login_sys/urls.py

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^', include('user.urls')),
                  url(r'^', include('goods.urls')),
                  url(r'^', include('cart.urls')),
                  url(r'^', include('order.urls')),
                  url(r'^', include('index.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
