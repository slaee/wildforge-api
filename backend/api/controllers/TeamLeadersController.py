from rest_framework import viewsets, mixins, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from api.models import TeamLeader
from api.models import ClassMember
from api.models import User
from api.serializers import ClassMemberSerializer
from api.serializers import TeamLeaderSerializer

class TeamLeadersController(viewsets.GenericViewSet,
                      mixins.ListModelMixin):
    queryset = TeamLeader.objects.all()
    serializer_class = TeamLeaderSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        If the action is 'destroy' or 'accept', only allow admin users to access.
        If the action is 'list', only allow authenticated users to access.
        otherwise, return 403 Forbidden.
        """
        if self.action in ['list']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return super().get_permissions()
    
    @swagger_auto_schema(
        operation_summary="Lists all team leaders of a class",
        operation_description="GET /classes/{class_pk}/teamleaders",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', TeamLeaderSerializer(many=True)),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def list(self, request, *args, **kwargs):
        team_leaders = TeamLeader.objects.filter(class_member_id__class_id=kwargs['class_pk']).select_related('class_member_id').all()
        serializer = TeamLeaderSerializer(team_leaders, many=True).data

        for team_leader in serializer:
            class_member = ClassMember.objects.get(id=team_leader['class_member_id'])
            class_member = ClassMemberSerializer(class_member).data
            user = User.objects.get(id=class_member['user_id'])
            team_leader['first_name'] = user.first_name
            team_leader['last_name'] = user.last_name
        
        return Response(serializer, status=status.HTTP_200_OK)