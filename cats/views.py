from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .services.cat_service import SpyCatService
from .serializers import SpyCatSerializer
from rest_framework.exceptions import ValidationError


class SpyCatListCreateView(APIView):
    """Handles listing and creating Spy Cats."""

    def get(self, request):
        """List all Spy Cats."""
        try:
            spy_cats = SpyCatService.list_spy_cats()
            serializer = SpyCatSerializer(spy_cats, many=True)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Create a new Spy Cat."""
        try:
            spy_cat = SpyCatService.create_spy_cat(request.data)
            serializer = SpyCatSerializer(spy_cat)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SpyCatDetailView(APIView):
    """Handles retrieving, updating, and deleting a single Spy Cat."""

    def get(self, request, pk):
        """Retrieve a single Spy Cat."""
        try:
            return Response(SpyCatService.get_spy_cat_by_id(pk))
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Partially update a single Spy Cat."""
        try:
            salary = request.data.get('salary')  # Only update salary
            if salary is not None:
                return Response(SpyCatService.update_spy_cat_salary(pk, salary))
            return Response({"error": "Salary is required."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a single Spy Cat."""
        try:
            SpyCatService.delete_spy_cat(pk)
            return Response({"message": "Spy Cat deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
