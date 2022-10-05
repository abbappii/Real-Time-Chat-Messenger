from curses.ascii import HT
from telnetlib import DO
from django.shortcuts import render, HttpResponse
import json
from account.models import Account
from friend.models import FriendRequests, FriendList
# Create your views here.

def send_friend_request(request,*args, **kwargs):
    user = request.user
    payload = {}

    if request.method == 'POST' and  user.is_authenticated:
        receiver_user_id = request.POST.get('receiver_user_id')

        if receiver_user_id:
            receiver = Account.objects.get(id = receiver_user_id)

            try:
                friend_requests = FriendRequests.objects.filter(sender=user,receiver=receiver)

                # if any of them are active 
                try:
                    for friend in friend_requests:
                        if friend.is_active == True:
                            raise Exception("You already sent a friend request.")
                    # if none are active then create a new frnd req 
                    friend_request = FriendRequests(sender=user, receiver=receiver)
                    friend_request.save()
                    payload['response']="Friend request sent."

                except Exception as e:
                    payload['response']=str(e)

            except FriendRequests.DoesNotExist:
                friend_request = FriendRequests(sender=user,receiver=receiver)
                friend_request.save()
                payload['response']="Friend request sent."

            if payload['response'] == None:
                payload['response'] = "Something went wrong"

        else:
            payload['response'] = "Unable to send a friend request."

    

    else:
        payload['response'] = "You are not authenticated user."
    return HttpResponse(json.dumps(payload), content_type="application/json")
                     