from rest_framework.permissions import BasePermission

from api.models import ClassMember

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.classmember.role == ClassMember.TEACHER
    
class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.classmember.role == ClassMember.STUDENT
    
class IsClassMember(BasePermission):
    def has_permission(self, request, view):
        return request.classmember.status == ClassMember.ACCEPTED