import requests
from django.core.exceptions import ValidationError
from functools import lru_cache
from django.conf import settings

CAT_API_URL = settings.CAT_API_URL


@lru_cache(maxsize=1)
def get_valid_breeds():
    """Fetches the valid breeds from TheCatAPI, caching the result."""
    response = requests.get(CAT_API_URL)
    if response.status_code != 200:
        raise ValidationError("Unable to fetch breed data from TheCatAPI.")

    breeds = response.json()
    return {b['name'].lower() for b in breeds}


def validate_breed(breed):
    """Validates if the provided breed is valid."""
    valid_breeds = get_valid_breeds()

    if breed.lower() not in valid_breeds:
        raise ValidationError(f"The breed '{breed}' is not valid.")
