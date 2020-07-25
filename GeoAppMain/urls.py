from django.urls import path, include
from .views import *

urlpatterns = [
    path('', hello, name='hello_page'),
    path('get_coord/', Coordinate.as_view(), name='coordinate'),
    path('user/<str:string_id>/', UserController.check_request_method, name='user_url'),
    path('user/login/', UserLogin.as_view(), name='login_url'),
    path('user/reset_pass/<str:string_id>/', UserResetPassword.as_view(), name='reset_pass_url'),  # GET
    path('user/action/<str:string_id>/', UserAction.as_view(), name='user_action_url'),
    # path('user/fav_mark/<str:string_id>/', FavMarkController.check_request_method, name='fav_mark_url'),
    path('user/mark/<str:string_id>/', MarkController.check_request_method, name='mark_url')
]
