from rest_framework import serializers

from api.models import ClassMember

class ClassMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMember
        pass