from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView,
    UserRegistrationView,
    UserProfileView,
    logout_view,
    verify_token_view
)

urlpatterns = [
    # Authentication endpoints
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout_view, name='logout'),
    path('verify/', verify_token_view, name='verify_token'),
    
    # User management endpoints
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
