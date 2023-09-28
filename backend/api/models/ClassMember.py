from django.db import models

class ClassMember(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    class_id = models.ForeignKey('Class', on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
