from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('make_payment/<int:policy_id>/', views.make_payment, name='make_payment'),
    path('payment_success/<int:policy_id>/', views.payment_success, name='payment_success'),
]