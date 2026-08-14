from django.urls import path
from . import views

urlpatterns=[
    path("add-reminder/",views.add_reminder,name="add_reminder"),
]

