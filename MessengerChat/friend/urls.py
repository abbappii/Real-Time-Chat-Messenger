from django.urls import path

from friend.views import send_friend_request, friend_requests, accept_friend_request

urlpatterns = [ 
    path('send-frnd-req/', send_friend_request, name='send_frnd_req'),
    path('frined-request/<int:id>/', friend_requests, name='friend_request'),
    path('accept-friend-request/<friend_request_id>/',accept_friend_request, name='accept_friend_request'),
        
]