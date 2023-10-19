from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    max_members = models.IntegerField(default=4)
    status = models.IntegerField(default=1)

    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['name', 'max_members']