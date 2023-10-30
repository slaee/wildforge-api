from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from api.models import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'max_members', 'status', 'team_member']
        labels = {
            'name': 'Team Name',
            'description': 'Team Description',
            'max_members': 'Maximum number of members',
            'status': 'Hiring Status'
        }

        # set default values
        extra_kwargs = {
            'description': {'required': False},
            'max_members': {'default': 4},
            'status': {'default': 'open'}
        }
    
    team_member = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='team-team-members-list',
        parent_lookup_kwargs={'team_pk': 'team_id'}
    )

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
class JoinTeamSerializer (serializers.Serializer):
    team_id = serializers.IntegerField()

    class Meta:
        ref_name = 'JoinTeamInput'