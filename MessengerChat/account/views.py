from re import search
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from account.models import Account
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from django.conf import settings

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
    
    if account:
        context['id'] = account.id
        context['username']=account.username
        context['email']=account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email

        # template variable 
        is_self = True
        is_friend = False
        user=request.user

        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False


        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL


    return render(request,'account/account.html',context)

def account_search_view(request,*args,**kwargs):
    context = {}
    if request.method == 'GET':
        search_query = request.GET.get('q')
        if len(search_query) > 0:
            search_results = Account.objects.filter(email__icontains=search_query).filter(
                                username__icontains=search_query
                            )
            accounts = []
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
            account.profile_image.delete()
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