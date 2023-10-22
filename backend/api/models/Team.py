from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    max_members = models.IntegerField(default=1)
    status = models.CharField(max_length=10, default='open')

    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['name', 'max_members']