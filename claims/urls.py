from django.urls import path
from . import views

app_name = 'claims'

urlpatterns = [
    path('file/<str:policy_type>/<int:policy_id>/', views.file_claim, name='file_claim'),
    path('success/<int:claim_id>/', views.claim_success, name='claim_success'),
]