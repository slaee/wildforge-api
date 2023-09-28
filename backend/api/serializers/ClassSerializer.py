import random
import string
from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from api.models import Class

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name', 'sections', 'schedule', 'class_code', 'class_member']
        labels = {
            'name': 'Class Name',
            'sections': 'Number of Sections',
            'schedule': 'Schedule',
            'class_code': 'Class Code'
        }

        # make class_code read-only and update-only
        extra_kwargs = {
            'class_code': {'read_only': True, 'required': False}
        }
    
    class_member = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='class-class-members-list',
        parent_lookup_kwargs={'class_pk': 'class_id'}
    )

    def create(self, validated_data):
        class_code_length = 8
        characters = string.ascii_letters + string.digits  # Alphanumeric characters
        while True: # Keep generating class_code until a unique one is generated
            class_code = ''.join(random.choice(characters) for _ in range(class_code_length))

            # Check if the generated class_code already exists in the database
            if not Class.objects.filter(class_code=class_code).exists():
                instance = self.Meta.model(**validated_data)
                instance.class_code = class_code
                instance.save()
                return instance
            
class JoinClassSerializer(serializers.Serializer):
    class_code = serializers.CharField(max_length=8)

    class Meta:
        ref_name = 'JoinClassInput'