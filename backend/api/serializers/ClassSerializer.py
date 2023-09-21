from rest_framework import serializers

from api.models import Class

class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name', 'sections', 'schedule']
        labels = {
            'name': 'Class Name',
            'sections': 'Number of Sections',
            'schedule': 'Schedule',
        }