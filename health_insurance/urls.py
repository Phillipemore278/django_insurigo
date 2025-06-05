from django.urls import path
from . import views

app_name = 'health_insurance'

urlpatterns = [
    path('apply/', views.apply_for_health_insurance, name='apply_policy'),
    path('add-dependents/<int:policy_id>/', views.add_dependents, name='add_dependents'),
]