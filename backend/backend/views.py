from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # return HttpResponse("Reminder Application")
    return render(request,"mainpage.html")


#app related methods

def about(request):
    return HttpResponse("Hello World, I am Abhijeet")