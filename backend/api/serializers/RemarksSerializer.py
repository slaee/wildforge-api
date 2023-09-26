from rest_framework import serializers

from api.models import Remarks

class RemarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remarks
        pass