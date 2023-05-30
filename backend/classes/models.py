from django.db import models

# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=120)
    sections = models.CharField(max_length=120)
    schedule = models.CharField(max_length=120)
    