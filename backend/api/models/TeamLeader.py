from django.db import models

class TeamLeader(models.Model):
    class_member_id = models.ForeignKey('ClassMember', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, default='pending')
    
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)

    