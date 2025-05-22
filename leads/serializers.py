from rest_framework import serializers
from .models import Lead

class LeadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'email', 'resume']
    
    def validate_resume(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB
            raise serializers.ValidationError("Resume file size must be under 5MB.")
        return value

class LeadListSerializer(serializers.ModelSerializer):
    resume_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Lead
        fields = [
            'id', 'first_name', 'last_name', 'email', 
            'resume_url', 'status', 'created_at', 'updated_at'
        ]
    
    def get_resume_url(self, obj):
        request = self.context.get('request')
        if obj.resume and request:
            return request.build_absolute_uri(obj.resume.url)
        return None

class LeadUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['status']
