from rest_framework import viewsets, mixins, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from api.models import Team
from api.models import TeamMember
from api.serializers import TeamSerializer
from api.serializers import UserSerializer

class TeamsController(viewsets.GenericViewSet,
                      mixins.ListModelMixin, 
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        If the action is 'create', 'destroy', 'update', or 'partial_update', only allow admin users to access.
        If the action is 'retrieve', 'list', or 'join', only allow authenticated users to access.
        otherwise, return 403 Forbidden.
        """
        if self.action in ['create','destroy', 'update', 'partial_update']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        elif self.action in ['retrieve', 'list', 'join']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    @swagger_auto_schema(
        operation_summary="Creates a new team",
        operation_description="POST /teams",
        request_body=TeamSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response('Created', TeamSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        new_team = Team.objects.get(id=response.data['id'])
        team_member = TeamMember.objects.create(
            user_id=request.user,
            team_id=new_team,
            role='tl',
            status='accepted'
        )
        team_member.save()
        return response
    
    @swagger_auto_schema(
        operation_summary="Updates a team",
        operation_description="PUT /teams/{id}",
        request_body=TeamSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Deletes a team",
        operation_description="DELETE /teams/{id}",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response('No Content'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Gets a team",
        operation_description="GET /teams/{id}",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamSerializer),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def list(self, request, *args, **kwargs):
        user = UserSerializer(request.user).data
        role = user.get('role')
        teams = []

        if role == 't':
            # For teachers, list all teams
            teams = Team.objects.all()
        elif role == 'tl':
            # For team leaders, list only the teams they belong to
            teams = Team.objects.filter(team_member__user_id=request.user, team_member__role='tl', team_member__status='accepted')
        elif role == 'tm':
            # For team members, list the teams they belong to where status is accepted
            teams = Team.objects.filter(team_member__user_id=request.user, team_member__role='tm', team_member__status='accepted')

        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Gets a team",
        operation_description="GET /teams/{id}",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Updates a team partially",
        operation_description="PATCH /teams/{id}",
        request_body=TeamSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Joins a team",
        operation_description="POST /teams/{id}/join",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    @action(detail=True, methods=['post'])
    def join(self, request, *args, **kwargs):
        team = self.get_object()
        team_member = TeamMember.objects.create(
            user_id=request.user,
            team_id=team,
            role='tm',
            status='pending'
        )
        team_member.save()
        serializer = TeamSerializer(team)
        return Response(serializer.data)