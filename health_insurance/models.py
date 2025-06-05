from django.db import models
from django.conf import settings

class Dependent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dependents')
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    relationship = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.relationship})"

class HealthHistory(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='health_history')
    conditions = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Health History for {self.user.username}"

class Provider(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class HealthPolicy(models.Model):
    POLICY_TYPE = 'health'
    policy_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='health_policies')
    start_date = models.DateField()
    end_date = models.DateField()
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    PLAN_CHOICES = [
        ('hmo', 'HMO'),
        ('ppo', 'PPO'),
        ('epo', 'EPO'),
    ]
    plan_type = models.CharField(max_length=10, choices=PLAN_CHOICES)
    dependents = models.ManyToManyField(Dependent, blank=True)
    add_ons = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Health Policy {self.policy_number} - {self.get_plan_type_display()}"

class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.provider.name} on {self.appointment_date}"
