from rest_framework import serializers

from api.models import ClassMember, User, Class
from .UserSerializer import UserSerializer

class ClassMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMember
        fields = ['id', 'user_id','class_id', 'role', 'status']
        labels = {
            'user_id': 'User ID',
            'class_id': 'Class ID',
            'role': 'Role',
            'status': 'Status'
        }

        # disable input data body for PUT and PATCH requests
        extra_kwargs = {
            'user_id': {'read_only': True, 'required': False},
            'class_id': {'read_only': True, 'required': False},
            'role': {'read_only': True, 'required': False},
            'status': {'read_only': True, 'required': False}
        }