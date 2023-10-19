from rest_framework import serializers

from api.models import PeerEval

class PeerEvalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerEval
        fields = ['id', 'name', 'forms_link', 'date_created', 'date_updated']
        read_only_fields = ['id', 'date_created', 'date_updated']
        extra_kwargs = {
            'name': {'required': True},
            'forms_link': {'required': True},
        }

    def create(self, validated_data):
        return PeerEval.objects.create(**validated_data)