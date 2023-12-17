from rest_framework import viewsets, mixins, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from api.models import Team
from api.models import TeamMember
from api.models import ClassMember

from api.serializers import TeamSerializer
from api.serializers import NoneSerializer
from api.serializers import TeamMemberSerializer

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
        if self.action in ['create','destroy', 'update', 'partial_update', 'retrieve', 'list', 'join']:
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
        pass
        # response = super().create(request, *args, **kwargs)
        # # get class member id by user id
        # class_member = ClassMember.objects.get(user_id=request.user)

        # new_team = Team.objects.get(id=response.data['id'])
        # team_member = TeamMember.objects.create(
        #     class_member_id=class_member,
        #     team_id=new_team,
        #     role='l',
        #     status='accepted'
        # )
        # team_member.save()
        # return response
    
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
        pass
        # return super().update(request, *args, **kwargs)
    
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
        pass
        # return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Gets a team",
        operation_description="GET /classes/{class_pk}/teams",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamSerializer),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def list(self, request, *args, **kwargs):
        pass
        # # get all teams and join with team members
        # response = super().list(request, *args, **kwargs)
        # for team in response.data:
        #     team_members = TeamMember.objects.filter(team_id=team['id'])
        #     team['team_members'] = TeamMemberSerializer(team_members, many=True).data
        # return response
    
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
        pass
        # response = super().retrieve(request, *args, **kwargs)
        # team_members = TeamMember.objects.filter(team_id=response.data['id'])
        # response.data['team_members'] = TeamMemberSerializer(team_members, many=True).data
        # return response
    
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
        pass
        # return super().partial_update(request, *args, **kwargs)
    
    
    @swagger_auto_schema(
        method='PUT',
        operation_summary="Post Hiring",
        operation_description="PUT /teams/{id}/open",
        request_body=NoneSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    @action(detail=True, methods=['PUT'])
    def open(self, request, *args, **kwargs):
        pass
        # team = self.get_object()
        
        # # Check if the recruitment status is 1 (recruitment is open)
        # if team.status == 1:
        #     return Response({"detail": "Team is already open for hiring"}, status=status.HTTP_400_BAD_REQUEST)
        
        # # Check if the current number of team members is less than max_members
        # current_members_count = TeamMember.objects.filter(team_id=team, status='accepted').count()
        # if current_members_count >= team.max_members:
        #     return Response({"detail": "The team has reached the maximum number of members."}, status=status.HTTP_400_BAD_REQUEST)

        # # If all conditions are met, update status
        # team.status = 1
        # team.save()
        
        # serializer = TeamSerializer(team)
        # return Response(serializer.data)

    @swagger_auto_schema(
        method='PUT',
        operation_summary="Close Hiring",
        operation_description="PUT /teams/{id}/close",
        request_body=NoneSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response('No Content'),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    @action(detail=True, methods=['PUT'])
    def close(self, request, *args, **kwargs):
        pass
        # team = self.get_object()
        
        # # Check if the recruitment status is 2 (hiring is open)
        # if team.status == 0:
        #     return Response({"detail": "Team is already closed for hiring."}, status=status.HTTP_400_BAD_REQUEST)
    
        # # If all conditions are met, update status
        # team.status = 0 # 0 means recruitment is closed
        # team.save()

        # # Delete all pending team members
        # pending_team_members = TeamMember.objects.filter(team_id=team, status='pending')
        # pending_team_members.delete()

        # serializer = TeamSerializer(team)
        # return Response(serializer.data)
    
    # ENDPOINT FOR A CLASS MEMBER TO APPLY TO A HIRING POST
    @swagger_auto_schema(
        operation_summary="Apply to a team",
        operation_description="POST /teams/{id}/join",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    @action(detail=True, methods=['post'])
    def join(self, request, *args, **kwargs):
        pass
        # team = self.get_object()
        
        # # Check if the recruitment status is 2 (hiring is open)
        # if team.recruitment_status != 2:
        #     return Response({"detail": "Hiring is not open for this team."}, status=status.HTTP_400_BAD_REQUEST)
        
        # # Check if the status is 1 (active team)
        # if team.status != 1:
        #     return Response({"detail": "This team is not active."}, status=status.HTTP_400_BAD_REQUEST)
        
        # # Check if the current number of team members is less than max_members
        # current_members_count = TeamMember.objects.filter(team_id=team, status='accepted').count()
        # if current_members_count >= team.max_members:
        #     return Response({"detail": "The team has reached the maximum number of members."}, status=status.HTTP_400_BAD_REQUEST)

        # # Check if the user is already a member of the team
        # if TeamMember.objects.filter(team_id=team, user_id=request.user, status='accepted').exists():
        #     return Response({"detail": "You are already a member of this team."}, status=status.HTTP_400_BAD_REQUEST)
        
        # # Check if the user has already applied to the team
        # if TeamMember.objects.filter(team_id=team, user_id=request.user, status='pending').exists():
        #     return Response({"detail": "You have already applied to this team."}, status=status.HTTP_400_BAD_REQUEST)
        
        # # If all conditions are met, create a team member with status pending
        # team_member = TeamMember.objects.create(
        #     user_id=request.user,
        #     team_id=team,
        #     role='tm',
        #     status='pending'
        # )
        # team_member.save()
        # serializer = TeamSerializer(team)
        # return Response(serializer.data)
    
    # ENDPOINT TO REQUEST TO JOIN A TEAM
    @swagger_auto_schema(
        operation_summary="Request to join a team",
        operation_description="POST /teams/{id}/request",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    @action(detail=True, methods=['post'])
    def request(self, request, *args, **kwargs):
        pass
        # team = self.get_object()
        
        # # Check if the recruitment status is 2 (hiring is open)
        # if team.recruitment_status != 2:
        #     return Response({"detail": "Hiring is not open for this team."}, status=status.HTTP_400_BAD_REQUEST)
        
        # # Check if the status is 1 (active team)
        # if team.status != 1:
        #     return Response({"detail": "This team is not active."}, status=status.HTTP_400_BAD_REQUEST)
        
        # # Check if the current number of team members is less than max_members
        # current_members_count = TeamMember.objects.filter(team_id=team, status='accepted').count()
        # if current_members_count >= team.max_members:
        #     return Response({"detail": "The team has reached the maximum number of members."}, status=status.HTTP_400_BAD_REQUEST)

        # # Check if the user is already a member of the team
        # if TeamMember.objects.filter(team_id=team, user_id=request.user, status='accepted').exists():
        #     return Response({"detail": "You are already a member of this team."}, status=status.HTTP_400_BAD_REQUEST)
        
        # # Check if the user has already applied to the team
        # if TeamMember.objects.filter(team_id=team, user_id=request.user, status='pending').exists():
        #     return Response({"detail": "You have already applied to this team."}, status=status.HTTP_400_BAD_REQUEST)
        
        # # If all conditions are met, create a team member with status pending
        # team_member = TeamMember.objects.create(
        #     user_id=request.user,
        #     team_id=team,
        #     role='tm',
        #     status='pending'
        # )
        # team_member.save()
        # serializer = TeamSerializer(team)
        # return Response(serializer.data)

    

    

    

    








    
