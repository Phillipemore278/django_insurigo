from django.db import models
from django.contrib.auth.models import User
# from claims.models import Claim
# from payments.models import Payment
# from health_insurance.models import Policy 
from django.conf import settings


class Vehicle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles')
    vin = models.CharField(max_length=17, unique=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    value = models.DecimalField(max_digits=12, decimal_places=2)
    garage_address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.vin})"


class CarPolicy(models.Model):
    POLICY_TYPE = 'car'
    policy_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='car_policies')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='policies')
    start_date = models.DateField()
    end_date = models.DateField()
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    COVERAGE_CHOICES = [
        ('third_party', 'Third Party Liability'),
        ('comprehensive', 'Comprehensive'),
        ('collision', 'Collision'),
        ('roadside', 'Roadside Assistance'),
        ('rental', 'Rental Coverage'),
    ]
    coverage_type = models.CharField(max_length=20, choices=COVERAGE_CHOICES)

    def __str__(self):
        return f"Car Policy {self.policy_number} for {self.vehicle}"
