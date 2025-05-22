from django.db import models
from django.core.validators import FileExtensionValidator

class Lead(models.Model):
    PENDING = 'PENDING'
    REACHED_OUT = 'REACHED_OUT'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (REACHED_OUT, 'Reached Out'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])]
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
