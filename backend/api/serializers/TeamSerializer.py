from rest_framework import serializers

from api.models import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        pass