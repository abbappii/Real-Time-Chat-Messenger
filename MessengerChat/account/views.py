from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from account.forms import RegistrationForm, AccountAuthenticationForm

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