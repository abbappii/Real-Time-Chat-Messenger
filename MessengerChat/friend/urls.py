from django.urls import path

from friend.views import send_friend_request, friend_requests

urlpatterns = [ 
    path('send-frnd-req/', send_friend_request, name='send_frnd_req'),
    path('frined-request/<int:id>/', friend_requests, name='friend_request'),
        
]