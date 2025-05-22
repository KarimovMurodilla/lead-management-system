from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from leads.models import Lead

class LeadModelTest(TestCase):
    def setUp(self):
        self.resume_file = SimpleUploadedFile(
            "test_resume.pdf",
            b"file_content",
            content_type="application/pdf"
        )
    
    def test_lead_creation(self):
        lead = Lead.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            resume=self.resume_file
        )
        self.assertEqual(lead.first_name, "John")
        self.assertEqual(lead.last_name, "Doe")
        self.assertEqual(lead.email, "john@example.com")
        self.assertEqual(lead.status, Lead.PENDING)
    
    def test_lead_str_representation(self):
        lead = Lead.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            resume=self.resume_file
        )
        self.assertEqual(str(lead), "Jane Smith - jane@example.com")
