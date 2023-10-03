from django.db import models

class ClassMember(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    class_id = models.ForeignKey('Class', on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=2, default='s')
    status = models.CharField(max_length=50, default='pending')
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
