from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import Lead
from .serializers import LeadCreateSerializer, LeadListSerializer, LeadUpdateSerializer
from .services import EmailService

class LeadCreateView(generics.CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadCreateSerializer
    permission_classes = [AllowAny]
    throttle_classes = []
    throttle_scope = 'anon'
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead = serializer.save()
        
        # Send email notifications
        email_service = EmailService()
        print(f"Sending email to some email")
        try:
            email_service.send_prospect_confirmation(lead)
            email_service.send_attorney_notification(lead)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Email sending failed: {str(e)}")
        
        return Response(
            LeadListSerializer(lead, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

class LeadListView(generics.ListAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadListSerializer
    permission_classes = [IsAuthenticated]

class LeadDetailView(generics.RetrieveAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadListSerializer
    permission_classes = [IsAuthenticated]

class LeadUpdateView(generics.UpdateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(
            LeadListSerializer(instance, context={'request': request}).data
        )
