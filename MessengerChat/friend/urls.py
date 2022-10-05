from django.urls import path

from friend.views import send_friend_request

urlpatterns = [ 
    path('send-frnd-req/', send_friend_request, name='send_frnd_req'),
    
]