from django.db import models
from django.conf import settings

class Payment(models.Model):
    POLICY_TYPE_CHOICES = [
        ('car', 'Car Insurance'),
        ('health', 'Health Insurance'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    policy_id = models.PositiveIntegerField()  # Generic ID for Car or Health Policy
    policy_type = models.CharField(max_length=10, choices=POLICY_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    success = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.email} - {self.policy_type} - {self.amount}"

    def get_policy(self):
        if self.policy_type == 'car':
            from car_insurance.models import CarPolicy
            return CarPolicy.objects.filter(id=self.policy_id).first()
        elif self.policy_type == 'health':
            from health_insurance.models import HealthPolicy
            return HealthPolicy.objects.filter(id=self.policy_id).first()
        return None

