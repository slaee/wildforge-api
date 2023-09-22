from rest_framework import viewsets, mixins
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from api.models import User
from api.serializers import UserSerializer

class UsersController(viewsets.GenericViewSet,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_description="POST /users")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="GET /users/{id}")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="PUT /users/{id}")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="PATCH /users/{id}")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="DELETE /users/{id}")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
