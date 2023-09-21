from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=100)
    sections = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100)