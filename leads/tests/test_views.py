from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from leads.models import Lead

class LeadAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='attorney',
            password='testpass123'
        )
        self.resume_file = SimpleUploadedFile(
            "test_resume.pdf",
            b"file_content",
            content_type="application/pdf"
        )
    
    def test_create_lead_public(self):
        """Test that anyone can create a lead"""
        url = reverse('lead-create')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'resume': self.resume_file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lead.objects.count(), 1)
    
    def test_list_leads_requires_auth(self):
        """Test that listing leads requires authentication"""
        url = reverse('lead-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_leads_authenticated(self):
        """Test that authenticated users can list leads"""
        self.client.force_authenticate(user=self.user)
        Lead.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            resume=self.resume_file
        )
        
        url = reverse('lead-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_update_lead_status(self):
        """Test updating lead status"""
        self.client.force_authenticate(user=self.user)
        lead = Lead.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            resume=self.resume_file
        )
        
        url = reverse('lead-update', kwargs={'pk': lead.pk})
        data = {'status': Lead.REACHED_OUT}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        lead.refresh_from_db()
        self.assertEqual(lead.status, Lead.REACHED_OUT)
