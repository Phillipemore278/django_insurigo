from django.urls import path

from . import views

app_name = 'customer'

urlpatterns = [
    path('dashboard/', views.user_dashboard_view, name='user_dashboard'),
    path('my-policies/', views.my_policies, name='my_policies'),
    path('my-policies/<str:policy_type>/<int:policy_id>/', views.policy_detail, name='policy_detail'),
    path('my-claims/', views.my_claims, name='my_claims'),
    path('get-quote/', views.get_quote, name='get_quote'),
    # path('quote-summary/', views.quote_summary, name='quote_summary'),
]