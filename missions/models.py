from django.db import models


class Mission(models.Model):
    cat = models.ForeignKey('cats.SpyCat', null=True, blank=True, related_name='missions', on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Target(models.Model):
    mission = models.ForeignKey(Mission, related_name='targets', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
