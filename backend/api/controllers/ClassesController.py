from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

from api.models import Class
from api.serializers import ClassesSerializer

class ClassesController(ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassesSerializer

    @swagger_auto_schema(operation_description="GET /classes")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="POST /classes")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="GET /classes/{id}")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="PUT /classes/{id}")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="PATCH /classes/{id}")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="DELETE /classes/{id}")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)