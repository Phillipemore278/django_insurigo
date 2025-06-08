from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .managers import CustomAccountManager


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # country = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"
        ordering = ('-created',)
        

    def __str__(self):
        return self.full_name+ ', ' + self.email
    

class Profile(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=300,blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20,blank=True, null=True)
    country = models.CharField(max_length=70, null=True, blank=True)
    socials = models.CharField(max_length=100, blank=True, null=True)
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.full_name}"
    
@receiver(post_save, sender=Customer)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)