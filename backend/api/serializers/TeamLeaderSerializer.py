from rest_framework import serializers

from api.models import TeamLeader

class TeamLeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamLeader
        fields = ['id', 'class_member_id', 'status', 'date_created', 'date_updated']
        labels = {
            'class_member_id': 'Class Member ID',
            'status': 'Status',
            'date_created': 'Date Created',
            'date_updated': 'Date Updated'
        }

        # disable input data body for PUT and PATCH requests
        extra_kwargs = {
            'class_member_id': {'read_only': True, 'required': False},
            'status': {'default': 'pending', 'required': False},
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
