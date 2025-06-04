from django.urls import path

from . import views

app_name = 'customer'

urlpatterns = [
    path('dashboard/', views.user_dashboard_view, name='user_dashboard'),
]