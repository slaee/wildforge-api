import random
import string
from django.db import transaction
from rest_framework import serializers

from api.models import Class

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name', 'sections', 'schedule', 'class_code']
        labels = {
            'name': 'Class Name',
            'sections': 'Number of Sections',
            'schedule': 'Schedule',
            'class_code': 'Class Code'
        }

    @transaction.atomic
    def create(self, validated_data):
        while True: # Keep generating class_code until a unique one is generated
            class_code_length = 8
            characters = string.ascii_letters + string.digits  # Alphanumeric characters
            class_code = ''.join(random.choice(characters) for _ in range(class_code_length))

            # Check if the generated class_code already exists in the database
            if not Class.objects.filter(class_code=class_code).exists():
                validated_data['class_code'] = class_code
                instance = self.Meta.model(**validated_data)
                instance.save()
                return instance

                