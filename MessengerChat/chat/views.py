from django.shortcuts import render

from django.conf import settings
DEBUG = True
def Home(request):
    context = {}
    context['debug'] = DEBUG
    context['room_id'] = "1"

    return render(request,'home.html',context)

