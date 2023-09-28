from django.db import models

class ClassAssigned(models.Model):
    peer_eval_id = models.ForeignKey('PeerEval', on_delete=models.CASCADE, null=True)
    class_id = models.ForeignKey('Class', on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['peer_eval_id', 'class_id']