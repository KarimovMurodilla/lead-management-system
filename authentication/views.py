from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer
)

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login view that returns user info along with tokens"""
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Get user info
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                user_data = UserProfileSerializer(user).data
                
                # Add user info to response
                response.data['user'] = user_data
        
        return response

class UserRegistrationView(generics.CreateAPIView):
    """Register new attorney/admin users"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAuthenticated]  # Only existing staff can create new users
    
    def perform_create(self, serializer):
        # Only staff users can create new accounts
        if not self.request.user.is_staff:
            raise PermissionDenied("Only staff members can create new accounts")
        
        user = serializer.save()
        user.is_staff = True  # Make new users staff by default
        user.save()

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout user by blacklisting refresh token"""
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token_view(request):
    """Verify if token is valid and return user info"""
    user_data = UserProfileSerializer(request.user).data
    return Response({'user': user_data, 'valid': True}, status=status.HTTP_200_OK)
