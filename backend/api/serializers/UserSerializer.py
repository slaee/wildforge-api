from rest_framework import serializers

from api.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'is_staff']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'password': 'Password',
            'is_staff': 'Is Staff',
            'is_superuser': 'Is Superuser'
        }

        # set default values
        extra_kwargs = {
            'is_staff': {'default': False},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser']
        # make all read-only fields
        extra_kwargs = {
            'first_name': {'read_only': True, 'required': False},
            'last_name': {'read_only': True, 'required': False},
            'email': {'read_only': True, 'required': False},
            'is_staff': {'read_only': True, 'required': False},
            'is_superuser': {'read_only': True, 'required': False}
        }