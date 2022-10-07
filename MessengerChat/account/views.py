# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib.auth import login, authenticate, logout
# from django.conf import settings

# from django.core.files.storage import default_storage
# from django.core.files.storage import FileSystemStorage
# import os
# import cv2
# import json
# import base64
# import requests
# from django.core import files


# from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
# from account.models import Account


# TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"

# # This is basically almost exactly the same as friends/friend_list_view
# def account_search_view(request, *args, **kwargs):
# 	context = {}
# 	if request.method == "GET":
# 		search_query = request.GET.get("q")
# 		if len(search_query) > 0:
# 			search_results = Account.objects.filter(email__icontains=search_query).filter(username__icontains=search_query).distinct()
# 			user = request.user
# 			accounts = [] # [(account1, True), (account2, False), ...]
# 			for account in search_results:
# 				accounts.append((account, False)) # you have no friends yet
# 			context['accounts'] = accounts
				
# 	return render(request, "account/search_results.html", context)



# def register_view(request, *args, **kwargs):
# 	user = request.user
# 	if user.is_authenticated: 
# 		return HttpResponse("You are already authenticated as " + str(user.email))

# 	context = {}
# 	if request.POST:
# 		form = RegistrationForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			email = form.cleaned_data.get('email').lower()
# 			raw_password = form.cleaned_data.get('password1')
# 			account = authenticate(email=email, password=raw_password)
# 			login(request, account)
# 			destination = kwargs.get("next")
# 			if destination:
# 				return redirect(destination)
# 			return redirect('home')
# 		else:
# 			context['registration_form'] = form

# 	else:
# 		form = RegistrationForm()
# 		context['registration_form'] = form
# 	return render(request, 'account/register.html', context)


# def logout_user(request):
# 	logout(request)
# 	return redirect("home")


# def login_user(request, *args, **kwargs):
# 	context = {}

# 	user = request.user
# 	if user.is_authenticated: 
# 		return redirect("home")

# 	destination = get_redirect_if_exists(request)
# 	print("destination: " + str(destination))

# 	if request.POST:
# 		form = AccountAuthenticationForm(request.POST)
# 		if form.is_valid():
# 			email = request.POST['email']
# 			password = request.POST['password']
# 			user = authenticate(email=email, password=password)

# 			if user:
# 				login(request, user)
# 				if destination:
# 					return redirect(destination)
# 				return redirect("home")

# 	else:
# 		form = AccountAuthenticationForm()

# 	context['login_form'] = form

# 	return render(request, "login.html", context)


# def get_redirect_if_exists(request):
# 	redirect = None
# 	if request.GET:
# 		if request.GET.get("next"):
# 			redirect = str(request.GET.get("next"))
# 	return redirect




# def account_view(request,id, *args, **kwargs):
# 	"""
# 	- Logic here is kind of tricky
# 		is_self (boolean)
# 			is_friend (boolean)
# 				-1: NO_REQUEST_SENT
# 				0: THEM_SENT_TO_YOU
# 				1: YOU_SENT_TO_THEM
# 	"""
# 	context = {}
# 	# user_id = kwargs.get("user_id")
# 	try:
#         # account = Account.objects.get(id=id)
# 		account = Account.objects.get(id=id)
# 	except:
# 		return HttpResponse("Something went wrong.")
# 	if account:
# 		context['id'] = account.id
# 		context['username'] = account.username
# 		context['email'] = account.email
# 		context['profile_image'] = account.profile_image.url
# 		context['hide_email'] = account.hide_email

# 		# Define template variables
# 		is_self = True
# 		is_friend = False
# 		user = request.user
# 		if user.is_authenticated and user != account:
# 			is_self = False
# 		elif not user.is_authenticated:
# 			is_self = False
			
# 		# Set the template variables to the values
# 		context['is_self'] = is_self
# 		context['is_friend'] = is_friend
# 		context['BASE_URL'] = settings.BASE_URL
# 		return render(request, "account/account.html", context)

# def save_temp_profile_image_from_base64String(imageString, user):
# 	INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
# 	try:
# 		if not os.path.exists(settings.TEMP):
# 			os.mkdir(settings.TEMP)
# 		if not os.path.exists(settings.TEMP + "/" + str(user.pk)):
# 			os.mkdir(settings.TEMP + "/" + str(user.pk))
# 		url = os.path.join(settings.TEMP + "/" + str(user.pk),TEMP_PROFILE_IMAGE_NAME)
# 		storage = FileSystemStorage(location=url)
# 		image = base64.b64decode(imageString)
# 		with storage.open('', 'wb+') as destination:
# 			destination.write(image)
# 			destination.close()
# 		return url
# 	except Exception as e:
# 		print("exception: " + str(e))
# 		# workaround for an issue I found
# 		if str(e) == INCORRECT_PADDING_EXCEPTION:
# 			imageString += "=" * ((4 - len(imageString) % 4) % 4)
# 			return save_temp_profile_image_from_base64String(imageString, user)
# 	return None


# def crop_image(request, *args, **kwargs):
# 	payload = {}
# 	user = request.user
# 	if request.POST and user.is_authenticated:
# 		try:
# 			imageString = request.POST.get("image")
# 			url = save_temp_profile_image_from_base64String(imageString, user)
# 			img = cv2.imread(url)

# 			cropX = int(float(str(request.POST.get("cropX"))))
# 			cropY = int(float(str(request.POST.get("cropY"))))
# 			cropWidth = int(float(str(request.POST.get("cropWidth"))))
# 			cropHeight = int(float(str(request.POST.get("cropHeight"))))
# 			if cropX < 0:
# 				cropX = 0
# 			if cropY < 0: # There is a bug with cropperjs. y can be negative.
# 				cropY = 0
# 			crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]

# 			cv2.imwrite(url, crop_img)

# 			# delete the old image
# 			user.profile_image.delete()

# 			# Save the cropped image to user model
# 			user.profile_image.save("profile_image.png", files.File(open(url, 'rb')))
# 			user.save()

# 			payload['result'] = "success"
# 			payload['cropped_profile_image'] = user.profile_image.url

# 			# delete temp file
# 			os.remove(url)
			
# 		except Exception as e:
# 			print("exception: " + str(e))
# 			payload['result'] = "error"
# 			payload['exception'] = str(e)
# 	return HttpResponse(json.dumps(payload), content_type="application/json")


# def edit_account_view(request,id, *args, **kwargs):
# 	if not request.user.is_authenticated:
# 		return redirect("login")
# 	# user_id = kwargs.get("user_id")
# 	account = Account.objects.get(pk=id)
# 	if account.pk != request.user.pk:
# 		return HttpResponse("You cannot edit someone elses profile.")
# 	context = {}
# 	if request.POST:
# 		form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
# 		if form.is_valid():
# 			form.save()
# 			return redirect('account',request.user.id)
# 			# return redirect("account:view", user_id=account.pk)
# 		else:
# 			form = AccountUpdateForm(request.POST, instance=request.user,
# 				initial={
# 					"id": account.pk,
# 					"email": account.email, 
# 					"username": account.username,
# 					"profile_image": account.profile_image,
# 					"hide_email": account.hide_email,
# 				}
# 			)
# 			context['form'] = form
# 	else:
# 		form = AccountUpdateForm(
# 			initial={
# 					"id": account.pk,
# 					"email": account.email, 
# 					"username": account.username,
# 					"profile_image": account.profile_image,
# 					"hide_email": account.hide_email,
# 				}
# 			)
# 		context['form'] = form
# 	context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
# 	return render(request, "account/edit_account.html", context)


from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from friend.friend_requests import FriendRequestStatus
 
from friend.utils import get_friend_request_or_false

from account.models import Account
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from django.conf import settings

from django.core.files.storage import default_storage
import requests

from friend.models import FriendList, FriendRequests

TEMP_PROFILE_IMAGE_NAME = 'temp_profile_image.png'

def register_view(request, *args, **kwargs):
    user = request.user

    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))


    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email,password=password)
            login(request, user)

            destination= get_redirect_if_exists(request)
            if destination:  #if destination !=None
                return redirect(destination)
            return redirect("home")
    else:
        form = RegistrationForm()
    context = {
        'registration_form':form 
    }
    return render(request, 'register.html',context)


def login_user(request,*args,**kwargs):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            return redirect('home')

        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            # form.save()
            
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:  #if destination !=None
                    return redirect(destination)
                return redirect("home")
    else:
        form = AccountAuthenticationForm()
    
    context = {
        'login_form':form
    }
    return render(request,'login.html',context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get("next"))
    return redirect


def logout_user(request):
    logout(request)
    return redirect('home')



def account_view(request,id,*args,**kwargs):
    """
	- Logic here is kind of tricky
		is_self (boolean)
			is_friend (boolean)
				-1: NO_REQUEST_SENT
				0: THEM_SENT_TO_YOU
				1: YOU_SENT_TO_THEM
	"""
    context = {}
    # user_id = kwargs.get("user_id")
    try:
        account=Account.objects.get(id=id)
    except:
        return HttpResponse("Something went wrong")
    
    # if account:
    #     context['id'] = account.id
    #     context['username']=account.username
    #     context['email']=account.email
    #     context['profile_image'] = account.profile_image.url
    #     context['hide_email'] = account.hide_email

    #     try:
    #         friend_list = FriendList.objects.get(user=account)
            
    #     except FriendList.DoesNotExist:
    #         # if doesn't exists friend in freinds list then add to friends list this account
    #         friend_list = FriendList(user=account)
    #         friend_list.save()
    #     # for showing how much friends have in self account 
    #     friends = friend_list.friends.all()

    #     context['friends'] = friends # pass it to context 

    #     # template variable 
    #     is_self = True
    #     is_friend = False
    #     user=request.user
        
    #     request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
    #     friend_requests = None

    #     if user.is_authenticated and user != account:
    #         is_self = False
    #         if friends.filter(pk=user.id):
    #             is_friend = True
    #         else:
    #             is_friend = False
    #             #case 1 : request has been sent from them to you: FriendRequestStatus.Them_sent_to_you
    #             if get_friend_request_or_false(sender=account, receiver=user) != False:
    #                 request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
    #                 context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id

    #             # case 2: request has been sent from you to them : FriendRequestStatus.YOU_sent_to_them
    #             elif get_friend_request_or_false(sender=account, receiver=user) != False:
    #                 request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
    #             # case 3 : no request has been sent. FriendRequestStatus.No_request_sent 
    #             else:
    #                 request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
                
    #     elif not user.is_authenticated:
    #         is_self = False

    #     # case if looking self.profile then show friendrequests that sent to you 
    #     else:
    #         try:
    #             friend_requests = FriendRequests.objects.filter(receiver= user, is_active=True)
    #         except:
    #             pass

    #     context['is_self'] = is_self
    #     context['is_friend'] = is_friend
    #     context['BASE_URL'] = settings.BASE_URL
    #     context['request_sent'] = request_sent
    #     context['friend_requests'] = friend_requests

    #     return render(request,'account/account.html',context)
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image
        context['hide_email'] = account.hide_email
        try:
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=account)
            friend_list.save()
        friends = friend_list.friends.all()
        
        context['friends'] = friends
	
		# Define template variables
        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value # range: ENUM -> friend/friend_request_status.FriendRequestStatus
        friend_requests = None
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
            if friends.filter(pk=user.id):
                is_friend = True
            else:
                is_friend = False
				# CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
                if get_friend_request_or_false(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
				# CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
				# CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        elif not user.is_authenticated:
            is_self = False
        else:
            try:
                friend_requests = FriendRequests.objects.filter(receiver=user, is_active=True)
            except:
                pass
			
		# Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['request_sent'] = request_sent
        context['friend_requests'] = friend_requests
        context['BASE_URL'] = settings.BASE_URL

        return render(request, "account/account.html", context)

def account_search_view(request,*args,**kwargs):
    context = {}
    if request.method == 'GET':
        search_query = request.GET.get('q')
        if len(search_query) > 0:
            search_results = Account.objects.filter(email__icontains=search_query).filter(
                                username__icontains=search_query
                            )
            user = request.user
            accounts = []

            if user.is_authenticated:
                auth_user_friend_list = FriendList.objects.get(user=user)
                for account in search_results:
                    accounts.append((account, auth_user_friend_list.is_mutual_friend(account)))
                context['accounts'] = accounts 

            else:
                for account in search_results:
                    accounts.append((account,False))  # no friends yet    
                context['accounts'] = accounts          
    return render(request,'account/search_results.html',context)


def edit_account_view(request,id, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')
    # user_id = kwargs.get('user_id')
    try:
        account = Account.objects.get(pk=id)
    except Account.DoesNotExist:
        return HttpResponse("something went wrong")
    
    if account.pk != request.user.pk:
        return HttpResponse("you can't edit someone elses profile.")

    context = {}

    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # account.profile_image.delete()
            form.save()
            return redirect('account',request.user.id)
        else:
            form = AccountUpdateForm(request.POST,instance=request.user,
            initial = {
                'id': account.pk,
                'email': account.email,
                'username':account.username,
                'profile_image': account.profile_image,
                'hide_email': account.hide_email
            })
            context['form'] = form
    else:
        form = AccountUpdateForm(
            initial = {
                'id': account.pk,
                'email': account.email,
                'username':account.username,
                'profile_image': account.profile_image,
                'hide_email': account.hide_email
            })
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request,'account/edit_account.html',context)

import os 
from django.core.files.storage import FileSystemStorage

def save_temp_profile_image_from_base64String(imageStr, user):
    INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(settings.TEMP + '/' + str(user.pk)):
            os.mkdir(settings.TEMP + '/' + str(user.pk))
        
        url = os.path.join(settings.TEMP + '/' + str(user.pk), TEMP_PROFILE_IMAGE_NAME)
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(imageStr)
        
        with storage.open('','wb+',) as des:
            des.write(image)
            des.close()
        return url 

    except Exception as e:
        print("exception: " + str(e))
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            imageStr += '=' * ((4 - len(imageStr) % 4 ) % 4 )
            return save_temp_profile_image_from_base64String(imageStr,user)
    
    return None


import cv2
from django.core import files
import json 


def crop_image(request, *args, **kwargs):
    payload = {}  #dictionary data like context

    user = request.user 

    
    if request.POST and user.is_authenticated:

        try:
            imageStr = request.POST.get('image')
            url = save_temp_profile_image_from_base64String(imageStr, user)
            img = cv2.imread(url)

            cropX = int(float(str(request.POST.get("cropX"))))
            cropY = int(float(str(request.POST.get("cropY"))))
            cropWidth = int(float(str(request.POST.get("cropWidth"))))
            cropHeight = int(float(str(request.POST.get("cropHeight"))))

            if cropX < 0:
                cropX = 0
            if cropY < 0:
                cropY = 0

            # image croping with open cv 
            crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]
            cv2.imwrite(url, crop_img)

            # del user old pic 
            user.profile_image.delete()

            # save new instance 
            user.profile_image.save("profile_image.png", files.File(open(url,'rb')))
            user.save()

            payload['result'] = 'success'
            payload['cropped_profile_image'] = user.profile_image.url

            os.remove(url)
        except Exception as e:
            print('exception: ' + str(e))
            payload['result'] = 'error'

            payload['exception'] = str(e)
    
    return HttpResponse(json.dumps(payload), content_type = "application/json")

    
