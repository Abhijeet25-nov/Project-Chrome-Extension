from django.shortcuts import render,redirect
from .models import Reminder
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

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

def delete_reminder(request, id):
    if request.method == "POST":
        reminder = Reminder.objects.get(id=id)
        reminder.delete()

    return redirect("home")


#----------------API---------------------
@csrf_exempt
def api_reminders(request):
    
    if request.method=="GET":
    
        reminders=Reminder.objects.all()
        
        data=[]
        
        for reminder in reminders:
            data.append({
                "id": reminder.id,
                "title": reminder.title,
                "date": str(reminder.date),
                "time": str(reminder.time),
            })
            
        return JsonResponse(data,safe=False)
    
    elif request.method == "POST":

        title = request.POST.get("title")
        date = request.POST.get("date")
        time = request.POST.get("time")

        reminder = Reminder.objects.create(
            title=title,
            date=date,
            time=time
        )

        return JsonResponse({
            "message": "Reminder created successfully",
            "id": reminder.id,
            "title": reminder.title,
            "date": str(reminder.date),
            "time": str(reminder.time)
        })
        
@csrf_exempt
def api_delete_reminder(request,id):
    
    if request.method=="DELETE":
        reminder = Reminder.objects.get(id=id)
        reminder.delete()
        
        return JsonResponse({
            "message": "Reminder Deleted successfully"
        })
    
    return JsonResponse({
        "error" : "Only DELETE method is allowed"
    })    
            