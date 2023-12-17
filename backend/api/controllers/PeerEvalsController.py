from rest_framework import viewsets, mixins, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

from api.models import PeerEval
from api.serializers import PeerEvalSerializer

class PeerEvalsController (viewsets.GenericViewSet,
                        mixins.ListModelMixin, 
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = PeerEval.objects.all()
    serializer_class = PeerEvalSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        If the action is 'destroy', only allow admin users to access.
        If the action is 'list', only allow authenticated users to access.
        otherwise, return 403 Forbidden.
        """
        if self.action in ['create', 'destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        elif self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    @swagger_auto_schema(
        operation_summary="Lists all peer evals",
        operation_description="GET /evals",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', PeerEvalSerializer(many=True)),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def list(self, request, *args, **kwargs):
        pass
        # return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Creates a peer eval",
        operation_description="POST /evals",
        request_body=PeerEvalSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response('Created', PeerEvalSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def create(self, request, *args, **kwargs):
        pass
        # return super().create(request, *args, **kwargs)
        
    @swagger_auto_schema(
        operation_summary="Retrieves a peer eval",
        operation_description="GET /evals/{id}",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', PeerEvalSerializer),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Updates a peer eval",
        operation_description="PUT /evals/{id}",
        request_body=PeerEvalSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response('OK', PeerEvalSerializer),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def update(self, request, *args, **kwargs):
        pass
        # return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Deletes a peer eval",
        operation_description="DELETE /evals/{id}",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', PeerEvalSerializer),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def destroy(self, request, *args, **kwargs):
        pass
        # return super().destroy(request, *args, **kwargs)
