from django.shortcuts import render,redirect
from .models import Reminder
from django.contrib import messages
# Create your views here.

def add_reminder(request):
    
    if request.method=="POST":
        title=request.POST.get("title")
        date=request.POST.get("date")
        time=request.POST.get("time")
        
        reminder=Reminder.objects.create(
            title=title,
            date=date,
            time=time
        )
        
        messages.success(request,"Reminder Added Successfully")
        print({
            "title": reminder.title,
            "date": reminder.date,
            "time": reminder.time,
            "created_at": reminder.created_at
        })
        
        
        return redirect("home")
    
    return redirect("home")