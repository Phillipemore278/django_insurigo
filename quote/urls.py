from django.urls import path
from .views import ping_supabase

app_name = 'quote'

urlpatterns = [
    path('ping/', ping_supabase),
]
