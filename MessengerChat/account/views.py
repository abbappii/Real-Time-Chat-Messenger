from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from account.models import Account
from account.forms import RegistrationForm, AccountAuthenticationForm
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