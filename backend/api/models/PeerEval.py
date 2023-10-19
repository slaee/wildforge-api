from django.db import models

class PeerEval(models.Model):
    name = models.CharField(max_length=255)
    forms_link = models.TextField(blank=False, null=False)

    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['name', 'forms_link']
