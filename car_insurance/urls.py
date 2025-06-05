from django.urls import path

from . import views

app_name = 'car_insurance'

urlpatterns = [
    path('apply-for-car-isurance/', views.apply_for_car_insurance, name='apply_for_car_insurance'),
    path('quote_confirmation/<int:policy_id>/', views.quote_confirmation, name='quote_confirmation'),
]