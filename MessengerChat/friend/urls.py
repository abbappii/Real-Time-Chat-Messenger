from django.urls import path

from friend.views import (
    send_friend_request, 
    friend_requests, 
    accept_friend_request,
    remove_friend,
    decline_friend_request,
    cancel_friend_request,
    friends_list_view
)

urlpatterns = [ 
    path('friend-list/<user_id>/',friends_list_view,name="friend_list"),
    path('send-frnd-req/', send_friend_request, name='send_frnd_req'),
    path('frined-request/user_id/', friend_requests, name='friend_request'),
    path('accept-friend-request/<friend_request_id>/',accept_friend_request, name='accept_friend_request'),
    path('remove-friend/', remove_friend, name='remove_friend'),
    path('decline-frined-request/<friend_request_id>/', decline_friend_request, name='decline_friend_request'),
    path('cancel-friend-request/',cancel_friend_request, name='cancel_friend_request'),

]