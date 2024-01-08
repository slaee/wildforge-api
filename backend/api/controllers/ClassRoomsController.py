from rest_framework import viewsets, mixins, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.db.models import F, OuterRef, Subquery, Q


from api.custom_permissions import IsModerator

from api.models import ClassRoom
from api.models import ClassMember
from api.models import PeerEval
from api.models import ClassRoomPE
from api.models import TeamMember

from api.serializers import ClassRoomSerializer
from api.serializers import ClassMemberSerializer
from api.serializers import JoinClassRoomSerializer
from api.serializers import UserSerializer
from api.serializers import SuperUserSerializer
from api.serializers import PeerEvalSerializer
from api.serializers import TeamMemberSerializer

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
        if self.action in ['create','destroy', 'update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsModerator()]
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
        """
        Creates a new class and adds the user as a teacher of the class.
        """
        response = super().create(request, *args, **kwargs)
        try:
            new_class = ClassRoom.objects.get(id=response.data['id'])
            class_member = ClassMember.objects.create(
                user_id=request.user,
                class_id=new_class,
                role=ClassMember.TEACHER,
                status=ClassMember.ACCEPTED
            )
            class_member.save()
        except:
            return Response({'details': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

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
        """
        Lists all classes that the user is a member of.
        This function will depend on the user's role.
        If superuser, return all classes otherwise, return classes that the user is a member of
        """
        try:
            user = SuperUserSerializer(request.user).data            
            if user.get('is_superuser'):
                queryset = ClassRoom.objects.all()
                serializer = self.get_serializer(queryset, many=True)
            else:
                queryset = ClassRoom.objects.filter(classmember__user_id=request.user, classmember__status=ClassMember.ACCEPTED)
                serializer = self.get_serializer(queryset, many=True)
        except:
            # <DEV ONLY>
            queryset = ClassRoom.objects.all()
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
        """
        Retrieves a class that the user is a member of.
        """
        class_id = kwargs['pk']
        try:
            ClassRoom.objects.get(id=class_id)
        except ClassRoom.DoesNotExist:
            return Response({'details': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        class_member = ClassMember.objects.filter(user_id=request.user, class_id=class_id)
        if not class_member:
            return Response({'details': 'You are not a member of this class'}, status=status.HTTP_401_UNAUTHORIZED)
        
        response = super().retrieve(request, *args, **kwargs)

        # count number of members
        roles = [ClassMember.TEACHER, ClassMember.STUDENT]
        number_of_students = ClassMember.objects.filter(class_id=class_id, role__in=roles, status=ClassMember.ACCEPTED).count()
        response.data['number_of_students'] = number_of_students
        
        return response
    
    
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
        """
        Updates a class.
        """
        return super().update(request, *args, **kwargs)
    
    
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
        """
        Updates a class partially.
        """
        return super().partial_update(request, *args, **kwargs)
    
    
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
        """
        Deletes a class by class id as path parameter.
        """
        return super().destroy(request, *args, **kwargs)
    
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
        """
        Joins a class by class code as request body.
        """
        class_code = request.data['class_code']
        try:
            # check if user is already a member of the class
            class_member = ClassMember.objects.filter(user_id=request.user, class_id__class_code=class_code)
            if class_member:
                return Response({'details': 'You already joined the class'})
            
            class_to_join = ClassRoom.objects.get(class_code=class_code)
            class_member = ClassMember.objects.create(
                user_id=request.user,
                class_id=class_to_join,
                role=ClassMember.STUDENT,
                status=ClassMember.PENDING,
            )
            class_member.save()
            return Response({'details': 'Partially joined class'}, status=status.HTTP_200_OK)
        except ClassRoom.DoesNotExist:
            return Response({'error': 'Invalid class code'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Lists all noneleaders of a class",
        operation_description="GET /classes/{id}/noneleaders",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', ClassRoomSerializer(many=True)),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_404_NOT_FOUND: openapi.Response('Not Found'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    @action(detail=True, methods=['GET'])
    def noneleaders(self, request, *args, **kwargs):
        try:
            class_id = kwargs['pk']

            class_members = ClassMember.objects.filter(
                class_id=class_id, 
                role=ClassMember.STUDENT
            ).annotate(
                teammember_status=Subquery(
                    TeamMember.objects.filter(
                        class_member_id_id=OuterRef('pk'),  # Assuming ForeignKey from ClassMember to TeamMember is named 'classmember'
                        status=TeamMember.PENDING
                    ).values('status')[:1]
                )
            ).filter(
                Q(teammember__isnull=True) | Q(teammember_status=TeamMember.PENDING)
            )

            none_leaders = []
            for class_member in class_members:
                user = UserSerializer(class_member.user_id).data
                member = {
                    'class_member_id': class_member.id,
                    'first_name': user.get('first_name'),
                    'last_name': user.get('last_name'),
                    'teamember_status': class_member.teammember_status
                }
                none_leaders.append(member)
            return Response(none_leaders, status=status.HTTP_200_OK)
        except ClassRoom.DoesNotExist:
            return Response({'details': 'Classroom not found'}, status=status.HTTP_404_NOT_FOUND)
        except ClassMember.DoesNotExist:
            return Response({'details': 'Class member not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'details': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(
        operation_summary="Lists all peer evals of a class",
        operation_description="GET /classes/{id}/evals",
        responses={
            status.HTTP_200_OK: openapi.Response('OK', ClassRoomSerializer(many=True)),
            status.HTTP_400_BAD_REQUEST: openapi.Response('Bad Request'),
            status.HTTP_401_UNAUTHORIZED: openapi.Response('Unauthorized'),
            status.HTTP_403_FORBIDDEN: openapi.Response('Forbidden'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('Internal Server Error'),
        }
    )
    @action(detail=True, methods=['GET'])
    def evals(self, request, *args, **kwargs):
        try:
            class_id = kwargs['pk']
            class_room_pe = ClassRoomPE.objects.filter(class_id=class_id)
            evals = PeerEval.objects.filter(id__in=class_room_pe.values('peer_eval_id'))
            serializer = PeerEvalSerializer(evals, many=True).data

            return Response(serializer, status=status.HTTP_200_OK)
        except ClassRoom.DoesNotExist:
            return Response({'details': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)
        except PeerEval.DoesNotExist:
            return Response({'details': 'Peer eval not found'}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({'details': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    