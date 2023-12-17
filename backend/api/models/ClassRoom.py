from uuid import uuid4
from django.db import models

class ClassRoom(models.Model):
    class_code = models.CharField(default=uuid4().hex[:8].upper(),max_length=8, unique=True)
    course_name = models.CharField(max_length=100)
    sections = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100)
    max_teams_members = models.IntegerField(default=5)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['name', 'sections', 'schedule']