from rest_framework import viewsets, mixins, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response


from api.custom_permissions import IsTeamLeader

from api.models import Team
from api.models import User
from api.models import TeamMember
from api.serializers import TeamMemberSerializer

class TeamMembersController(viewsets.GenericViewSet,
                      mixins.ListModelMixin, 
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
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
        if self.action in ['create','destroy', 'update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsTeamLeader()]
        elif self.action in ['retrieve', 'list', 'join']:
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
        pass
        # current_team_member = TeamMember.objects.filter(team_id=kwargs['team_pk'], user_id=request.user, status='accepted')
        # if not current_team_member.exists():
        #     return Response({'error': 'You are not a member of this class.'}, status=403)
        
        # team_members = TeamMember.objects.filter(team_id=kwargs['team_pk']).select_related('user_id').all()
        # serializer = TeamMemberSerializer(team_members, many=True).data

        # for team_member in serializer:
        #     user = User.objects.get(id=team_member['user_id'])
        #     team_member['first_name'] = user.first_name
        #     team_member['last_name'] = user.last_name
        

        # return Response(serializer, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_summary="Remove a member from the team",
        operation_description="DELETE /teams/{team_pk}/members/{id}",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamMemberSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def destroy(self, request, *args, **kwargs):
        pass
        # team_member = TeamMember.objects.get(team_id=kwargs['team_pk'], id=kwargs['id'])
        # team_leader = TeamMember.objects.get(team_id=kwargs['team_pk'], role='tl')
    
        # # Check if the user is the team leader of the team member's team or a teacher of the class
        # if not (request.user == team_leader or request.user.is_teacher):
        #     return Response({'detail': 'You are not authorized to remove this team member.'}, status=status.HTTP_403_FORBIDDEN)

        # team_member.delete()
        # return Response({'message': 'Team member removed.'}, status=status.HTTP_200_OK)
    
    # ENDPOINT FOR A TEAM LEADER TO ACCEPT A PENDING TEAM MEMBER
    @swagger_auto_schema(
        operation_summary="Accept a team member",
        operation_description="POST /teams/{team_pk}/members/{id}/accept",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamMemberSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    @action(detail=True, methods=['post'])
    def accept_member(self, request, *args, **kwargs):
        pass
        # team_member = TeamMember.objects.get(team_id=kwargs['team_pk'], user_id=kwargs['id'])
        # team_leader = TeamMember.objects.get(team_id=kwargs['team_pk'], role='tl')
    
        # # Check if the user is a team leader or teacher
        # if not (team_leader or request.user.is_teacher):
        #     return Response({'detail': 'You are not authorized to accept a team member.'}, status=status.HTTP_403_FORBIDDEN)

        # team_member.status = 'accepted'
        # team_member.save()
        # serializer = TeamMemberSerializer(team_member)
        # return Response(serializer.data)