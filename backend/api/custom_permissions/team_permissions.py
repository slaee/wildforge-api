from rest_framework.permissions import BasePermission

from api.models import TeamMember

class IsTeamLeader(BasePermission):
    def has_permission(self, request, view):
        return request.team_member.role == TeamMember.LEADER

class IsTeamMember(BasePermission):
    def has_permission(self, request, view):
        return request.team_member.role == TeamMember.MEMBER
    
