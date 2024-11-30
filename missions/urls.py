from django.urls import path
from .views import MissionView

urlpatterns = [
    path('missions/', MissionView.as_view(), name='create-mission'),  # For creating a mission with targets
    path('missions/<int:pk>/', MissionView.as_view(), name='delete-mission'),  # For deleting a mission
    path('missions/<int:pk>/targets/<int:target_id>/', MissionView.as_view(), name='update-target'),  # For updating a target
    path('missions/<int:pk>/assign-cat/', MissionView.as_view(), name='assign-cat-to-mission'),  # For assigning a cat to a mission
    path('missions/list/', MissionView.as_view(), name='list-missions'),  # For listing all missions
    path('missions/<int:pk>/detail/', MissionView.as_view(), name='mission-detail'),  # For fetching mission details
]
