from django.db import models

class TeamMember(models.Model):
    class_member_id = models.ForeignKey('ClassMember', on_delete=models.CASCADE, null=True)
    team_id = models.ForeignKey('Team', on_delete=models.CASCADE, null=True)

    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now=True)

    