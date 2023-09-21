from django.urls import path
from .controllers import ClassesController

urlpatterns = [
    path('classes/', ClassesController.as_view({
        'post': 'createClass',
        'get': 'getAllClasses',
    }), name='POST | GET classes'),
    path('classes/<int:id>', ClassesController.as_view({
        'get': 'getClassById',
        'put': 'updateClass',
        'delete': 'deleteClass'
    }), name='GET | PUT | DELETE class'),
]