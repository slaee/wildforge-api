from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework import status

from api.models import Class
from api.serializers import ClassesSerializer

class ClassesController(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Class.objects.all()
    serializer_class = ClassesSerializer

    @action(methods=['GET'], detail=False)
    def getAllClasses(self, request):
        instance = self.get_queryset()
        data = []
        for classes in instance:
            data.append(ClassesSerializer(classes).data)
        return Response(data)
    
    @action(methods=['GET'], detail=True)
    def getClassById(self, request, id):
        instance = self.get_queryset().filter(id=id).first()
        if instance is None:
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(ClassesSerializer(instance).data)
    
    @action(methods=['POST'], detail=False)
    def createClass(self, request):
        data = request.data
        newClass = Class()
        newClass.name = data['name']
        newClass.sections = data['sections']
        newClass.schedule = data['schedule']
        newClass.save()
        return Response(ClassesSerializer(newClass).data)
    
    @action(methods=['PUT'], detail=True)
    def updateClass(self, request, id):
        data = request.data
        instance = self.get_queryset().filter(id=id).first()
        if instance is None:
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)
        instance.name = data['name']
        instance.sections = data['sections']
        instance.schedule = data['schedule']
        instance.save()
        return Response(ClassesSerializer(instance).data)
    
    @action(methods=['DELETE'], detail=True)
    def deleteClass(self, request, id):
        instance = self.get_queryset().filter(id=id).first()
        if instance is None:
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response({"success": "Class deleted"})