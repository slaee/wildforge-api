from rest_framework import viewsets, mixins, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from api.models import Class
from api.models import ClassMember
from api.serializers import ClassSerializer
from api.serializers import UserSerializer
from api.serializers import SuperUserSerializer
from api.serializers import JoinClassSerializer

class ClassesController(viewsets.GenericViewSet,
                      mixins.ListModelMixin, 
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ['create','destroy', 'update', 'partial_update']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        elif self.action in ['retrieve', 'list', 'join']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    @swagger_auto_schema(operation_description="POST /classes")
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        new_class = Class.objects.get(id=response.data['id'])
        class_member = ClassMember.objects.create(
            user_id=request.user,
            class_id=new_class,
            role='t',
            status='accepted'
        )
        class_member.save()
        return response

    @swagger_auto_schema(operation_description="GET /classes")
    def list(self, request, *args, **kwargs):
        # JOIN ClassMembers ON ClassMembers.class_id = Class.id LEFT JOIN Users ON Users.id = ClassMembers.user_id
        try:
            user = SuperUserSerializer(request.user).data            
            if user.get('is_superuser'):
                queryset = Class.objects.all()
                serializer = self.get_serializer(queryset, many=True)
            else:
                queryset = Class.objects.filter(classmember__user_id=request.user, classmember__status='accepted')
                serializer = self.get_serializer(queryset, many=True)
        except:
            # <DEV ONLY>
            queryset = Class.objects.all()
            serializer = self.get_serializer(queryset, many=True)
            # </DEV ONLY>

        for i in range(len(serializer.data)):
            class_id = serializer.data[i]['id']
            class_members = ClassMember.objects.filter(class_id=class_id)

            serializer.data[i]['members'] = []
            for class_member in class_members:
                user = UserSerializer(class_member.user_id).data
                member = {
                    'member_id': class_member.id,
                    'first_name': user.get('first_name'),
                    'last_name': user.get('last_name'),
                    'email': user.get('email'),
                    'role': class_member.role,
                    'status': class_member.status
                }
                
                serializer.data[i]['members'].append(member)
        return Response(serializer.data)
    
    
    @swagger_auto_schema(operation_description="GET /classes/{id}")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    
    @swagger_auto_schema(operation_description="PUT /classes/{id}")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    
    @swagger_auto_schema(operation_description="PATCH /classes/{id}")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    
    @swagger_auto_schema(operation_description="DELETE /classes/{id}")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_description="POST /classes/join", request_body=JoinClassSerializer)
    @action(methods=['POST'], detail=False, url_name='join')
    def join(self, request, *args, **kwargs):
        class_code = request.data['class_code']
        try:
            # check if user is already a member of the class
            class_member = ClassMember.objects.filter(user_id=request.user, class_id__class_code=class_code)
            if class_member:
                return Response({'details': 'You are already a member of this class'})
            
            class_to_join = Class.objects.get(class_code=class_code)
            class_member = ClassMember.objects.create(
                user_id=request.user,
                class_id=class_to_join
            )
            class_member.save()
            return Response({'details': 'Successfully joined class'})
        except:
            return Response({'details': 'Invalid class code'})