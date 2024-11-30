from rest_framework import serializers
from .models import SpyCat
from .utils import validate_breed


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = ['id', 'name', 'years_of_experience', 'breed', 'salary']

    def validate_breed(self, value):
        validate_breed(value)
        return value
