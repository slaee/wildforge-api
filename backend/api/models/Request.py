from django.db import models

class Request(models.Model):
    sender_id = models.ForeignKey('ClassMember', on_delete=models.CASCADE, null=True, related_name='sender')
    receiver_id = models.ForeignKey('ClassMember', on_delete=models.CASCADE, null=True, related_name='receiver')

    message = models.TextField(blank=True, null=True)

    DISCHARGE_MEMBER_REQUEST = 0
    JOIN_TEAM_REQUEST = 1
    LEAVE_TEAM_REQUEST = 2
    remarks_type_choices = (
        (DISCHARGE_MEMBER_REQUEST, 'Discharge Member Request'),
        (JOIN_TEAM_REQUEST, 'Join Team Request'),
        (LEAVE_TEAM_REQUEST, 'Leave Team Request'),
    )
    request_type = models.PositiveSmallIntegerField(choices=remarks_type_choices, null=True, blank=True)

    PENDING = 0
    ACCEPTED = 1
    DECLINED = 2
    status_choices = (
        (PENDING, 'pending'),
        (ACCEPTED, 'accepted'),
        (DECLINED, 'declined'),
    )
    status = models.PositiveSmallIntegerField(choices=status_choices, null=True, blank=True)

    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)
