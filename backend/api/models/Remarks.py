from django.db import models

class Remarks(models.Model):
    sender_id = models.ForeignKey('ClassMember', on_delete=models.CASCADE, related_name='sent_remarks', null=True)
    receiver_id = models.ForeignKey('ClassMember', on_delete=models.CASCADE, related_name='received_remarks', null=True)
    remarks = models.TextField(blank=True, null=True)
    type = models.IntegerField(default=0)
    is_viewed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
