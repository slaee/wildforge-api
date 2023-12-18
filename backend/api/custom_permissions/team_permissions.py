from rest_framework.permissions import BasePermission

from api.models import TeamMember

class IsTeamLeader(BasePermission):
    def has_permission(self, request, view):
        return request.teammeber.role == TeamMember.LEADER

class IsTeamMember(BasePermission):
    def has_permission(self, request, view):
        return request.teammeber.role == TeamMember.MEMBER
    
