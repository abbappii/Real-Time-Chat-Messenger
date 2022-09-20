
from django.urls import path 

from .views import register_view, login_user, logout_user

urlpatterns = [ 
    path('register/', register_view, name='register'),
    path('login/',login_user,name='login'),
    path('logout/', logout_user,name='logout'),
]