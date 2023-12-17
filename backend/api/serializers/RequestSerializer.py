from rest_framework import serializers

from api.models import Request

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'sender_id', 'receiver_id', 'message', 'request_type', 'status']
        labels = {
            'sender_id': 'Sender ID',
            'receiver_id': 'Receiver ID',
            'message': 'Message',
            'request_type': 'Request Type',
            'status': 'Status',
        }

        extra_kwargs = {
            'sender_id': {'read_only': True, 'required': False},
            'receiver_id': {'read_only': True, 'required': False},
            'message': {'read_only': True, 'required': False},
            'request_type': {'read_only': True, 'required': False},
            'status': {'read_only': True, 'required': False},
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance