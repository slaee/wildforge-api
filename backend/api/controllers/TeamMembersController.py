from rest_framework import viewsets, mixins, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from api.custom_permissions import IsTeamLeader

from api.models import User
from api.models import TeamMember

from api.serializers import TeamMemberSerializer
from api.serializers import NoneSerializer

class TeamMembersController(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        If the action is 'create', 'destroy', 'update', or 'partial_update', only allow admin users to access.
        If the action is 'retrieve', 'list', or 'join', only allow authenticated users to access.
        otherwise, return 403 Forbidden.
        """
        if self.action in ['remove', 'accept']:
            return [permissions.IsAuthenticated(), IsTeamLeader()]
        elif self.action in ['retrieve', 'list']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    @swagger_auto_schema(
        operation_summary="Lists all members of the team",
        operation_description="GET /teams/{team_pk}/members",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamMemberSerializer(many=True)),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }   
    )
    def list(self, request, *args, **kwargs):
        try:
            team_members = TeamMember.objects.filter(team_id=kwargs['team_pk']).all()
            serializer = TeamMemberSerializer(team_members, many=True).data

            for team_member in serializer:
                user = User.objects.get(id=team_member['user_id'])
                team_member['first_name'] = user.first_name
                team_member['last_name'] = user.last_name
            
            return Response(serializer, status=status.HTTP_200_OK)
        except TeamMember.DoesNotExist:
            return Response({'error': 'Team does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_summary="Remove a member from the team",
        operation_description="DELETE /teams/{team_pk}/members/{id}/remove",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamMemberSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    @action(detail=True, methods=['DELETE'])
    def remove(self, request, *args, **kwargs):
        try:
            team_member = TeamMember.objects.get(id=kwargs['pk'])
            team_member.delete()

            return Response({'detail': 'Team Member removed from team'}, status=status.HTTP_200_OK)
        except TeamMember.DoesNotExist:
            return Response({'error': 'Team Member does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_summary="Accept a team member",
        operation_description="PUT /teams/{team_pk}/members/{id}/accept",
        request_body=NoneSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamMemberSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    @action(detail=True, methods=['PUT'])
    def accept(self, request, *args, **kwargs):
        try:
            pending_team_member = TeamMember.objects.get(id=kwargs['pk'])
            pending_team_member.status = TeamMember.ACCEPTED
            pending_team_member.save()

            return Response(TeamMemberSerializer(pending_team_member).data, status=status.HTTP_200_OK)
        except TeamMember.DoesNotExist:
            return Response({'error': 'Team Member does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        