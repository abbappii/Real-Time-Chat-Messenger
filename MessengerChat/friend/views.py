
from django.dispatch import receiver
from django.shortcuts import render, HttpResponse, redirect
import json
from account.models import Account
from friend.models import FriendRequests, FriendList
# Create your views here.

def friend_requests(request,id):
    context = {}

    user = request.user
    if user.is_authenticated:
        account = Account.objects.get(pk=id)
        if user == account:
            friend_requests = FriendRequests.objects.filter(receiver=account, is_active=True)
            context['friend_requests'] = friend_requests
        else:
            return HttpResponse("You cant't view another persons friend requests.")

    else:
        redirect("login")

    return render(request,'friend/friend_requests.html',context)
    
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
                     