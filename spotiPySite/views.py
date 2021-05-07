from django.http import HttpResponse
from django.shortcuts import render
from spotipyStuff.generate import testMain

def index(request):
    return render(request,"index.html",{})

def resultpage(request):
    print(request.POST.get('search'))
    context = {
        "search": request.POST.get('search')
    }
    result = testMain(context)
    return render(request,"resultpage.html", result)