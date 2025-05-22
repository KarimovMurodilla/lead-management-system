from django.urls import path
from .views import LeadCreateView, LeadListView, LeadDetailView, LeadUpdateView

urlpatterns = [
    path('', LeadCreateView.as_view(), name='lead-create'),
    path('list/', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
]
