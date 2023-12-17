from rest_framework import viewsets, mixins, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from api.models import ClassRoom
from api.models import ClassMember
from api.serializers import ClassRoomSerializer
from api.serializers import UserSerializer
from api.serializers import SuperUserSerializer
from api.serializers import JoinClassRoomSerializer

class ClassRoomsController(viewsets.GenericViewSet,
                      mixins.ListModelMixin, 
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
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
        operation_summary="Creates a new class",
        operation_description="POST /classes",
        request_body=ClassRoomSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response('Created', ClassRoomSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def create(self, request, *args, **kwargs):
        pass
        # """
        # Creates a new class and adds the user as a teacher of the class.
        # """
        # response = super().create(request, *args, **kwargs)
        # new_class = ClassRoom.objects.get(id=response.data['id'])
        # class_member = ClassMember.objects.create(
        #     user_id=request.user,
        #     class_id=new_class,
        #     role='t',
        #     status='accepted'
        # )
        # class_member.save()
        # return response


    @swagger_auto_schema(
        operation_summary="Lists all classes",
        operation_description="GET /classes",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', ClassRoomSerializer(many=True)),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def list(self, request, *args, **kwargs):
        pass
        # """
        # Lists all classes that the user is a member of.
        # This function will depend on the user's role.
        #     if superuser, return all classes
        #     otherwise, return classes that the user is a member of
        # """
        # # JOIN ClassMembers ON ClassMembers.class_id = ClassRoom.id LEFT JOIN Users ON Users.id = ClassMembers.user_id
        # try:
        #     user = SuperUserSerializer(request.user).data            
        #     if user.get('is_superuser'):
        #         queryset = ClassRoom.objects.all()
        #         serializer = self.get_serializer(queryset, many=True)
        #     else:
        #         queryset = ClassRoom.objects.filter(classmember__user_id=request.user, classmember__status='accepted')
        #         serializer = self.get_serializer(queryset, many=True)
        # except:
        #     # <DEV ONLY>
        #     queryset = ClassRoom.objects.all()
        #     serializer = self.get_serializer(queryset, many=True)
        #     # </DEV ONLY>

        # for i in range(len(serializer.data)):
        #     class_id = serializer.data[i]['id']
        #     class_members = ClassMember.objects.filter(class_id=class_id)

        #     serializer.data[i]['members'] = []
        #     for class_member in class_members:
        #         user = UserSerializer(class_member.user_id).data
        #         member = {
        #             'member_id': class_member.id,
        #             'first_name': user.get('first_name'),
        #             'last_name': user.get('last_name'),
        #             'email': user.get('email'),
        #             'role': class_member.role,
        #             'status': class_member.status
        #         }
                
        #         serializer.data[i]['members'].append(member)
        # return Response(serializer.data)
    
    
    @swagger_auto_schema(
        operation_summary="Retrieves a class",
        operation_description="GET /classes/{id}",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', ClassRoomSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        pass
        # """
        # Retrieves a class that the user is a member of.
        # """
        # class_id = kwargs['pk']
        # try:
        #     ClassRoom.objects.get(id=class_id)
        # except ClassRoom.DoesNotExist:
        #     return Response({'details': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        # class_member = ClassMember.objects.filter(user_id=request.user, class_id=class_id)
        # if not class_member:
        #     return Response({'details': 'You are not a member of this class'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # data = super().retrieve(request, *args, **kwargs)

        # # count number of members
        # roles = ['tl', 's']
        # number_of_students = ClassMember.objects.filter(class_id=class_id, role__in=roles, status='accepted').count()
        # data.data['number_of_students'] = number_of_students
        
        # return data
    
    
    @swagger_auto_schema(
        operation_summary="Updates a class",
        operation_description="PUT /classes/{id}",
        request_body=ClassRoomSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response('OK', ClassRoomSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def update(self, request, *args, **kwargs):
        pass
        # """
        # Updates a class.
        # """
        # return super().update(request, *args, **kwargs)
    
    
    @swagger_auto_schema(
        operation_summary="Updates a class partially",
        operation_description="PATCH /classes/{id}",
        request_body=ClassRoomSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response('OK', ClassRoomSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        pass
        # """
        # Updates a class partially.
        # """
        # return super().partial_update(request, *args, **kwargs)
    
    
    @swagger_auto_schema(
        operation_summary="Deletes a class",
        operation_description="DELETE /classes/{id}",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response('No Content'),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    def destroy(self, request, *args, **kwargs):
        pass
        # """
        # Deletes a class by class id as path parameter.
        # """
        # return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        method='POST',
        operation_summary="Joins a class",
        operation_description="POST /classes/join", 
        request_body=JoinClassRoomSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response('OK', JoinClassRoomSerializer),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    @action(methods=['POST'], detail=False, url_name='join')
    def join(self, request, *args, **kwargs):
        pass
        # """
        # Joins a class by class code as request body.
        # """
        # class_code = request.data['class_code']
        # try:
        #     # check if user is already a member of the class
        #     class_member = ClassMember.objects.filter(user_id=request.user, class_id__class_code=class_code)
        #     if class_member:
        #         return Response({'details': 'You are already a member of this class'})
            
        #     class_to_join = ClassRoom.objects.get(class_code=class_code)
        #     class_member = ClassMember.objects.create(
        #         user_id=request.user,
        #         class_id=class_to_join
        #     )
        #     class_member.save()
        #     return Response({'details': 'Successfully joined class'}, status=status.HTTP_200_OK)
        # except ClassRoom.DoesNotExist:
        #     return Response({'error': 'Invalid class code'}, status=status.HTTP_400_BAD_REQUEST)
