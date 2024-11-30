from django.urls import path
from .views import SpyCatListCreateView, SpyCatDetailView

urlpatterns = [
    path('cats/', SpyCatListCreateView.as_view(), name='cat-list-create'),
    path('cats/<int:pk>/', SpyCatDetailView.as_view(), name='cat-detail'),
]
