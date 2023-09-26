from rest_framework import serializers

from api.models import ClassAssigned

class ClassAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassAssigned
        pass