from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import get_object_or_404
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="POST /users")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="GET /users/{id}")
    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        self.check_object_permissions(request, user)
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="PUT /users/{id}")
    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        self.check_object_permissions(request, user)
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="PATCH /users/{id}")
    def partial_update(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        self.check_object_permissions(request, user)
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="DELETE /users/{id}")
    def destroy(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        self.check_object_permissions(request, user)
        return super().destroy(request, *args, **kwargs)
