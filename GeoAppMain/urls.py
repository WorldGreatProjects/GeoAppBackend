from django.urls import path, include
from .views import *

urlpatterns = [
    path('', hello, name='hello_page'),
    path('get_coord/', Coordinate.as_view(), name='coordinate'),
    path('user/', UserController.check_request_method, name='user')
]
