from rest_framework.exceptions import ValidationError
from missions.models import Mission, Target
from cats.models import SpyCat
from missions.serializers import MissionSerializer, TargetSerializer


class MissionService:

    @staticmethod
    def create_mission_with_targets(data):
        """
        Logic for creating a mission with associated targets.
        """
        try:
            name = data['name']
            targets_data = data['targets']

            mission = Mission.objects.create(
                name=name,
            )

            for target_data in targets_data:
                Target.objects.create(
                    mission=mission,
                    name=target_data['name'],
                    country=target_data['country'],
                    notes=target_data.get('notes', ''),
                    is_completed=target_data.get('is_completed', False)
                )

            # Return serialized mission data
            mission_serializer = MissionSerializer(mission)
            return mission_serializer.data

        except KeyError:
            raise ValidationError("Missing required fields for mission or targets.")

    @staticmethod
    def delete_mission(mission_id):
        """
        Logic for deleting a mission if it's not assigned to a cat.
        """
        try:
            mission = Mission.objects.get(pk=mission_id)
            if mission.cat:
                raise ValidationError("Mission cannot be deleted as it is assigned to a cat.")
            mission.delete()
        except Mission.DoesNotExist:
            raise ValidationError("Mission not found.")

    @staticmethod
    def update_target(mission_id, target_id, data):
        """
        Logic for updating a target's details.
        """
        try:
            mission = Mission.objects.get(pk=mission_id)
            target = Target.objects.get(pk=target_id, mission=mission)

            if 'notes' in data:
                target.notes = data['notes']
            if 'is_completed' in data:
                target.is_completed = data['is_completed']

            target.save()

            target_serializer = TargetSerializer(target)
            return target_serializer.data
        except Mission.DoesNotExist:
            raise ValidationError("Mission not found.")
        except Target.DoesNotExist:
            raise ValidationError("Target not found.")

    @staticmethod
    def assign_cat_to_mission(mission_id, data):
        """
        Logic for assigning a cat to a mission.
        """
        try:
            mission = Mission.objects.get(pk=mission_id)
            cat = SpyCat.objects.get(id=data.get('cat_id'))

            mission.cat = cat
            mission.save()

            mission_serializer = MissionSerializer(mission)
            return mission_serializer.data
        except Mission.DoesNotExist:
            raise ValidationError("Mission not found.")
        except SpyCat.DoesNotExist:
            raise ValidationError("Cat not found.")

    @staticmethod
    def get_mission_details(mission_id):
        """
        Logic for getting details of a single mission.
        """
        try:
            mission = Mission.objects.get(pk=mission_id)
            mission_serializer = MissionSerializer(mission)
            return mission_serializer.data
        except Mission.DoesNotExist:
            raise ValidationError("Mission not found.")

    @staticmethod
    def get_all_missions():
        """
        Logic for getting all missions.
        """
        missions = Mission.objects.all()
        mission_serializer = MissionSerializer(missions, many=True)
        return mission_serializer.data
