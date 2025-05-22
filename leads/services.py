from mailjet_rest import Client
from django.conf import settings
from .models import Lead

class EmailService:
    def __init__(self):
        self.mailjet = Client(
            auth=(settings.MAILJET_API_KEY, settings.MAILJET_SECRET_KEY),
            version='v3.1'
        )
    
    def send_prospect_confirmation(self, lead: Lead):
        """Send confirmation email to the prospect"""
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": settings.MAILJET_FROM_EMAIL,
                        "Name": "Legal Team"
                    },
                    "To": [
                        {
                            "Email": lead.email,
                            "Name": f"{lead.first_name} {lead.last_name}"
                        }
                    ],
                    "Subject": "Thank you for your application",
                    "TextPart": f"""
Dear {lead.first_name} {lead.last_name},

Thank you for submitting your application. We have received your resume and will review it shortly.

Our team will contact you within 2-3 business days regarding next steps.

Best regards,
Legal Team
                    """,
                    "HTMLPart": f"""
<h3>Dear {lead.first_name} {lead.last_name},</h3>
<p>Thank you for submitting your application. We have received your resume and will review it shortly.</p>
<p>Our team will contact you within 2-3 business days regarding next steps.</p>
<p>Best regards,<br/>Legal Team</p>
                    """
                }
            ]
        }
        
        result = self.mailjet.send.create(data=data)
        return result.status_code == 200
    
    def send_attorney_notification(self, lead: Lead):
        """Send notification email to the attorney"""
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": settings.MAILJET_FROM_EMAIL,
                        "Name": "Lead Management System"
                    },
                    "To": [
                        {
                            "Email": settings.ATTORNEY_EMAIL,
                            "Name": "Attorney"
                        }
                    ],
                    "Subject": f"New Lead: {lead.first_name} {lead.last_name}",
                    "TextPart": f"""
New lead submission received:

Name: {lead.first_name} {lead.last_name}
Email: {lead.email}
Submitted: {lead.created_at.strftime('%Y-%m-%d %H:%M:%S')}
Status: {lead.status}

Please log in to the system to review the complete application and resume.
                    """,
                    "HTMLPart": f"""
<h3>New lead submission received:</h3>
<ul>
    <li><strong>Name:</strong> {lead.first_name} {lead.last_name}</li>
    <li><strong>Email:</strong> {lead.email}</li>
    <li><strong>Submitted:</strong> {lead.created_at.strftime('%Y-%m-%d %H:%M:%S')}</li>
    <li><strong>Status:</strong> {lead.status}</li>
</ul>
<p>Please log in to the system to review the complete application and resume.</p>
                    """
                }
            ]
        }
        
        result = self.mailjet.send.create(data=data)
        return result.status_code == 200
