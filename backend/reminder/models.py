from django.db import models

# Create your models here.

class Reminder(models.Model):
    title=models.CharField(max_length=1000)
    date= models.DateField()
    time=models.TimeField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title #Mainly useful for looking reminders in django admin


