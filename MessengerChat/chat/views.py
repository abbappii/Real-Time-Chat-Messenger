from django.shortcuts import render

# Create your views here.

def Home(request):
    name = 'abbappii'
    context ={
        'name':name
    }
    return render(request,'home.html',context)