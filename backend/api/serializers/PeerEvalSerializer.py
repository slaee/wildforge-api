from rest_framework import serializers

from api.models import PeerEval

class PeerEvalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerEval
        fields = ['id', 'name', 'forms_link', 'date_created', 'date_updated']
        labels = {
            'name': 'Name',
            'forms_link': 'Forms Link',
            'date_created': 'Date Created',
            'date_updated': 'Date Updated',
        }

class AssignPeerEvalSerializer(serializers.Serializer):
    classrooms = serializers.ListField(
        child=serializers.IntegerField()
    )