from django.shortcuts import render

def user_dashboard_view(request):
    return render(request, 'customer/user_dashboard.html')
