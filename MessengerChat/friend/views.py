
from django.dispatch import receiver
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse

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
    
    body_unicode = request.body.decode('utf-8')
    receiver_user_id = json.loads(body_unicode)['id']
    print(type(receiver_user_id))
    print(receiver_user_id)
 
    if request.method == 'POST' and  user.is_authenticated:
        print('rec_id',receiver_user_id)

        if receiver_user_id:
            receiver = Account.objects.get(id = receiver_user_id)

            try:
                friend_requests = FriendRequests.objects.filter(sender=user,receiver=receiver)

                # if any of them are active 
                try:
                    for friend in friend_requests:
                        if friend.is_active:
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
    # return HttpResponse(json.dumps(payload), content_type="application/json")
    return JsonResponse(payload)



def accept_friend_request(request, *args, **kwargs):
    context = {}

    user = request.user
    if request.method == 'GET' and user.is_authenticated:
        friend_request_id = kwargs.get('friend_request_id')
        if friend_request_id:
            friend_request = FriendRequests.objects.get(id=friend_request_id)
            if friend_request.receiver == user:
                if friend_request:
                    friend_request.accept()
                    context['response'] = "Friend request accepted."
                else:
                    context['response'] = "something went wrong."
            else:
                context['response'] = "That is not your request to accept."
        else:
            context['response'] = "Unable to accept the request."
    else:
        context['response'] = "You must authenticate to accept a friend request."
    
    return JsonResponse(context)

    # return HttpResponse(request,json.dumps(context), content_type='application/json')

def remove_friend(request, *args, **kwargs):

    user = request.user 
    payload = {}
    if request.method =="POST" and user.is_authenticated:
        body_unicode = request.body.decode('utf-8')
        user_id = json.loads(body_unicode)['remove_id']
        # user_id = request.POST.get('id') remove_id
        print("user id: ",user_id)

        if user_id:
            try:
                removee = Account.objects.get(pk=user_id)
                friend_list = FriendList.objects.get(user=user)
                friend_list.unfrined(removee)
                payload['response'] = "Successfully removed that friend."
            except Exception as e:
                payload['response'] = f"Something went wrond: {str(e)}."
        else:
            payload['response'] = "There was an error. Unable to remove that friend."
    else:
        payload['response'] = "You must be authenticated to remove a friend."

    
    return JsonResponse(payload)
    # return HttpResponse(request, json.dumps(payload))


# decline friend request after sending request someone 
def decline_friend_request(request,*args, **kwargs):
    user = request.user
    context = {}

    if request.method == "GET" and user.is_authenticated:
        friend_request_id  = kwargs.get('friend_request_id')

        if friend_request_id:
            friend_request = FriendRequests.objects.get(pk=friend_request_id)

            if friend_request.receiver == user:
                if friend_request:
                    friend_request.decline()
                    context['response'] = "Friend req decline successfully."
                else:
                    context['response'] = "Something went wrong."
            else:
                context['response'] = "That is not your friend request to decline"

        else:
             context['response'] = "Unable to decline friend request."

    else:
        context['response'] = "You must authenticated to decline a friend request."

    return JsonResponse(context)
    # return HttpResponse(request, json.dumps(context), content_type="application/json")

