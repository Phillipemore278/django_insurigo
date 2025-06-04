from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('register/', views.register_view, name='register'),
]