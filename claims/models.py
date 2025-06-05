from django.db import models
from django.conf import settings

class Claim(models.Model):
    CLAIM_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid_out', 'Paid Out'),
    ]

    claim_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='claims')
    policy_number = models.CharField(max_length=20)  # Reference policy by number (or FK to policies in future)
    filed_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CLAIM_STATUS_CHOICES, default='pending')
    description = models.TextField()
    amount_claimed = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # documents = models.FileField(upload_to='claim_documents/', blank=True, null=True)

    def __str__(self):
        return f"Claim {self.claim_number} - {self.status}"
