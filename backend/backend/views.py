from django.http import HttpResponse
from django.shortcuts import render
from reminder.models import Reminder


def home(request):
    # return HttpResponse("Reminder Application")
    reminders = Reminder.objects.all()
    return render(request,"mainpage.html",{"reminders": reminders})


#app related methods

def about(request):
    return HttpResponse("Hello World, I am Abhijeet")