from rest_framework import serializers

from api.models import ClassMember, User, Class

class ClassMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMember
        fields = ['id', 'user_id','class_id', 'is_teacher']
        labels = {
            'user_id': 'User ID',
            'class_id': 'Class ID',
            'is_teacher': 'User is a teacher?'
        }

    def create(self, validated_data):
        user_id = validated_data.get('user_id')
        class_id = validated_data.get('class_id')

        # Check if user_id and class_id exist in the database
        if not User.objects.filter(id=user_id).exists():
            raise serializers.ValidationError("User ID does not exist.")

        if not Class.objects.filter(id=class_id).exists():
            raise serializers.ValidationError("Class ID does not exist.")

        # Create the instance if both IDs exist
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance