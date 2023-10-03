from rest_framework import viewsets, mixins, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

from api.models import ClassMember
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
        if self.action in ['destroy', 'accept']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        elif self.action in ['list']:
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
        class_member = ClassMember.objects.filter(class_id=kwargs['class_pk'], user_id=request.user, status='accepted')
        if not class_member.exists():
            return Response({'error': 'You are not a member of this class.'}, status=403)
        
        class_members = ClassMember.objects.filter(class_id=kwargs['class_pk'])
        serializer = self.get_serializer(class_members, many=True)
        return Response(serializer.data)
    

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
            class_member.status = 'accepted'
            class_member.save()
            return Response({'detail': 'User join request accepted'}, status=status.HTTP_202_ACCEPTED)
        except ClassMember.DoesNotExist:
            return Response({'error': 'Class member does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
    
