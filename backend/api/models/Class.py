from django.db import models
from .User import User

class Class(models.Model):
    teacherId = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sections = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
    class_code = models.CharField(max_length=100, unique=True) # class code is generated when class is created

    REQUIRED_FIELDS = ['name', 'sections', 'schedule']