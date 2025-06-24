from django.urls import path
from .views import ping_supabase

urlpatterns = [
    path('api/ping/', ping_supabase),
]
