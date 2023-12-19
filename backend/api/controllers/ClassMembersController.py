from rest_framework import viewsets, mixins, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

from api.custom_permissions import IsModerator

from api.models import User
from api.models import ClassMember
from api.models import TeamMember
from api.serializers import ClassMemberSerializer

class ClassMembersController(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin):
    queryset = ClassMember.objects.all()
    serializer_class = ClassMemberSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        If the action is 'destroy' or 'accept', only allow admin users to access.
        If the action is 'list', only allow authenticated users to access.
        otherwise, return 403 Forbidden.
        """
        if self.action in ['destroy', 'accept', 'setleader']:
            return [permissions.IsAuthenticated(), IsModerator()]
        elif self.action in ['list', 'acceptasleader']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()


    @swagger_auto_schema(
        operation_summary="Lists all members of a class",
        operation_description="GET /classes/{class_pk}/members",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', ClassMemberSerializer(many=True)),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def list(self, request, *args, **kwargs):
        current_class_member = ClassMember.objects.filter(class_id=kwargs['class_pk'], user_id=request.user, status=ClassMember.ACCEPTED)
        if not current_class_member.exists():
            return Response({'error': 'You are not a member of this class.'}, status=403)
        
        class_members = ClassMember.objects.filter(class_id=kwargs['class_pk']).select_related('user_id').all()
        serializer = ClassMemberSerializer(class_members, many=True).data

        for class_member in serializer:
            user = User.objects.get(id=class_member['user_id'])
            class_member['first_name'] = user.first_name
            class_member['last_name'] = user.last_name
        
        return Response(serializer, status=status.HTTP_200_OK)
    

    @swagger_auto_schema(
        operation_summary="Deletes a class member",
        operation_description="DELETE /classes/{class_pk}/members/{id}",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response('No Content'),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    

    @swagger_auto_schema(
        method='PUT',
        operation_summary="Accepts a class member",
        operation_description="PUT /classes/{class_pk}/members/{id}/accept", request_body=None,
        responses={
            status.HTTP_202_ACCEPTED: openapi.Response('Accepted'),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    @action(detail=True, methods=['PUT'])
    def accept(self, request, *args, **kwargs):
        try:
            class_member = ClassMember.objects.get(id=kwargs['pk'])
            class_member.status = ClassMember.ACCEPTED
            class_member.save()
            return Response({'detail': 'User join request accepted'}, status=status.HTTP_202_ACCEPTED)
        except ClassMember.DoesNotExist:
            return Response({'error': 'Class member does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        method='POST',
        operation_summary="Sets a class member as a team leader",
        operation_description="POST /classes/{class_pk}/members/{id}/setleader", request_body=None,
        responses={
            status.HTTP_200_OK: openapi.Response('Class member is now a pending team leader.'),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    @action(detail=True, methods=['POST'])
    def setleader(self, request, *args, **kwargs):
        try:
            # get the class member by id 
            class_member = ClassMember.objects.get(id=kwargs['pk'])
            
            # check if class member is accepted
            if class_member.status != ClassMember.ACCEPTED:
                return Response({'error': 'Class member is not accepted yet'}, status=status.HTTP_400_BAD_REQUEST)
            
            # check if class member is already a team leader
            teammember = TeamMember.objects.filter(class_member_id=class_member)
            if teammember.exists():
                teammember = teammember.first()
                if teammember.role == TeamMember.LEADER and teammember.status == TeamMember.ACCEPTED:
                    return Response({'error': 'Class member is already a team leader'}, status=status.HTTP_400_BAD_REQUEST)
                if teammember.role == TeamMember.LEADER and teammember.status == TeamMember.PENDING:
                    return Response({'error': 'Class member is already a pending team leader'}, status=status.HTTP_400_BAD_REQUEST)
            
            # create a new team member with role as leader and status as pending
            team_leader = TeamMember.objects.create(
                class_member_id=class_member, 
                role=TeamMember.LEADER, 
                status=TeamMember.PENDING
            )
            team_leader.save()

            return Response({'detail': 'Class member is now a pending team leader.'}, status=status.HTTP_200_OK)
        except ClassMember.DoesNotExist:
            return Response({'error': 'Class member does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        method='PUT',
        operation_summary="Updates status of pending team leader",
        operation_description="PUT /classes/{class_pk}/members/{id}/acceptasleader", request_body=None,
        responses={
            status.HTTP_202_ACCEPTED: openapi.Response('Accepted'),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    @action(detail=True, methods=['PUT'])
    def acceptasleader(self, request, *args, **kwargs):
        try:
            # get the class member by id 
            class_member = ClassMember.objects.get(id=kwargs['pk'])
            
            # check if class member is accepted
            if class_member.status != ClassMember.ACCEPTED:
                return Response({'error': 'Class member is not accepted yet'}, status=status.HTTP_400_BAD_REQUEST)
            
             # check if class member is already a team leader
            teammember = TeamMember.objects.filter(class_member_id=class_member)
            if teammember.exists():
                teammember = teammember.first()
                if teammember.role == TeamMember.LEADER and teammember.status == TeamMember.ACCEPTED:
                    return Response({'error': 'Class member is already a team leader'}, status=status.HTTP_400_BAD_REQUEST)
            
            # update the team leader object
            teammember.status = TeamMember.ACCEPTED
            teammember.save()
            return Response({'detail': 'Class member is now a team leader.'}, status=status.HTTP_202_ACCEPTED)
        except:
            # return Internal Server Error if something went wrong
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)