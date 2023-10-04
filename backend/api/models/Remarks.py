from django.db import models

class Remarks(models.Model):
    sender_id = models.ForeignKey('ClassMember', on_delete=models.CASCADE, null=True)
    receiver_id = models.ForeignKey('TeamMember', on_delete=models.CASCADE, null=True)
    remarks = models.TextField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    is_viewed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)