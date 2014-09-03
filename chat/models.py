from django.db import models

# Create your models here.

class Message(models.Model):
    isDisplay = models.BooleanField(default = False)
    content = models.CharField(max_length = 256)
    customID = models.CharField(max_length = 128)
    name = models.CharField(max_length = 16)
    phone = models.CharField(max_length = 16)
    time = models.DateTimeField(auto_now_add = True)

class Feedback(models.Model):
    customID = models.CharField(max_length = 128)
    isDisplay = models.BooleanField(default = False)
    content = models.CharField(max_length = 256)
    time = models.DateTimeField(auto_now_add = True)