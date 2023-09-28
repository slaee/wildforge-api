from rest_framework import serializers

from api.models import ClassAssigned, Class, PeerEval


class ClassAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassAssigned
        fields = ['id', 'peer_eval_id', 'class_id']
        labels = {
            'peer_eval_id': 'Peer Evaluation ID',
            'class_id': 'Class ID'
        }

    def create(self, validated_data):
        peer_eval_id = validated_data.get('peer_eval_id')
        class_id = validated_data.get('class_id')

        # Check if peer_eval_id and class_id exist in the database
        if not Class.objects.filter(id=class_id).exists():
            raise serializers.ValidationError("Class ID does not exist.")

        if not PeerEval.objects.filter(id=peer_eval_id).exists():
            raise serializers.ValidationError("Peer Evaluation ID does not exist.")

        # Create the instance if both IDs exist
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance