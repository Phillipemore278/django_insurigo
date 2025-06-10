from django.urls import path

from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('get-quote-now/', views.frontend_get_quote, name='frontend_get_quote'),
]