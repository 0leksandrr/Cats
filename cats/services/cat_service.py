from rest_framework.exceptions import ValidationError
from cats.models import SpyCat
from cats.serializers import SpyCatSerializer
import requests


class SpyCatService:
    """Service layer for SpyCat CRUD operations."""

    @staticmethod
    def validate_breed(breed: str) -> bool:
        """Validates the cat breed with an external API (TheCatAPI)."""
        url = f'https://api.thecatapi.com/v1/breeds'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValidationError("Could not fetch breed data from external API.")

        breeds = response.json()
        valid_breeds = [b['name'].lower() for b in breeds]
        if breed.lower() not in valid_breeds:
            raise ValidationError(f"{breed} is not a valid breed.")

    @staticmethod
    def create_spy_cat(data):
        """Creates a new SpyCat after validating the breed."""
        SpyCatService.validate_breed(data.get('breed'))
        serializer = SpyCatSerializer(data=data)
        if serializer.is_valid():
            spy_cat = serializer.save()
            return serializer.data
        raise ValidationError(serializer.errors)

    @staticmethod
    def update_spy_cat_salary(pk: int, salary: float) -> dict:
        """Update the salary of a SpyCat and return serialized data."""
        spy_cat = SpyCat.objects.get(pk=pk)

        spy_cat.salary = salary
        spy_cat.save()
        serializer = SpyCatSerializer(spy_cat)
        return serializer.data

    @staticmethod
    def delete_spy_cat(pk: int):
        spy_cat = SpyCat.objects.get(pk=pk)
        """Deletes a SpyCat."""
        spy_cat.delete()

    @staticmethod
    def get_spy_cat_by_id(pk: int):
        """Retrieve a SpyCat by its ID."""
        try:
            spy_cat = SpyCat.objects.get(pk=pk)
            serializer = SpyCatSerializer(spy_cat)
            return serializer.data  # Return serialized data
        except SpyCat.DoesNotExist:
            raise ValidationError(f"SpyCat with ID {pk} does not exist.")

    @staticmethod
    def list_spy_cats():
        """List all SpyCats."""
        spy_cats = SpyCat.objects.all()
        serializer = SpyCatSerializer(spy_cats, many=True)
        return serializer.data
