from rest_framework import viewsets, mixins, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
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
        if self.action in ['destroy', 'accept']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        elif self.action in ['list']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    @swagger_auto_schema(operation_description="GET /classes/{class_pk}/members")
    def list(self, request, *args, **kwargs):
        class_member = ClassMember.objects.filter(class_id=kwargs['class_pk'], user_id=request.user, status='accepted')
        if not class_member.exists():
            return Response({'error': 'You are not a member of this class.'}, status=403)
        
        class_members = ClassMember.objects.filter(class_id=kwargs['class_pk'])
        serializer = self.get_serializer(class_members, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(operation_description="DELETE /classes/{class_pk}/members/{id}")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="PUT /classes/{class_pk}/members/{id}/accept", request_body=None)
    @action(detail=True, methods=['PUT'])
    def accept(self, request, *args, **kwargs):
        class_member = ClassMember.objects.get(id=kwargs['pk'])
        class_member.status = 'accepted'
        class_member.save()
        return Response({'status': 'accepted'})
    
