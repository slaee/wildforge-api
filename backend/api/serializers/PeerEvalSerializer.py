from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from api.models import PeerEval

class PeerEvalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerEval
        fields = ['id', 'name', 'forms_link', 'class_id']
        labels = {
            'name': 'Peer Evaluation Name',
            'forms_link': 'Google Forms Link'
        }
        
    class_assigned = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='class-class-members-list',
        parent_lookup_kwargs={'class_pk': 'class_id'}
    )

    class_id = serializers.PrimaryKeyRelatedField(
        queryset=PeerEval.objects.all(),
        source='class_assigned',
        write_only=True,
        required=False
    )

    def create(self, validated_data):
        class_assigned = validated_data.pop('class_assigned')
        peer_eval = PeerEval.objects.create(**validated_data)
        for class_member in class_assigned:
            peer_eval.class_assigned.add(class_member)
        return peer_eval
    
    