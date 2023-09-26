from rest_framework import serializers

from api.models import PeerEval

class PeerEvalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeerEval
        pass