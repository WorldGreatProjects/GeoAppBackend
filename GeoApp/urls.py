

from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirection),
    path('geo_app_main/', include('GeoAppMain.urls'))
]
