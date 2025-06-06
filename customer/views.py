from django.shortcuts import get_object_or_404, render
from datetime import datetime
from django.contrib.auth.decorators import login_required
from car_insurance.models import CarPolicy
from health_insurance.models import HealthPolicy,  HealthHistory

@login_required
def user_dashboard_view(request):

    current_date = datetime.now().strftime("%A, %b %d, %Y")
    context = {
        'current_date':current_date,
    }
    return render(request, 'customer/user_dashboard.html', context)


@login_required
def my_policies(request):
    car_policies = CarPolicy.objects.filter(user=request.user)
    health_policies = HealthPolicy.objects.filter(user=request.user)

    return render(request, 'customer/my_policies.html', {
        'car_policies': car_policies,
        'health_policies': health_policies,
    })


@login_required
def policy_detail(request, policy_type, policy_id):
    health_history = None  # Initialize here to avoid reference error
    
    if policy_type == 'car':
        policy = get_object_or_404(CarPolicy, id=policy_id, user=request.user)
        context = {'policy': policy, 'policy_type': policy_type}

    elif policy_type == 'health':
        policy = get_object_or_404(HealthPolicy, id=policy_id, user=request.user)
        try:
            health_history = HealthHistory.objects.get(user=request.user)
        except HealthHistory.DoesNotExist:
            health_history = None
        context = {
            'policy': policy,
            'policy_type': policy_type,
            'health_history': health_history
        }

    else:
        return render(request, '404.html', status=404)

    return render(request, 'customer/policy_detail.html', context)

