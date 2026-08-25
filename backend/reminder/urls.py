from django.urls import path
from . import views

urlpatterns=[
    path("add-reminder/",views.add_reminder,name="add_reminder"),
    path("delete-remimder/<int:id>/",views.delete_reminder,name="delete_reminder"),
    path("api/reminders/", views.api_reminders, name="api_reminders"),
    
    path("api/reminders/<int:id>/", 
         views.api_delete_reminder, 
         name="api_delete_reminder"
    ),
]

