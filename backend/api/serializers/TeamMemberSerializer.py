from rest_framework import serializers

from api.models import TeamMember

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['id', 'class_member_id', 'team_id']
        labels = {
            'class_member_id': 'Class Member ID',
            'team_id': 'Team ID'
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    