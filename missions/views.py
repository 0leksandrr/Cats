from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.exceptions.base import ApplicationException

from missions.services.mission_service import MissionService


class MissionView(APIView):
    """
    A view to handle mission creation, deletion, updating targets, and assigning cats.
    """
    def post(self, request):
        """
        Create a mission with associated targets in one request.
        """
        try:
            mission_data = MissionService.create_mission_with_targets(request.data)
            return Response(mission_data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ApplicationException as e:
            return Response({"error": e.message}, status=e.status_code)

    def delete(self, request, pk):
        """
        Delete a mission if it is not assigned to a cat.
        """
        try:
            MissionService.delete_mission(pk)
            return Response({"message": "Mission deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ApplicationException as e:
            return Response({"error": e.message}, status=e.status_code)

    def patch(self, request, pk, *args, **kwargs):
        """
        Update a mission target or assign a cat to a mission.
        """
        target_id = kwargs.get("target_id")

        try:
            if target_id:
                updated_target = MissionService.update_target(pk, target_id, request.data)
                return Response(updated_target, status=status.HTTP_200_OK)
            else:
                assigned_cat = MissionService.assign_cat_to_mission(pk, request.data)
                return Response(assigned_cat, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ApplicationException as e:
            return Response({"error": e.message}, status=e.status_code)

    def get(self, request, pk=None):
        """
        List all missions or get details of a single mission.
        """
        try:
            if pk:
                mission_data = MissionService.get_mission_details(pk)
                return Response(mission_data, status=status.HTTP_200_OK)
            else:
                missions = MissionService.get_all_missions()
                return Response(missions, status=status.HTTP_200_OK)
        except ApplicationException as e:
            return Response({"error": e.message}, status=e.status_code)
