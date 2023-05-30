from django.http import JsonResponse

from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response

from classes.models import Class
from classes.serializers import ClassesSerializer

@api_view(['GET', 'POST', 'PUT'])
def api_classes(request, *args, **kwargs):
    if request.method == 'POST':
        serializer = ClassesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PUT':
        id = request.data.get('id')
        classes = Class.objects.get(id=id)
        if classes is None:
            return Response({"error": "Class not found"})
        serializer = ClassesSerializer(classes, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'GET':
        instance = Class.objects.all()
        data = []
        for classes in instance:
            data.append(ClassesSerializer(classes).data)
        return Response(data)
    else:
        return Response({"error": "Invalid Request"})
    
@api_view(['DELETE'])
def api_classes_delete(request, id, *args, **kwargs):
    if request.method == 'DELETE':
        instance = Class.objects.get(id=id)
        instance.delete()
        return Response({"success": "Class deleted"})
    else:
        return Response({"error": "Invalid Request"})
