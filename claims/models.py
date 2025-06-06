from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings

class Claim(models.Model):
    CLAIM_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    policy_type = models.CharField(max_length=10, choices=[('car', 'Car Insurance'), ('health', 'Health Insurance')])
    policy_id = models.PositiveIntegerField()  # generic policy id
    date_of_incident = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=CLAIM_STATUS_CHOICES, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optionally: file upload for evidence
    # evidence = models.FileField(upload_to='claim_evidence/', blank=True, null=True)

    def __str__(self):
        return f"Claim #{self.id} by {self.user.email} for {self.policy_type} policy {self.policy_id}"

