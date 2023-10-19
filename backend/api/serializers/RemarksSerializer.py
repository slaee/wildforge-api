from rest_framework import serializers

from api.models import Remarks

class RemarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remarks
        fields = ['id', 'sender_id', 'receiver_id', 'remarks', 'type', 'is_viewed', 'is_approved']
        labels = {
            'sender_id': 'Sender',
            'receiver_id': 'Receiver',
            'remarks': 'Remarks',
            'type': 'Type',
            'is_viewed': 'Is Viewed',
            'is_approved': 'Is Approved'
        }

        # set default values
        extra_kwargs = {
            'is_viewed': {'default': False},
            'is_approved': {'default': False}
        }

    def create(self, validated_data):
        remarks = Remarks.objects.create(**validated_data)
        return remarks