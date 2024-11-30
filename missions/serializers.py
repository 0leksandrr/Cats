from rest_framework import serializers
from .models import Mission, Target


class TargetSerializer(serializers.ModelSerializer):
    """Serializer for targets."""
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'is_completed']


class MissionSerializer(serializers.ModelSerializer):
    """Serializer for missions, including targets."""
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['id', 'name', 'cat', 'is_completed', 'created_at', 'targets']

    def create(self, validated_data):
        """Create a mission with its targets."""
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission
