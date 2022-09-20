from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate

from account.forms import RegistrationForm

def register_view(request, *args, **kwargs):
    user = request.user

    if user.is_authenticated:
        return HttpResponse(f"You are already authenticate as {user.email}")

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email,password=password)
            login(request, user)
            destination=kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect("home")
    else:
        form = RegistrationForm()
    context = {
        'registration_form':form 
    }
    return render(request, 'register.html',context)