from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=100)
    sections = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100)

    class_code = models.CharField(max_length=8, unique=True)

    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['name', 'sections', 'schedule']