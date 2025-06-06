from django.urls import path
from . import views

app_name = 'health_insurance'

urlpatterns = [
    path('apply/', views.apply_for_health_insurance, name='apply_policy'),
    path('add-dependents/<int:policy_id>/', views.add_dependents, name='add_dependents'),
    path('add-health-history/<int:policy_id>/', views.add_health_history, name='add_health_history'),
    path('quote-summary/<int:policy_id>/', views.quote_summary, name='quote_summary'),



]