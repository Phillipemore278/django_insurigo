from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('make-payment/<str:policy_type>/<int:policy_id>/', views.make_payment, name='make_payment'),
    path('payment-success/<str:policy_number>/', views.payment_success, name='payment_success'),

]
