from django.shortcuts import render

def home(request, *args, **kwargs):
    context={}
    return render(request, 'personal/home.html', context)
