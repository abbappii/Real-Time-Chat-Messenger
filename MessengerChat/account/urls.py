
from django.urls import path 
from django.contrib.auth import views as auth_views

from .views import (
    register_view, 
    login_user, 
    logout_user,
    account_view,
    account_search_view,
)

urlpatterns = [ 
    path('register/', register_view, name='register'),
    # path('account/<user_id>/',account_view,name='account'),
    path('account/<int:id>/',account_view,name='account'),
    path('search/', account_search_view,name='search'),

    path('login/',login_user,name='login'),
    path('logout/', logout_user,name='logout'),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
     name='password_reset_complete'),
]